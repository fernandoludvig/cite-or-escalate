"""O parse do agente é o único ponto dele que, quebrado, impede a avaliação de
rodar — então tem teste. O resto do agente é descartável."""

import pytest

from agent.run import parse

PAYLOAD = '{"answer": "14 dias corridos.", "cited_docs": ["doc_politica_reembolso"]}'


@pytest.mark.parametrize(
    "raw",
    [
        PAYLOAD,
        f"```json\n{PAYLOAD}\n```",
        f"Claro! Aqui está:\n\n{PAYLOAD}\n\nEspero ter ajudado.",
    ],
)
def test_parse_aceita_json_embrulhado(raw):
    assert parse(raw)["cited_docs"] == ["doc_politica_reembolso"]


def test_parse_texto_puro_vira_resposta_sem_citacao():
    out = parse("NAO_ENCONTRADO")
    assert out == {"answer": "NAO_ENCONTRADO", "cited_docs": []}
