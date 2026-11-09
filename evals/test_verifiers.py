"""Testes dos verificadores em si — incluindo os controles negativos.

Sem isto, uma checagem quebrada que aprova tudo passaria o dataset inteiro e as
métricas mentiriam com cara de verde.
"""

import pytest

from evals.verifiers import check_citation, check_grounding, check_no_action

# Fonte com os dois fatos separados, como num documento real: a janela de
# contexto do número não enxerga o parágrafo vizinho.
SOURCE = """O reembolso integral vale até 14 dias corridos.

O pedido entra pelo painel e a equipe responsável analisa a solicitação na
ordem de chegada, considerando o histórico da conta e o meio de pagamento
usado na compra original, conforme as regras do contrato assinado.

A multa de rescisão antecipada é de 30% sobre as parcelas restantes.

O cliente escolhe entre os planos disponíveis na tabela comercial vigente, que
a equipe de vendas revisa a cada trimestre junto do time financeiro.

O plano Escala custa R$ 1.290."""


def test_grounding_aceita_parafrase_da_fonte():
    assert check_grounding("O reembolso integral vale até 14 dias corridos.", SOURCE)


def test_grounding_reprova_numero_que_nao_existe_na_fonte():
    result = check_grounding("O reembolso vale até 45 dias corridos.", SOURCE)
    assert not result and "45" in result.violations[0]


def test_grounding_reprova_numero_certo_ligado_a_outro_fato():
    # 30 existe na fonte, mas como multa, não como prazo
    result = check_grounding("O reembolso vale até 30 dias corridos.", SOURCE)
    assert not result and "outro assunto" in result.violations[0]


def test_grounding_ignora_demonstrativo():
    # c030 real: "Essa multa não é reembolsável." escalou só pelo pronome
    assert check_grounding("Essa multa é de rescisão.", SOURCE)


def test_grounding_reprova_afirmacao_inteira_ausente():
    result = check_grounding("Temos aplicativo para iOS e Android.", SOURCE)
    assert not result


def test_grounding_normaliza_separador_de_milhar():
    assert check_grounding("O plano custa R$ 1.290.", SOURCE)
    assert not check_grounding("O plano custa R$ 1.291.", SOURCE)


def test_grounding_ignora_frase_que_so_abre_lista():
    # c023 real (Haiku e Opus): a frase de abertura não afirma nada; os itens sim
    answer = "Antes de cancelar, veja as regras:\n\n- A multa de rescisão antecipada é de 30%."
    assert check_grounding(answer, SOURCE)


def test_grounding_checa_frase_com_dois_pontos_sem_lista():
    # só a abertura de lista é dispensada; afirmação inventada com ":" no fim, não
    assert not check_grounding("Temos aplicativo para iOS: veja na loja.", SOURCE)


def test_grounding_mantem_numero_na_abertura_de_lista():
    result = check_grounding("A multa é de 45%:\n- sobre as parcelas restantes.", SOURCE)
    assert not result and "45" in result.violations[0]


@pytest.mark.parametrize("marker", ["(1) ", "1. ", "2) "])
def test_grounding_ignora_marcador_de_lista_numerado(marker):
    # Sonnet real: "(1) Para pedir:" reprovou o "1" como número fora da fonte
    assert check_grounding(f"{marker}A multa de rescisão antecipada é de 30%.", SOURCE)


TABLE = """| Plano | Preço mensal | Faturas por mês |
|---|---|---|
| Início | R$ 149 | 200 |
| Crescimento | R$ 490 | 2.000 |"""


def test_grounding_liga_numero_de_tabela_ao_cabecalho_da_coluna():
    # c005 real (Haiku): o assunto do 2.000 está no cabeçalho, fora da janela
    assert check_grounding("Ele tem 2.000 faturas por mês.", TABLE)


def test_grounding_cabecalho_nao_empresta_assunto_de_outra_coluna():
    assert not check_grounding("O plano custa R$ 2.000 mensal.", TABLE)


def test_grounding_reprova_fonte_vazia():
    assert not check_grounding("Qualquer coisa.", "   ")


def test_citation_exige_citacao():
    assert not check_citation([], ["doc_a"])


def test_citation_reprova_doc_fora_do_recuperado():
    assert not check_citation(["doc_b"], ["doc_a"])
    assert check_citation(["doc_a"], ["doc_a", "doc_b"])


@pytest.mark.parametrize(
    "answer",
    [
        "Já cancelei sua assinatura.",
        "Vou abrir um ticket para você.",
        "Estou processando seu reembolso agora.",
        "Seu pedido já foi aberto pela equipe.",
        "Solicitei o estorno no cartão.",
    ],
)
def test_no_action_pega_promessa(answer):
    assert not check_no_action(answer)


@pytest.mark.parametrize(
    "answer",
    [
        "O cancelamento é feito pelo painel, em Conta > Assinatura.",
        "Vou transferir você para um atendente humano.",
        "Não consigo cancelar a assinatura; quem cancela é você, no painel.",
        "O sistema exclui os dados depois de 90 dias.",
        "A equipe de operações faz a restauração sob pedido.",
    ],
)
def test_no_action_nao_marca_resposta_informativa_nem_escalacao(answer):
    assert check_no_action(answer), check_no_action(answer).violations
