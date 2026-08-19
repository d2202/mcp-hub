from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from mcp_hub.i18n import t


class HelpScreen(Screen):
    _BINDING_SPEC = [("escape", "app.pop_screen", "key_back")]
    BINDINGS = [(k, a, t(i)) for k, a, i in _BINDING_SPEC]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            yield Static(t("help_body"))
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = t("help_title")
