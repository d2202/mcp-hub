from pathlib import Path

import yaml

from mcp_hub.models import ServerSpec

CATALOG_PATH = Path(__file__).parent / "catalog.yaml"


def load_catalog(path: Path = CATALOG_PATH) -> list[ServerSpec]:
    data = yaml.safe_load(path.read_text()) or []
    return [
        ServerSpec(
            name=item["name"],
            command=item["command"],
            args=list(item.get("args", [])),
            env={key: "" for key in item.get("env", [])},
        )
        for item in data
    ]
