"""Checagem 2 — a citação pertence ao conjunto efetivamente recuperado.

Citar documento que o retrieval não trouxe é o modo de falha silencioso: a
resposta parece fundamentada e passa por uma revisão humana rápida. Aqui é
comparação de conjuntos, nada mais. Resposta sem citação nenhuma também falha —
não existe afirmação válida sem fonte.
"""

from .result import Result


def check_citation(cited_docs: list[str], retrieved_docs: list[str]) -> Result:
    if not cited_docs:
        return Result(False, ["resposta não citou nenhum documento"])

    retrieved = set(retrieved_docs)
    invented = [d for d in cited_docs if d not in retrieved]
    if invented:
        return Result(
            False,
            [f"citou documento fora do conjunto recuperado: {d}" for d in invented],
        )
    return Result(True)
