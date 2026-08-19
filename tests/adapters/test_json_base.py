import json

import pytest

from mcp_hub.adapters._json_base import JsonMcpServersAdapter
from mcp_hub.models import ServerSpec


class DummyAdapter(JsonMcpServersAdapter):
    name = "dummy"

    def __init__(self, config_path):
        self.config_path = config_path


@pytest.fixture
def config_path(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({
        "mcpServers": {
            "existing": {"command": "foo", "args": [], "env": {}}
        },
        "otherKey": "untouched",
    }))
    return path


def test_detect_true_when_file_exists(config_path):
    assert DummyAdapter(config_path).detect() is True


def test_detect_false_when_file_missing(tmp_path):
    assert DummyAdapter(tmp_path / "missing.json").detect() is False


def test_list_servers_returns_existing_entry(config_path):
    entries = DummyAdapter(config_path).list_servers()
    assert len(entries) == 1
    assert entries[0].name == "existing"
    assert entries[0].command == "foo"
    assert entries[0].valid is True


def test_list_servers_flags_malformed_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not valid json")
    entries = DummyAdapter(path).list_servers()
    assert len(entries) == 1
    assert entries[0].valid is False
    assert entries[0].error is not None


def test_add_server_writes_new_entry_and_backup(config_path):
    adapter = DummyAdapter(config_path)
    adapter.add_server(ServerSpec(name="new", command="npx", args=["-y", "pkg"], env={"KEY": "val"}))

    data = json.loads(config_path.read_text())
    assert data["mcpServers"]["new"]["command"] == "npx"
    assert data["mcpServers"]["existing"]["command"] == "foo"
    assert data["otherKey"] == "untouched"

    backup_path = config_path.with_suffix(config_path.suffix + ".bak")
    assert backup_path.exists()
    backup_data = json.loads(backup_path.read_text())
    assert "new" not in backup_data["mcpServers"]


def test_remove_server_deletes_entry_and_backs_up(config_path):
    adapter = DummyAdapter(config_path)
    adapter.remove_server("existing")

    data = json.loads(config_path.read_text())
    assert "existing" not in data["mcpServers"]

    backup_path = config_path.with_suffix(config_path.suffix + ".bak")
    assert backup_path.exists()
