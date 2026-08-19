from textual.app import ComposeResult
from textual.message import Message
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from mcp_hub.adapters import AgentAdapter, get_adapters
from mcp_hub.i18n import t


class DashboardScreen(Screen):
    BINDINGS = [("q", "app.quit", "Quit")]

    class AgentSelected(Message):
        def __init__(self, adapter: AgentAdapter) -> None:
            self.adapter = adapter
            super().__init__()

    def __init__(self) -> None:
        super().__init__()
        self._adapters = get_adapters()

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="agent-table")
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = t("dashboard_title")
        table = self.query_one(DataTable)
        table.add_columns(
            t("col_agent"), t("col_detected"), t("col_servers"), t("col_config_path")
        )
        table.cursor_type = "row"
        for adapter in self._adapters:
            detected = adapter.detect()
            count = len(adapter.list_servers()) if detected else 0
            table.add_row(
                adapter.name,
                t("yes") if detected else t("no"),
                str(count),
                str(adapter.config_path),
                key=adapter.name,
            )

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        adapter = next(a for a in self._adapters if a.name == event.row_key.value)
        self.post_message(self.AgentSelected(adapter))
