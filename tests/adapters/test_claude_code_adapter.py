import json

from mcp_hub.adapters.claude_code import ClaudeCodeAdapter
from mcp_hub.models import ServerSpec


def test_default_config_path_is_home_claude_json():
    adapter = ClaudeCodeAdapter()
    assert adapter.config_path.name == ".claude.json"
    assert adapter.name == "claude-code"


def test_add_and_list_server(tmp_path):
    path = tmp_path / ".claude.json"
    path.write_text(json.dumps({"mcpServers": {}}))

    adapter = ClaudeCodeAdapter(config_path=path)
    adapter.add_server(ServerSpec(name="fs", command="npx", args=["-y", "fs"], env={}))

    entries = adapter.list_servers()
    assert entries[0].name == "fs"
