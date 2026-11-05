# Regressões

Todo caso que já quebrou uma vez mora aqui, para que o mesmo erro não volte.

Um arquivo `.jsonl` por incidente. Cada linha junta o caso **e** a resposta que
quebrou, no mesmo objeto — a resposta fica congelada, então a regressão não
depende de rodar o modelo de novo:

```json
{"id": "r001", "question": "...", "docs": ["doc_x"], "expected": "escalate",
 "expected_citation": null, "note": "o que quebrou e quando",
 "answer": "a resposta que passou indevidamente", "cited_docs": ["doc_x"],
 "retrieved": ["doc_x", "doc_y"]}
```

O `pytest` recolhe esta pasta junto do dataset principal, e as regressões entram
nas métricas como qualquer outro caso. Use prefixo `r` no id para não colidir
com os casos `c###`.
