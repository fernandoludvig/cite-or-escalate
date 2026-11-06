"""O parse do agente é o único ponto dele que, quebrado, impede a avaliação de
rodar — então tem teste. O resto do agente é descartável."""

from types import SimpleNamespace

import pytest

from agent.run import parse, text_of


def block(type_: str, text: str = ""):
    return SimpleNamespace(type=type_, text=text)

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


def test_text_of_ignora_bloco_de_thinking():
    """Regressão: content[0] era um ThinkingBlock e a rodada toda morria nele."""
    message = SimpleNamespace(
        content=[block("thinking", ""), block("text", PAYLOAD)]
    )
    assert text_of(message) == PAYLOAD


def test_text_of_sem_bloco_de_texto_devolve_vazio():
    """Vazio vira resposta sem citação, que o portão reprova — escalar é o
    comportamento certo quando não há o que avaliar."""
    assert text_of(SimpleNamespace(content=[block("thinking")])) == ""
