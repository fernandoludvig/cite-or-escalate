"""Regrava evals/dataset/responses.jsonl rodando o agente nos casos do dataset.

As respostas gravadas são o que o pytest avalia, então o CI roda sem chave de
API e sem custo. Rode isto quando quiser medir um modelo novo:

    CITE_MODEL=claude-opus-5 python -m agent.record
"""

import json
from pathlib import Path

from agent.retrieval import load_corpus, search
from agent.run import MODEL, answer

DATASET = Path(__file__).resolve().parent.parent / "evals" / "dataset"


def main() -> None:
    docs = load_corpus()
    cases = [json.loads(line) for line in (DATASET / "cases.jsonl").read_text().splitlines() if line.strip()]

    with (DATASET / "responses.jsonl").open("w", encoding="utf-8") as fh:
        for case in cases:
            retrieved = search(case["question"], docs)
            out = answer(case["question"], docs, retrieved)
            record = {
                "id": case["id"],
                "model": MODEL,
                "answer": out["answer"],
                "cited_docs": out.get("cited_docs", []),
                "retrieved": retrieved,
            }
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"{case['id']}: ok")


if __name__ == "__main__":
    main()
