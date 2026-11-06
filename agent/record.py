"""Regrava evals/dataset/responses.jsonl rodando o agente nos casos do dataset.

As respostas gravadas são o que o pytest avalia, então o CI roda sem chave de
API e sem custo. Rode isto quando quiser medir um modelo novo:

    CITE_MODEL=claude-opus-5 python -m agent.record

Com um número, grava só os N primeiros casos em responses.partial.jsonl — é o
jeito barato de confirmar que a API e o parse funcionam antes de pagar 32
chamadas:

    python -m agent.record 1
"""

import json
import sys
from pathlib import Path

from agent.retrieval import load_corpus, search
from agent.run import MODEL, answer
from otel import span, trace_id

DATASET = Path(__file__).resolve().parent.parent / "evals" / "dataset"


def main(limit: int = 0) -> None:
    docs = load_corpus()
    cases = [json.loads(line) for line in (DATASET / "cases.jsonl").read_text().splitlines() if line.strip()]
    if limit:
        cases = cases[:limit]

    # Grava só no fim: abrir o arquivo em "w" antes da primeira chamada apaga o
    # dataset gravado se a chamada falhar, e aí o CI perde a referência.
    records = []
    for case in cases:
        with span("case", **{"cite.case_id": case["id"]}) as active:
            retrieved = search(case["question"], docs)
            out = answer(case["question"], docs, retrieved)
            tid = trace_id(active)
        records.append(
            {
                "id": case["id"],
                "model": MODEL,
                "answer": out["answer"],
                "cited_docs": out.get("cited_docs", []),
                "retrieved": retrieved,
                # Sem SDK instalado isto é string vazia: o campo existe sempre,
                # para o relatório não precisar de dois formatos de registro.
                "trace_id": tid,
            }
        )
        # Resposta cortada ainda vira registro (o portão escala), mas não pode
        # passar em silêncio como no c030 da primeira rodada.
        status = "TRUNCADA (max_tokens)" if out.get("stop_reason") == "max_tokens" else "ok"
        print(f"{case['id']}: {status}{' · ' + tid if tid else ''}")

    target = DATASET / ("responses.jsonl" if not limit else "responses.partial.jsonl")
    target.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8"
    )
    print(f"\n{len(records)} respostas em {target}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
