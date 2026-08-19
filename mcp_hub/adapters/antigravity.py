from pathlib import Path

from mcp_hub.adapters._json_base import JsonMcpServersAdapter


class AntigravityAdapter(JsonMcpServersAdapter):
    name = "antigravity"

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or (
            Path.home() / ".gemini" / "config" / "mcp_config.json"
        )
