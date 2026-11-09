"""Carrega dataset + respostas, roda o portão em cada caso, calcula as métricas."""

import json
from dataclasses import dataclass
from pathlib import Path

from agent.retrieval import load_corpus
from evals.verifiers import ANSWER, ESCALATE, Verdict, decide

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "evals" / "dataset"
REGRESSIONS = ROOT / "evals" / "regressions"

CASE_FIELDS = {"id", "question", "docs", "expected", "expected_citation", "note"}


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_dataset(responses_path: Path = DATASET / "responses.jsonl") -> tuple[list[dict], dict[str, dict]]:
    """Casos e respostas, já com a pasta de regressões incluída.

    Um arquivo em regressions/ traz caso e resposta no MESMO objeto — cada
    regressão é um caso que já quebrou uma vez, congelado com a resposta que
    quebrou. Ver evals/regressions/README.md.
    """
    cases = _load_jsonl(DATASET / "cases.jsonl")
    responses = {r["id"]: r for r in _load_jsonl(responses_path)}

    for path in sorted(REGRESSIONS.glob("*.jsonl")):
        for row in _load_jsonl(path):
            cases.append({k: v for k, v in row.items() if k in CASE_FIELDS})
            responses[row["id"]] = row

    return cases, responses


@dataclass(frozen=True)
class Run:
    case: dict
    response: dict
    verdict: Verdict

    @property
    def id(self) -> str:
        return self.case["id"]

    @property
    def expected(self) -> str:
        return self.case["expected"]

    @property
    def decision(self) -> str:
        return self.verdict.decision


def evaluate(responses_path: Path = DATASET / "responses.jsonl") -> list[Run]:
    docs = load_corpus()
    cases, responses = load_dataset(responses_path)
    runs = []
    for case in cases:
        response = responses.get(case["id"])
        if response is None:
            raise AssertionError(
                f"caso {case['id']} sem resposta gravada em responses.jsonl "
                f"(rode `python -m agent.record`)"
            )
        verdict = decide(
            response["answer"],
            response.get("cited_docs", []),
            response.get("retrieved") or case["docs"],
            docs,
        )
        runs.append(Run(case, response, verdict))
    return runs


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def metrics(runs: list[Run]) -> dict[str, float]:
    """Três métricas sobre o AGENTE, nos casos que ele deveria conseguir
    responder, e uma sobre o PORTÃO, no conjunto inteiro.

    Medir grounding sobre o conjunto inteiro não diria nada: 12 casos existem
    justamente para falhar.
    """
    answerable = [r for r in runs if r.expected == ANSWER]

    tp = sum(1 for r in runs if r.expected == ESCALATE and r.decision == ESCALATE)
    fp = sum(1 for r in runs if r.expected == ANSWER and r.decision == ESCALATE)
    fn = sum(1 for r in runs if r.expected == ESCALATE and r.decision == ANSWER)

    return {
        "grounding_rate": _rate(
            sum(1 for r in answerable if r.verdict.checks["grounding"].ok), len(answerable)
        ),
        "citation_validity": _rate(
            sum(1 for r in answerable if r.verdict.checks["citation"].ok), len(answerable)
        ),
        "action_promise_rate": _rate(
            sum(1 for r in answerable if not r.verdict.checks["no_action"].ok), len(answerable)
        ),
        "escalation_precision": _rate(tp, tp + fp),
        "escalation_recall": _rate(tp, tp + fn),
    }
