"""O portão: três checagens determinísticas e uma decisão.

A tese do repositório mora aqui. Se qualquer checagem falha, a resposta não vale
e a saída é escalar para humano — nunca tentar consertar a resposta.
"""

from dataclasses import dataclass

from .citation import check_citation
from .grounding import DEFAULT_MIN_OVERLAP, check_grounding
from .no_action import check_no_action
from .result import Result

__all__ = [
    "check_citation",
    "check_grounding",
    "check_no_action",
    "Result",
    "Verdict",
    "decide",
]

ANSWER = "answer"
ESCALATE = "escalate"


@dataclass(frozen=True)
class Verdict:
    decision: str  # "answer" | "escalate"
    checks: dict[str, Result]

    @property
    def violations(self) -> list[str]:
        return [
            f"[{name}] {v}"
            for name, result in self.checks.items()
            for v in result.violations
        ]


def decide(
    answer: str,
    cited_docs: list[str],
    retrieved_docs: list[str],
    docs: dict[str, str],
    min_overlap: float = DEFAULT_MIN_OVERLAP,
) -> Verdict:
    """Decide se a resposta pode ir ao cliente ou se o caso escala.

    `docs` mapeia id -> texto do documento; a fonte do grounding é o texto dos
    documentos citados (um id citado que não existe no corpus não vira fonte,
    e a checagem de citação já reprova isso).
    """
    source = "\n".join(docs[d] for d in cited_docs if d in docs)
    checks = {
        "citation": check_citation(cited_docs, retrieved_docs),
        "grounding": check_grounding(answer, source, min_overlap),
        "no_action": check_no_action(answer),
    }
    ok = all(r.ok for r in checks.values())
    return Verdict(ANSWER if ok else ESCALATE, checks)
