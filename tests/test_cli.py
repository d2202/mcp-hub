from mcp_hub.cli import main


def test_main_runs_without_error(capsys):
    main([])
    captured = capsys.readouterr()
    assert "mcp-hub" in captured.out
