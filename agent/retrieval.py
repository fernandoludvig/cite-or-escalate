"""Recuperação BM25 em memória sobre o corpus de markdown.

Oito documentos não justificam banco vetorial nem dependência de ranking; BM25
em ~40 linhas resolve e mantém o repositório clonável sem setup.
"""

import math
from collections import Counter
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"

K1 = 1.5
B = 0.75


def load_corpus(corpus_dir: Path = CORPUS_DIR) -> dict[str, str]:
    """id do documento (nome do arquivo sem extensão) -> texto."""
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(corpus_dir.glob("*.md"))}


def search(query: str, docs: dict[str, str], top_k: int = 3) -> list[str]:
    from otel import span

    with span("retrieval") as active:
        result = _bm25(query, docs, top_k)
        if active:
            active.set_attribute("cite.retrieved", result)
        return result


def _bm25(query: str, docs: dict[str, str], top_k: int) -> list[str]:
    from evals.verifiers.text import tokens  # mesma normalização dos verificadores

    doc_tokens = {doc_id: tokens(text) for doc_id, text in docs.items()}
    n = len(doc_tokens)
    avgdl = sum(len(t) for t in doc_tokens.values()) / n
    df = Counter(term for toks in doc_tokens.values() for term in set(toks))

    scores: dict[str, float] = {}
    for doc_id, toks in doc_tokens.items():
        tf = Counter(toks)
        dl = len(toks)
        score = 0.0
        for term in tokens(query):
            if term not in df:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            freq = tf[term]
            score += idf * freq * (K1 + 1) / (freq + K1 * (1 - B + B * dl / avgdl))
        scores[doc_id] = score

    ranked = sorted(scores, key=lambda d: scores[d], reverse=True)
    return [d for d in ranked if scores[d] > 0][:top_k]
