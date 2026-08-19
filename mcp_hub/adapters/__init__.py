from pathlib import Path
from typing import Protocol

from mcp_hub.models import ServerEntry, ServerSpec


class AgentAdapter(Protocol):
    name: str
    config_path: Path

    def detect(self) -> bool: ...
    def list_servers(self) -> list[ServerEntry]: ...
    def add_server(self, spec: ServerSpec) -> None: ...
    def remove_server(self, name: str) -> None: ...


def get_adapters() -> list[AgentAdapter]:
    from mcp_hub.adapters.antigravity import AntigravityAdapter
    from mcp_hub.adapters.claude_code import ClaudeCodeAdapter
    from mcp_hub.adapters.codex import CodexAdapter

    return [ClaudeCodeAdapter(), CodexAdapter(), AntigravityAdapter()]
