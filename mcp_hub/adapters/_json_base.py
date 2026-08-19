import json
import shutil
from pathlib import Path

from mcp_hub.models import ServerEntry, ServerSpec


class JsonMcpServersAdapter:
    name: str = ""
    config_path: Path

    def detect(self) -> bool:
        return self.config_path.exists()

    def _load(self) -> dict:
        text = self.config_path.read_text().strip()
        return json.loads(text) if text else {}

    def list_servers(self) -> list[ServerEntry]:
        try:
            data = self._load()
        except (OSError, json.JSONDecodeError) as exc:
            return [ServerEntry(
                name="<config>", command="", args=[], env={},
                valid=False, error=str(exc),
            )]

        entries = []
        for name, cfg in data.get("mcpServers", {}).items():
            try:
                entries.append(ServerEntry(
                    name=name,
                    command=cfg.get("command") or "",
                    args=list(cfg.get("args") or []),
                    env=dict(cfg.get("env") or {}),
                ))
            except (AttributeError, TypeError) as exc:
                entries.append(ServerEntry(
                    name=name, command="", args=[], env={},
                    valid=False, error=str(exc),
                ))
        return entries

    def add_server(self, spec: ServerSpec) -> None:
        data = self._load()
        data.setdefault("mcpServers", {})[spec.name] = {
            "command": spec.command,
            "args": spec.args,
            "env": spec.env,
        }
        self._backup_and_write(json.dumps(data, indent=2) + "\n")

    def remove_server(self, name: str) -> None:
        data = self._load()
        data.get("mcpServers", {}).pop(name, None)
        self._backup_and_write(json.dumps(data, indent=2) + "\n")

    def _backup_and_write(self, text: str) -> None:
        backup_path = self.config_path.with_suffix(self.config_path.suffix + ".bak")
        shutil.copy2(self.config_path, backup_path)
        self.config_path.write_text(text)
