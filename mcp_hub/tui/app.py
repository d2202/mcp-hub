from textual.app import App

from mcp_hub.tui.add_wizard import AddWizardScreen
from mcp_hub.tui.dashboard import DashboardScreen
from mcp_hub.tui.server_list import ServerListScreen


class McpHubApp(App):
    TITLE = "mcp-hub"

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())

    def on_dashboard_screen_agent_selected(self, message: DashboardScreen.AgentSelected) -> None:
        self.push_screen(ServerListScreen(message.adapter))

    def on_server_list_screen_open_add_wizard(self, message: ServerListScreen.OpenAddWizard) -> None:
        self._pending_adapter = message.adapter
        self.push_screen(AddWizardScreen())

    def on_server_list_screen_remove_requested(self, message: ServerListScreen.RemoveRequested) -> None:
        message.adapter.remove_server(message.server_name)
        self._refresh_current_server_list()

    def on_add_wizard_screen_wizard_done(self, message: AddWizardScreen.WizardDone) -> None:
        self.pop_screen()
        self._refresh_current_server_list()

    def _refresh_current_server_list(self) -> None:
        screen = self.screen
        if isinstance(screen, ServerListScreen):
            screen._refresh_table()
