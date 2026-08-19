import shutil
from pathlib import Path

import tomlkit
from tomlkit.exceptions import TOMLKitError

from mcp_hub.models import ServerEntry, ServerSpec


class CodexAdapter:
    name = "codex"

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or (Path.home() / ".codex" / "config.toml")

    def detect(self) -> bool:
        return self.config_path.exists()

    def _load(self):
        return tomlkit.parse(self.config_path.read_text())

    def list_servers(self) -> list[ServerEntry]:
        try:
            doc = self._load()
        except (OSError, TOMLKitError) as exc:
            return [ServerEntry(
                name="<config>", command="", args=[], env={},
                valid=False, error=str(exc),
            )]

        entries = []
        for name, cfg in doc.get("mcp_servers", {}).items():
            entries.append(ServerEntry(
                name=name,
                command=cfg.get("command", ""),
                args=list(cfg.get("args", [])),
                env=dict(cfg.get("env", {})),
            ))
        return entries

    def add_server(self, spec: ServerSpec) -> None:
        doc = self._load()
        if "mcp_servers" not in doc:
            doc["mcp_servers"] = tomlkit.table(is_super_table=True)

        table = tomlkit.table()
        table["command"] = spec.command
        table["args"] = spec.args
        if spec.env:
            table["env"] = spec.env

        doc["mcp_servers"][spec.name] = table
        self._backup_and_write(tomlkit.dumps(doc))

    def remove_server(self, name: str) -> None:
        doc = self._load()
        servers = doc.get("mcp_servers")
        if servers is not None and name in servers:
            del servers[name]
        self._backup_and_write(tomlkit.dumps(doc))

    def _backup_and_write(self, text: str) -> None:
        backup_path = self.config_path.with_suffix(self.config_path.suffix + ".bak")
        shutil.copy2(self.config_path, backup_path)
        self.config_path.write_text(text)
