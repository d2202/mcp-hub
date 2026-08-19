import json

from mcp_hub.adapters.antigravity import AntigravityAdapter
from mcp_hub.models import ServerSpec


def test_default_config_path_is_gemini_mcp_config():
    adapter = AntigravityAdapter()
    assert adapter.config_path.name == "mcp_config.json"
    assert adapter.name == "antigravity"


def test_add_and_list_server(tmp_path):
    path = tmp_path / "mcp_config.json"
    path.write_text(json.dumps({"mcpServers": {}}))

    adapter = AntigravityAdapter(config_path=path)
    adapter.add_server(ServerSpec(name="fs", command="npx", args=["-y", "fs"], env={}))

    entries = adapter.list_servers()
    assert entries[0].name == "fs"
