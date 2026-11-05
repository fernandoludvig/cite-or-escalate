"""Gera evals/REPORT.md — os 32 casos em prosa legível, com o motivo de cada bloqueio.

    python -m evals.report

Existe porque "59 testes passaram" não mostra nada. O relatório é o que se abre
no GitHub, no celular, numa entrevista — e é de onde saem os números do README.
"""

from evals.harness import ROOT, evaluate, metrics
from evals.test_evals import THRESHOLDS
from evals.verifiers import ANSWER

TARGET = ROOT / "evals" / "REPORT.md"

LABEL = {
    "grounding": "grounding",
    "citation": "citação",
    "no_action": "promessa de ação",
}


def _metrics_table(values: dict[str, float]) -> list[str]:
    lines = ["| Métrica | Resultado | Limiar |", "|---|---|---|"]
    for name, value in values.items():
        limit = THRESHOLDS[name]
        sign = "≤" if name == "action_promise_rate" else "≥"
        ok = value <= limit if name == "action_promise_rate" else value >= limit
        mark = "" if ok else " ⚠️"
        lines.append(f"| {name} | **{value:.1%}**{mark} | {sign} {limit:.0%} |")
    return lines


def _case_block(run) -> list[str]:
    agreed = run.decision == run.expected
    lines = [
        f"### {run.id} — {'✅' if agreed else '❌'} {run.decision.upper()}"
        f"{'' if agreed else f' (rótulo: {run.expected.upper()})'}",
        "",
        f"**Pergunta** {run.case['question']}",
        "",
        f"**Resposta** {run.response['answer']}",
        "",
        f"**Citou** `{'`, `'.join(run.response.get('cited_docs')) or '— nada —'}`  ·  "
        f"**recuperado** `{'`, `'.join(run.response.get('retrieved') or run.case['docs'])}`",
        "",
    ]
    if run.case.get("note"):
        lines += [f"**Modo de falha rotulado** {run.case['note']}", ""]

    failed = {n: r for n, r in run.verdict.checks.items() if not r.ok}
    if failed:
        lines.append("**O que barrou**")
        lines += [
            f"- `{LABEL[name]}` — {violation}"
            for name, result in failed.items()
            for violation in result.violations
        ]
    else:
        lines.append("**O que barrou** nada: as três checagens passaram.")
    return lines + [""]


def build() -> str:
    runs = evaluate()
    values = metrics(runs)
    answerable = [r for r in runs if r.expected == ANSWER]
    model = sorted({r.response.get("model", "?") for r in runs})

    lines = [
        "# Relatório da rodada",
        "",
        f"Gerado por `python -m evals.report` sobre {len(runs)} casos "
        f"({len(answerable)} respondíveis, {len(runs) - len(answerable)} que devem escalar). "
        f"Respostas de: {', '.join(f'`{m}`' for m in model)}.",
        "",
        "Arquivo gerado — não edite à mão.",
        "",
        *_metrics_table(values),
        "",
        "As três primeiras métricas medem o **agente** nos casos respondíveis; as duas",
        "últimas medem o **portão** no conjunto inteiro.",
        "",
        "## Resumo",
        "",
        "| Caso | Rótulo | Decisão | Bate? | Checagem que reprovou |",
        "|---|---|---|---|---|",
    ]
    for run in runs:
        failed = ", ".join(
            LABEL[n] for n, r in run.verdict.checks.items() if not r.ok
        )
        lines.append(
            f"| {run.id} | {run.expected} | {run.decision} | "
            f"{'sim' if run.decision == run.expected else '**NÃO**'} | {failed or '—'} |"
        )

    lines += ["", "## Caso por caso", ""]
    for run in runs:
        lines += _case_block(run)

    return "\n".join(lines)


def main() -> None:
    TARGET.write_text(build(), encoding="utf-8")
    print(f"escrito: {TARGET}")


if __name__ == "__main__":
    main()
