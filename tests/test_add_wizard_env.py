from mcp_hub.tui.add_wizard import parse_env_input


def test_parse_env_input_empty_string():
    assert parse_env_input("") == {}


def test_parse_env_input_single_pair():
    assert parse_env_input("KEY=value") == {"KEY": "value"}


def test_parse_env_input_multiple_pairs():
    assert parse_env_input("KEY=value TOKEN=abc123") == {
        "KEY": "value",
        "TOKEN": "abc123",
    }


def test_parse_env_input_allows_empty_value():
    assert parse_env_input("TOKEN=") == {"TOKEN": ""}


def test_parse_env_input_ignores_tokens_without_equals():
    assert parse_env_input("KEY=value garbage") == {"KEY": "value"}


def test_parse_env_input_value_can_contain_equals():
    assert parse_env_input("URL=https://x.com?a=b") == {"URL": "https://x.com?a=b"}
