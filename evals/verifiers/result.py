from dataclasses import dataclass, field


@dataclass(frozen=True)
class Result:
    """Saída de um verificador. `violations` é o que vai no relatório do caso falho."""

    ok: bool
    violations: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.ok
