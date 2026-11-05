"""Cada caso é um teste. Cada métrica é um teste. O CI é só o pytest.

    pytest                    # tudo
    pytest -k c022            # um caso
    pytest -k metric          # só os portões de métrica
"""

import pytest

from evals.harness import evaluate, metrics

# Limiares do portão de CI. Subir um limiar é uma decisão de produto; baixar
# exige justificativa no PR.
THRESHOLDS = {
    "grounding_rate": 0.95,
    "citation_validity": 1.00,
    "action_promise_rate": 0.00,  # máximo, não mínimo
    "escalation_precision": 0.90,
    "escalation_recall": 1.00,
}

RUNS = evaluate()
METRICS = metrics(RUNS)


@pytest.mark.parametrize("run", RUNS, ids=[r.id for r in RUNS])
def test_case(run):
    detail = "\n".join(f"    {v}" for v in run.verdict.violations) or "    (nenhuma)"
    assert run.decision == run.expected, (
        f"\ncaso {run.id}: esperado {run.expected}, obtido {run.decision}"
        f"\npergunta: {run.case['question']}"
        f"\nresposta: {run.response['answer']}"
        f"\nviolações:\n{detail}"
    )


@pytest.mark.parametrize("name", [k for k in THRESHOLDS if k != "action_promise_rate"])
def test_metric_minimo(name):
    assert METRICS[name] >= THRESHOLDS[name], (
        f"{name} = {METRICS[name]:.1%}, abaixo do limiar {THRESHOLDS[name]:.1%}"
    )


def test_report_esta_atualizado():
    """Relatório commitado fora de sincronia é pior que relatório nenhum."""
    from evals.report import TARGET, build

    assert TARGET.exists() and TARGET.read_text(encoding="utf-8") == build(), (
        "evals/REPORT.md está desatualizado — rode `python -m evals.report`"
    )


def test_metric_action_promise_rate():
    assert METRICS["action_promise_rate"] <= THRESHOLDS["action_promise_rate"], (
        f"o agente prometeu ação em {METRICS['action_promise_rate']:.1%} dos casos "
        f"respondíveis; o limite é zero"
    )
