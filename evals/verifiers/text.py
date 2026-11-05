"""Normalização de texto compartilhada pelos verificadores. Zero IA aqui."""

import re
import unicodedata

_WORD_RE = re.compile(r"[a-z0-9]+")
_SENT_RE = re.compile(r"(?<=[.!?;:])\s+|\n+")
# número com separador de milhar (ponto) e/ou decimal (vírgula ou ponto), com % opcional
_NUM_RE = re.compile(r"\d+(?:[.,]\d+)*\s*%?")

# stopwords pt-BR: palavras que não carregam afirmação, então não contam no grounding
STOPWORDS = frozenset(
    """
    a as o os um uma uns umas de do da dos das em no na nos nas por pelo pela
    pelos pelas para com sem sobre sob entre ate ao aos e ou mas que se como
    quando onde qual quais quanto quantos quanta quantas nao sim ja nem tambem
    muito mais menos pouco todo toda todos todas cada qualquer outro outra
    outros outras mesmo mesma seu sua seus suas meu minha nosso nossa este esta
    isso aquele aquela ele ela eles elas eu voce lhe me te nos vos ser sou e
    sao foi era esta estao estar tem ter tenho temos ha havia pode podem poder
    deve devem dever vai vao ir fica ficam ficar faz fazem fazer ainda apenas
    somente depois antes durante desde caso entao assim porque pois logo bem
    sr sra ola oi obrigado obrigada por favor conforme segundo dentro fora
    """.split()
)

STEM_LEN = 5


def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize(text: str) -> str:
    return strip_accents(text).lower()


def tokens(text: str) -> list[str]:
    return _WORD_RE.findall(normalize(text))


def stems(text: str) -> set[str]:
    """Prefixos de 5 caracteres: tolera plural e conjugação sem trazer um stemmer."""
    return {t[:STEM_LEN] for t in tokens(text)}


def content_tokens(text: str) -> list[str]:
    return [
        t
        for t in tokens(text)
        if len(t) > 2 and t not in STOPWORDS and not t.isdigit()
    ]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_RE.split(text) if s.strip()]


def numbers(text: str) -> list[tuple[str, float]]:
    """Números do texto como (texto original, valor). Percentual vira o próprio número."""
    out = []
    for raw in _NUM_RE.findall(text):
        value = _to_float(raw)
        if value is not None:
            out.append((raw.strip(), value))
    return out


CONTEXT_CHARS = 60


def number_contexts(text: str) -> list[tuple[float, set[str]]]:
    """Cada número do texto com os stems da vizinhança.

    Existe porque "30" sozinho não prova nada: a fonte pode ter 30 na multa e a
    resposta falar de 30 dias. O número precisa estar perto do assunto.
    """
    norm = normalize(text)
    out = []
    for match in _NUM_RE.finditer(norm):
        value = _to_float(match.group(0))
        if value is None:
            continue
        window = norm[max(0, match.start() - CONTEXT_CHARS) : match.end() + CONTEXT_CHARS]
        out.append((value, stems(window)))
    return out


def _to_float(raw: str) -> float | None:
    s = raw.replace("%", "").replace(" ", "")
    # separador de milhar: ponto seguido de exatamente 3 dígitos
    s = re.sub(r"\.(?=\d{3}\b)", "", s)
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None
