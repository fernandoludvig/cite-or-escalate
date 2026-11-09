"""O mesmo dataset, vários modelos, lado a lado.

    python -m evals.compare

Lê evals/dataset/responses.jsonl (o modelo padrão, que o CI usa como portão) e
cada evals/dataset/models/<modelo>.jsonl gravado com CITE_MODEL. As regressões
ficam de fora: são respostas congeladas, iguais para todo modelo, e só diluiriam
a diferença.
"""

from evals.harness import DATASET, evaluate, metrics


def build() -> str:
    paths = [DATASET / "responses.jsonl", *sorted((DATASET / "models").glob("*.jsonl"))]
    columns = {}
    for path in paths:
        runs = [r for r in evaluate(path) if not r.id.startswith("r")]
        columns[runs[0].response["model"]] = (metrics(runs), runs)

    names = list(columns)
    lines = ["| | " + " | ".join(f"`{n}`" for n in names) + " |", "|---" * (len(names) + 1) + "|"]
    for metric in next(iter(columns.values()))[0]:
        lines.append(f"| {metric} | " + " | ".join(f"{columns[n][0][metric]:.1%}" for n in names) + " |")
    lines.append(
        "| decisão ≠ rótulo | "
        + " | ".join(", ".join(r.id for r in columns[n][1] if r.decision != r.expected) or "—" for n in names)
        + " |"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(build())
