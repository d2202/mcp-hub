from mcp_hub.adapters import get_adapters


def test_get_adapters_returns_all_three_known_agents():
    adapters = get_adapters()
    names = {a.name for a in adapters}
    assert names == {"claude-code", "codex", "antigravity"}
