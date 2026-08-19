from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, SelectionList, Static

from mcp_hub.adapters import get_adapters
from mcp_hub.catalog import load_catalog
from mcp_hub.i18n import t
from mcp_hub.models import ServerSpec


class AddWizardScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cancel")]

    class WizardDone(Message):
        pass

    def __init__(self) -> None:
        super().__init__()
        self._catalog = load_catalog()
        self._adapters = [a for a in get_adapters() if a.detect()]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(t("wizard_catalog_prompt"))
            yield SelectionList[str](
                *[(spec.name, spec.name) for spec in self._catalog],
                id="catalog-pick",
            )
            yield Label(t("label_name"))
            yield Input(id="name-input")
            yield Label(t("label_command"))
            yield Input(id="command-input")
            yield Label(t("label_args"))
            yield Input(id="args-input")
            yield Static(t("wizard_targets_prompt"))
            yield SelectionList[str](
                *[(a.name, a.name, True) for a in self._adapters],
                id="agent-pick",
            )
            yield Button(t("btn_add"), id="submit", variant="primary")
        yield Footer()

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        if event.selection_list.id != "catalog-pick":
            return
        selected = event.selection_list.selected
        if not selected:
            return
        spec = next(s for s in self._catalog if s.name == selected[-1])
        self.query_one("#name-input", Input).value = spec.name
        self.query_one("#command-input", Input).value = spec.command
        self.query_one("#args-input", Input).value = " ".join(spec.args)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "submit":
            return

        name = self.query_one("#name-input", Input).value.strip()
        command = self.query_one("#command-input", Input).value.strip()
        args = self.query_one("#args-input", Input).value.split()
        if not name or not command:
            return

        spec = ServerSpec(name=name, command=command, args=args, env={})
        targets = self.query_one("#agent-pick", SelectionList).selected
        for adapter in self._adapters:
            if adapter.name in targets:
                adapter.add_server(spec)

        self.post_message(self.WizardDone())
