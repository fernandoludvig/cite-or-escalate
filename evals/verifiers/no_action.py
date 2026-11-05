"""Checagem 3 — a resposta não promete executar ação.

Um agente de resposta não tem as mãos do sistema. "Já cancelei sua assinatura"
e "vou abrir seu ticket" criam uma expectativa que ninguém vai cumprir, e o
cliente só descobre dias depois. É o modo de falha mais caro em confiança e o
mais fácil de checar sem IA: é vocabulário, não semântica.

Não entram na lista os verbos de escalação (escalar, encaminhar, transferir):
"vou transferir para um atendente" é justamente o comportamento desejado.
"""

import re

from .result import Result
from .text import normalize

# verbos de execução na conta do cliente, no infinitivo
_VERBS = [
    "abrir", "cancelar", "estornar", "reembolsar", "processar", "enviar",
    "agendar", "criar", "emitir", "ajustar", "alterar", "atualizar", "ativar",
    "desativar", "bloquear", "desbloquear", "liberar", "reativar", "suspender",
    # "excluir" fora da lista: "exclui" é 1ª pessoa do passado E 3ª do presente
    # ("o sistema exclui os dados"), e geraria falso positivo. "apagar" cobre.
    "revogar", "restaurar", "apagar", "corrigir", "resolver",
    "registrar", "solicitar", "providenciar", "estender", "renovar",
]

_CONJ = {"ar": ("ando", "ei", "amos"), "er": ("endo", "i", "emos"), "ir": ("indo", "i", "imos")}


def _forms(index: int) -> str:
    out = set()
    for verb in _VERBS:
        stem, ending = verb[:-2], verb[-2:]
        out.add(stem + _CONJ[ending][index])
    return "|".join(sorted(out))


_INFINITIVES = "|".join(sorted(_VERBS))
_GERUNDS = _forms(0)
_DONE = _forms(1) + "|" + _forms(2)

PATTERNS = {
    "promessa futura": re.compile(
        rf"\b(vou|irei|vamos|iremos|ja vou)\b[^.!?]{{0,30}}?\b({_INFINITIVES})\b"
    ),
    "ação em curso": re.compile(
        rf"\b(estou|estamos)\b[^.!?]{{0,25}}?\b({_GERUNDS})\b"
    ),
    "ação concluída": re.compile(rf"\b(ja\s+)?({_DONE})\b"),
    "conclusão passiva": re.compile(
        r"\bja\b[^.!?]{0,25}?\b(foi|foram|esta|estao)\b[^.!?]{0,20}?"
        r"\b(cancelad\w+|estornad\w+|reembolsad\w+|abert\w+|processad\w+"
        r"|emitid\w+|enviad\w+|resolvid\w+|liberad\w+|ativad\w+)\b"
    ),
}


def check_no_action(answer: str) -> Result:
    text = normalize(answer)
    violations = [
        f"{label}: {match.group(0)!r}"
        for label, pattern in PATTERNS.items()
        for match in pattern.finditer(text)
    ]
    return Result(not violations, violations)
