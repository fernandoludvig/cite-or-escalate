"""Agente de brinquedo: recupera com BM25, responde com a Claude, passa no portão.

Cobaia descartável. Só existe para as três checagens terem o que avaliar — a
qualidade dele não é o produto deste repositório.

    export ANTHROPIC_API_KEY=...
    python -m agent.run "Qual o prazo de reembolso?"
"""

import json
import os
import re
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

    # Sem span próprio aqui de propósito: o SDK do anthropic (>=2.6) se
    # auto-instrumenta quando acha o SDK do OTel no ambiente e emite
    # "anthropic.messages.create" com os atributos gen_ai.* completos — request
    # id, tokens de cache e stop_reason inclusos. Um span nosso em volta só
    # repetiria um subconjunto disso.
    context = "\n\n".join(f"<doc id=\"{d}\">\n{docs[d]}\n</doc>" for d in retrieved)
    message = anthropic.Anthropic().messages.create(
        model=model,
        max_tokens=600,
        system=SYSTEM % context,
        messages=[{"role": "user", "content": question}],
    )
    return parse(message.content[0].text)


def parse(raw: str) -> dict:
    """Extrai o JSON da resposta do modelo.

    O modelo às vezes embrulha o JSON em cerca de markdown ou numa frase. Isso
    é problema do agente, não do harness — e um agente que explode no parse
    impede a avaliação de rodar, então aqui tolera as duas formas.
    """
    text = raw.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        # NAO_ENCONTRADO em texto puro é resposta válida: sem citação, o portão
        # já reprova e o caso escala, que é o comportamento certo.
        return {"answer": text, "cited_docs": []}
    return json.loads(match.group(0))


def main(question: str) -> int:
    from otel import span, trace_id

    docs = load_corpus()
    with span("case", **{"cite.question": question}) as case:
        retrieved = search(question, docs)
        out = answer(question, docs, retrieved)
        # O portão ganha span próprio: é o que transforma "este caso falhou" em
        # "aqui está a checagem que reprovou e por quê".
        with span("gate") as gate:
            verdict = decide(out["answer"], out.get("cited_docs", []), retrieved, docs)
            if gate:
                gate.set_attribute("cite.decision", verdict.decision)
                gate.set_attribute("cite.violations", verdict.violations)
        tid = trace_id(case)

    print(f"recuperado: {retrieved}")
    print(f"resposta:   {out['answer']}")
    print(f"decisão:    {verdict.decision.upper()}")
    for violation in verdict.violations:
        print(f"  - {violation}")
    if tid:
        print(f"trace_id:   {tid}")
    return 0


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:]) or "Qual o prazo de reembolso?"))
