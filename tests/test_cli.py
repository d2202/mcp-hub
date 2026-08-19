def test_main_is_callable():
    from mcp_hub.cli import main

    assert callable(main)
