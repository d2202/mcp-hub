from dataclasses import dataclass, field


@dataclass
class ServerSpec:
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class ServerEntry:
    name: str
    command: str
    args: list[str]
    env: dict[str, str]
    valid: bool = True
    error: str | None = None
