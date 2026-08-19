from textual.app import ComposeResult
from textual.message import Message
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from mcp_hub.adapters import AgentAdapter
from mcp_hub.i18n import t


class ServerListScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("a", "add", "Add server"),
        ("r", "remove", "Remove selected"),
    ]

    class OpenAddWizard(Message):
        def __init__(self, adapter: AgentAdapter) -> None:
            self.adapter = adapter
            super().__init__()

    class RemoveRequested(Message):
        def __init__(self, adapter: AgentAdapter, server_name: str) -> None:
            self.adapter = adapter
            self.server_name = server_name
            super().__init__()

    def __init__(self, adapter: AgentAdapter) -> None:
        super().__init__()
        self.adapter = adapter

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="server-table")
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = self.adapter.name
        self._refresh_table()

    def _refresh_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(t("col_name"), t("col_command"), t("col_args"), t("col_valid"))
        table.cursor_type = "row"
        for entry in self.adapter.list_servers():
            table.add_row(
                entry.name,
                entry.command,
                " ".join(entry.args),
                t("yes") if entry.valid else f"{t('no')} ({entry.error})",
                key=entry.name,
            )

    def action_add(self) -> None:
        self.post_message(self.OpenAddWizard(self.adapter))

    def action_remove(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is None:
            return
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        self.post_message(self.RemoveRequested(self.adapter, row_key.value))
