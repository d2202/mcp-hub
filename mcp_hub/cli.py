def main(argv: list[str] | None = None) -> None:
    from mcp_hub.tui.app import McpHubApp

    McpHubApp().run()
