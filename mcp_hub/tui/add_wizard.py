import shlex

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, SelectionList, Static

from mcp_hub.adapters import AgentAdapter, get_adapters
from mcp_hub.catalog import load_catalog
from mcp_hub.i18n import t
from mcp_hub.models import ServerEntry, ServerSpec
from mcp_hub.tui.confirm import ConfirmScreen


def parse_args_input(text: str) -> list[str]:
    """Parse a shell-style, space-separated arg list. Quote an arg
    ("--path" "C:\\Program Files") to keep spaces inside it together.
    """
    return shlex.split(text)


def parse_env_input(text: str) -> dict[str, str]:
    """Parse a shell-style "KEY=value KEY2=value2" string into a dict.
    Quote a value to keep spaces inside it together. Tokens without "="
    are ignored; only the first "=" splits key from value, so values may
    contain "=" themselves (e.g. URLs).
    """
    env: dict[str, str] = {}
    for token in shlex.split(text):
        if "=" not in token:
            continue
        key, _, value = token.partition("=")
        env[key] = value
    return env


class AddWizardScreen(Screen):
    _BINDING_SPEC = [("escape", "app.pop_screen", "key_cancel")]
    BINDINGS = [(k, a, t(i)) for k, a, i in _BINDING_SPEC]

    class WizardDone(Message):
        pass

    def __init__(
        self,
        adapter: AgentAdapter | None = None,
        edit_entry: ServerEntry | None = None,
    ) -> None:
        if edit_entry is not None and adapter is None:
            raise ValueError("edit_entry requires an adapter")
        super().__init__()
        self._catalog = load_catalog()
        self._adapters = [a for a in get_adapters() if a.detect()]
        self._edit_adapter = adapter
        self._edit_entry = edit_entry

    def compose(self) -> ComposeResult:
        yield Header()
        editing = self._edit_entry is not None
        with Vertical():
            if not editing:
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
            yield Label(t("label_env"))
            yield Input(id="env-input")
            if not editing:
                yield Static(t("wizard_targets_prompt"))
                yield SelectionList[str](
                    *[(a.name, a.name, True) for a in self._adapters],
                    id="agent-pick",
                )
            yield Button(t("btn_save") if editing else t("btn_add"), id="submit", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        entry = self._edit_entry
        if entry is None:
            return
        self.query_one("#name-input", Input).value = entry.name
        self.query_one("#command-input", Input).value = entry.command
        self.query_one("#args-input", Input).value = shlex.join(entry.args)
        self.query_one("#env-input", Input).value = shlex.join(f"{k}={v}" for k, v in entry.env.items())

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        if event.selection_list.id != "catalog-pick":
            return
        selected = event.selection_list.selected
        if not selected:
            return
        spec = next(s for s in self._catalog if s.name == selected[-1])
        self.query_one("#name-input", Input).value = spec.name
        self.query_one("#command-input", Input).value = spec.command
        self.query_one("#args-input", Input).value = shlex.join(spec.args)
        self.query_one("#env-input", Input).value = shlex.join(f"{k}=" for k in spec.env)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "submit":
            return

        name = self.query_one("#name-input", Input).value.strip()
        command = self.query_one("#command-input", Input).value.strip()
        args = parse_args_input(self.query_one("#args-input", Input).value)
        env = parse_env_input(self.query_one("#env-input", Input).value)
        if not name or not command:
            return

        spec = ServerSpec(name=name, command=command, args=args, env=env)

        if self._edit_entry is not None:
            renamed = name != self._edit_entry.name
            collides = renamed and any(
                e.name == name for e in self._edit_adapter.list_servers()
            )
            if collides:
                def handle_confirm(confirmed: bool | None) -> None:
                    if confirmed:
                        self._save_edit(spec, renamed=True)

                self.app.push_screen(
                    ConfirmScreen(t("confirm_overwrite").format(name=name)),
                    handle_confirm,
                )
            else:
                self._save_edit(spec, renamed=renamed)
        else:
            targets = self.query_one("#agent-pick", SelectionList).selected
            for adapter in self._adapters:
                if adapter.name in targets:
                    adapter.add_server(spec)
            self.post_message(self.WizardDone())

    def _save_edit(self, spec: ServerSpec, renamed: bool) -> None:
        if renamed:
            self._edit_adapter.remove_server(self._edit_entry.name)
        self._edit_adapter.add_server(spec)
        self.post_message(self.WizardDone())
