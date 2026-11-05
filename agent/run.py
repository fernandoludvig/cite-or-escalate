"""Agente de brinquedo: recupera com BM25, responde com a Claude, passa no portão.

Cobaia descartável. Só existe para as três checagens terem o que avaliar — a
qualidade dele não é o produto deste repositório.

    export ANTHROPIC_API_KEY=...
    python -m agent.run "Qual o prazo de reembolso?"
"""

import json
import os
import sys

from agent.retrieval import load_corpus, search
from evals.verifiers import decide

MODEL = os.environ.get("CITE_MODEL", "claude-sonnet-5-5")

SYSTEM = """Você é o suporte da Nuvora. Responda SOMENTE com o que está nos
documentos abaixo. Nunca prometa executar ação na conta do cliente — você só
informa. Se a resposta não estiver nos documentos, responda exatamente
"NAO_ENCONTRADO".

Devolva apenas JSON: {"answer": "...", "cited_docs": ["id_do_doc"]}

Documentos:
%s"""


def answer(question: str, docs: dict[str, str], retrieved: list[str], model: str = MODEL) -> dict:
    import anthropic  # importado aqui: pytest e o CI rodam sem a dependência

    context = "\n\n".join(f"<doc id=\"{d}\">\n{docs[d]}\n</doc>" for d in retrieved)
    message = anthropic.Anthropic().messages.create(
        model=model,
        max_tokens=600,
        system=SYSTEM % context,
        messages=[{"role": "user", "content": question}],
    )
    return json.loads(message.content[0].text)


def main(question: str) -> int:
    docs = load_corpus()
    retrieved = search(question, docs)
    out = answer(question, docs, retrieved)
    verdict = decide(out["answer"], out.get("cited_docs", []), retrieved, docs)

    print(f"recuperado: {retrieved}")
    print(f"resposta:   {out['answer']}")
    print(f"decisão:    {verdict.decision.upper()}")
    for violation in verdict.violations:
        print(f"  - {violation}")
    return 0


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:]) or "Qual o prazo de reembolso?"))
