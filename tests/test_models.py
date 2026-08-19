from mcp_hub.models import ServerSpec, ServerEntry


def test_server_spec_defaults():
    spec = ServerSpec(name="fs", command="npx")
    assert spec.args == []
    assert spec.env == {}


def test_server_entry_valid_by_default():
    entry = ServerEntry(name="fs", command="npx", args=["-y", "pkg"], env={})
    assert entry.valid is True
    assert entry.error is None


def test_server_entry_can_mark_invalid():
    entry = ServerEntry(
        name="<config>", command="", args=[], env={},
        valid=False, error="bad json",
    )
    assert entry.valid is False
    assert entry.error == "bad json"
