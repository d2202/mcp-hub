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

        servers = data.get("mcpServers")
        if not isinstance(servers, dict):
            servers = {}

        entries = []
        for name, cfg in servers.items():
            try:
                command = cfg.get("command") or ""
                args = list(cfg.get("args") or [])
                env = dict(cfg.get("env") or {})
                if not isinstance(command, str):
                    raise TypeError(f"command must be a string, got {type(command).__name__}")
                if not all(isinstance(a, str) for a in args):
                    raise TypeError("args must all be strings")
                if not all(isinstance(v, str) for v in env.values()):
                    raise TypeError("env values must all be strings")
                entries.append(ServerEntry(name=name, command=command, args=args, env=env))
            except (AttributeError, TypeError) as exc:
                entries.append(ServerEntry(
                    name=name, command="", args=[], env={},
                    valid=False, error=str(exc),
                ))
        return entries

    def add_server(self, spec: ServerSpec) -> None:
        data = self._load()
        if not isinstance(data.get("mcpServers"), dict):
            data["mcpServers"] = {}
        data["mcpServers"][spec.name] = {
            "command": spec.command,
            "args": spec.args,
            "env": spec.env,
        }
        self._backup_and_write(json.dumps(data, indent=2) + "\n")

    def remove_server(self, name: str) -> None:
        data = self._load()
        servers = data.get("mcpServers")
        if isinstance(servers, dict):
            servers.pop(name, None)
        self._backup_and_write(json.dumps(data, indent=2) + "\n")

    def _backup_and_write(self, text: str) -> None:
        backup_path = self.config_path.with_suffix(self.config_path.suffix + ".bak")
        shutil.copy2(self.config_path, backup_path)
        self.config_path.write_text(text)
