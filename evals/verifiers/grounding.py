"""Checagem 1 — toda afirmação e todo número da resposta existe no trecho citado.

Determinístico de propósito: nenhum modelo opina aqui. Dois testes por frase.

1. Números são requisito duro. Um número na resposta que não está na fonte é
   invenção — é o modo de falha que mais dói em suporte (prazo, preço, multa).
2. Afirmação é cobertura de vocabulário: as palavras de conteúdo da frase têm
   que aparecer na fonte, acima de um limiar. Não entende semântica, e isso é
   intencional — o custo do falso positivo (passar invenção) é maior que o do
   falso negativo (escalar à toa), e escalar à toa é o comportamento seguro.
"""

from .result import Result
from .text import content_tokens, number_contexts, numbers, sentences, stems

DEFAULT_MIN_OVERLAP = 0.7


def check_grounding(
    answer: str, source: str, min_overlap: float = DEFAULT_MIN_OVERLAP
) -> Result:
    if not source.strip():
        return Result(False, ["fonte citada vazia"])

    source_stems = stems(source)
    source_numbers = number_contexts(source)
    violations: list[str] = []

    for sentence in sentences(answer):
        content = content_tokens(sentence)
        sentence_stems = {t[:5] for t in content}

        for raw, value in numbers(sentence):
            windows = [w for v, w in source_numbers if v == value]
            if not windows:
                violations.append(f"número não está na fonte: {raw!r} em {sentence!r}")
            elif not any(w & sentence_stems for w in windows):
                violations.append(
                    f"número está na fonte mas ligado a outro assunto: "
                    f"{raw!r} em {sentence!r}"
                )

        if not content:
            continue
        missing = [t for t in content if t[:5] not in source_stems]
        coverage = 1 - len(missing) / len(content)
        if coverage < min_overlap:
            violations.append(
                f"afirmação sem apoio na fonte (cobertura {coverage:.0%}, "
                f"faltou {missing}): {sentence!r}"
            )

    return Result(not violations, violations)
