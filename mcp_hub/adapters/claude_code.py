from pathlib import Path

from mcp_hub.adapters._json_base import JsonMcpServersAdapter


class ClaudeCodeAdapter(JsonMcpServersAdapter):
    name = "claude-code"

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or (Path.home() / ".claude.json")
