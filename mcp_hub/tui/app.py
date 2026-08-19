from textual.app import App

from mcp_hub import i18n, settings
from mcp_hub.i18n import t
from mcp_hub.tui.add_wizard import AddWizardScreen
from mcp_hub.tui.dashboard import DashboardScreen
from mcp_hub.tui.help import HelpScreen
from mcp_hub.tui.server_list import ServerListScreen

_TRANSLATABLE_SCREENS = (DashboardScreen, ServerListScreen, AddWizardScreen, HelpScreen)


class McpHubApp(App):
    TITLE = "mcp-hub"
    _BINDING_SPEC = [
        ("l", "toggle_language", "key_language"),
        ("?", "help", "key_help"),
    ]
    BINDINGS = [(k, a, t(i)) for k, a, i in _BINDING_SPEC]

    def on_mount(self) -> None:
        i18n.load_language()
        self._retranslate_all_bindings()

        saved_theme = settings.load().get("theme")
        if saved_theme and saved_theme in self.available_themes:
            self.theme = saved_theme

        self.push_screen(DashboardScreen())

    def watch_theme(self, old_theme: str, new_theme: str) -> None:
        settings.save(theme=new_theme)

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
        # `_merged_bindings` once at construction, so our own keys need a
        # direct refresh here too. Patch only the keys we own (by key,
        # not by wholesale replacement) so Textual's own instance-level
        # binding for ctrl+p (the command palette, added in App.__init__
        # and never present on the class) survives untouched.
        for key, bindings in McpHubApp._merged_bindings.key_to_bindings.items():
            self._bindings.key_to_bindings[key] = list(bindings)

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
