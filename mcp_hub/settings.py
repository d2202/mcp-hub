import json
from pathlib import Path

SETTINGS_PATH = Path.home() / ".config" / "mcp-hub" / "settings.json"


def load() -> dict:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def save(**updates: str) -> None:
    data = load()
    data.update(updates)
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(data))
