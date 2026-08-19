from textual.app import App

from mcp_hub import i18n
from mcp_hub.i18n import t
from mcp_hub.tui.add_wizard import AddWizardScreen
from mcp_hub.tui.dashboard import DashboardScreen
from mcp_hub.tui.help import HelpScreen
from mcp_hub.tui.server_list import ServerListScreen

_TRANSLATABLE_SCREENS = (DashboardScreen, ServerListScreen, AddWizardScreen, HelpScreen)


class McpHubApp(App):
    TITLE = "mcp-hub"
    ENABLE_COMMAND_PALETTE = False
    _BINDING_SPEC = [
        ("l", "toggle_language", "key_language"),
        ("?", "help", "key_help"),
    ]
    BINDINGS = [(k, a, t(i)) for k, a, i in _BINDING_SPEC]

    def on_mount(self) -> None:
        i18n.load_language()
        self._retranslate_all_bindings()
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

    def action_toggle_language(self) -> None:
        i18n.toggle_language()
        self._retranslate_all_bindings()
        self._rebuild_current_screen()

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    def _retranslate_all_bindings(self) -> None:
        for cls in (McpHubApp, *_TRANSLATABLE_SCREENS):
            i18n.retranslate_bindings(cls)
        # McpHubApp is a long-lived singleton (unlike screens, which get
        # recreated on toggle): its own `_bindings` was copied from
        # `_merged_bindings` once at construction, so it needs a direct
        # refresh here too.
        self._bindings = McpHubApp._merged_bindings.copy()

    def _rebuild_current_screen(self) -> None:
        screen = self.screen
        if isinstance(screen, ServerListScreen):
            self.switch_screen(ServerListScreen(screen.adapter))
        elif isinstance(screen, _TRANSLATABLE_SCREENS):
            self.switch_screen(type(screen)())

    def _refresh_current_server_list(self) -> None:
        screen = self.screen
        if isinstance(screen, ServerListScreen):
            screen._refresh_table()
