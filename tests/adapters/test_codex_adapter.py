from mcp_hub.adapters.codex import CodexAdapter
from mcp_hub.models import ServerSpec

EXISTING_TOML = """
model = "gpt-5"

[mcp_servers.existing]
command = "foo"
args = []
"""


def test_default_config_path_is_codex_config_toml():
    adapter = CodexAdapter()
    assert adapter.config_path.parts[-2:] == (".codex", "config.toml")
    assert adapter.name == "codex"


def test_list_servers_reads_existing_table(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text(EXISTING_TOML)

    entries = CodexAdapter(config_path=path).list_servers()
    assert len(entries) == 1
    assert entries[0].name == "existing"
    assert entries[0].command == "foo"


def test_add_server_preserves_unrelated_keys_and_backs_up(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text(EXISTING_TOML)

    adapter = CodexAdapter(config_path=path)
    adapter.add_server(ServerSpec(name="new", command="uvx", args=["pkg"], env={"K": "v"}))

    text = path.read_text()
    assert 'model = "gpt-5"' in text
    assert "[mcp_servers.new]" in text
    assert "[mcp_servers.existing]" in text

    backup_path = path.with_suffix(path.suffix + ".bak")
    assert backup_path.exists()
    assert "mcp_servers.new" not in backup_path.read_text()


def test_remove_server_deletes_table(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text(EXISTING_TOML)

    adapter = CodexAdapter(config_path=path)
    adapter.remove_server("existing")

    entries = adapter.list_servers()
    assert entries == []


def test_list_servers_flags_malformed_toml(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("not = [valid toml")

    entries = CodexAdapter(config_path=path).list_servers()
    assert len(entries) == 1
    assert entries[0].valid is False
