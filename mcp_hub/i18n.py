import json
from pathlib import Path

SETTINGS_PATH = Path.home() / ".config" / "mcp-hub" / "settings.json"

STRINGS: dict[str, dict[str, str]] = {
    "key_quit": {"en": "Quit", "ru": "Выход"},
    "key_back": {"en": "Back", "ru": "Назад"},
    "key_add_server": {"en": "Add server", "ru": "Добавить сервер"},
    "key_remove_selected": {"en": "Remove selected", "ru": "Удалить выбранное"},
    "key_cancel": {"en": "Cancel", "ru": "Отмена"},
    "key_language": {"en": "Language", "ru": "Язык"},
    "key_help": {"en": "Help", "ru": "Справка"},
    "dashboard_title": {"en": "Agents", "ru": "Агенты"},
    "col_agent": {"en": "Agent", "ru": "Агент"},
    "col_detected": {"en": "Detected", "ru": "Найден"},
    "col_servers": {"en": "Servers", "ru": "Серверы"},
    "col_config_path": {"en": "Config Path", "ru": "Путь к конфигу"},
    "yes": {"en": "yes", "ru": "да"},
    "no": {"en": "no", "ru": "нет"},
    "col_name": {"en": "Name", "ru": "Имя"},
    "col_command": {"en": "Command", "ru": "Команда"},
    "col_args": {"en": "Args", "ru": "Аргументы"},
    "col_valid": {"en": "Valid", "ru": "Валидно"},
    "wizard_catalog_prompt": {
        "en": "Pick from catalog (or leave blank for custom):",
        "ru": "Выбери из каталога (или оставь пусто для своего):",
    },
    "label_name": {"en": "Name", "ru": "Имя"},
    "label_command": {"en": "Command", "ru": "Команда"},
    "label_args": {"en": "Args (space-separated)", "ru": "Аргументы (через пробел)"},
    "wizard_targets_prompt": {
        "en": "Target agents (detected only):",
        "ru": "Целевые агенты (только найденные):",
    },
    "btn_add": {"en": "Add", "ru": "Добавить"},
    "help_title": {"en": "mcp-hub help", "ru": "Справка mcp-hub"},
    "help_body": {
        "en": (
            "mcp-hub detects which AI coding agents are installed on this "
            "machine (Claude Code, Codex, Antigravity) and lets you view "
            "and manage the MCP servers connected to each one.\n\n"
            "Screens:\n"
            "  Dashboard   - one row per agent: detected or not, how many "
            "servers, where its config file lives. Select a row to open it.\n"
            "  Server List - the MCP servers configured for that agent. "
            "Invalid entries show why parsing failed.\n"
            "  Add Wizard  - pick a server from the bundled catalog or "
            "enter one by hand, choose which detected agents to write it "
            "to, and confirm.\n\n"
            "Keys:\n"
            "  enter  - open the selected row\n"
            "  a      - open the add wizard (from a server list)\n"
            "  r      - remove the selected server (from a server list)\n"
            "  l      - toggle language (English / Russian)\n"
            "  ?      - this help screen\n"
            "  escape - go back\n"
            "  q      - quit\n\n"
            "Every add or remove writes a .bak copy of the config file "
            "before changing it."
        ),
        "ru": (
            "mcp-hub определяет, какие AI-агенты установлены на этой "
            "машине (Claude Code, Codex, Antigravity), и позволяет "
            "смотреть и управлять MCP-серверами, подключёнными к каждому.\n\n"
            "Экраны:\n"
            "  Dashboard   - по строке на агента: найден или нет, сколько "
            "серверов, где лежит его конфиг. Выбери строку, чтобы открыть.\n"
            "  Server List - MCP-серверы, настроенные у этого агента. "
            "Невалидные записи показывают причину ошибки.\n"
            "  Add Wizard  - выбери сервер из встроенного каталога или "
            "введи вручную, отметь, в каких найденных агентов записать, "
            "и подтверди.\n\n"
            "Клавиши:\n"
            "  enter  - открыть выбранную строку\n"
            "  a      - открыть мастер добавления (из списка серверов)\n"
            "  r      - удалить выбранный сервер (из списка серверов)\n"
            "  l      - переключить язык (English / Русский)\n"
            "  ?      - этот экран справки\n"
            "  escape - назад\n"
            "  q      - выход\n\n"
            "Перед каждой записью/удалением делается .bak копия конфига."
        ),
    },
}

_current_language = "en"


def get_language() -> str:
    return _current_language


def t(key: str) -> str:
    return STRINGS[key][_current_language]


def load_language() -> None:
    global _current_language
    _current_language = "en"
    if SETTINGS_PATH.exists():
        try:
            data = json.loads(SETTINGS_PATH.read_text())
            if data.get("language") in ("en", "ru"):
                _current_language = data["language"]
        except (OSError, json.JSONDecodeError):
            pass


def set_language(language: str) -> None:
    global _current_language
    _current_language = language
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps({"language": language}))


def toggle_language() -> None:
    set_language("ru" if _current_language == "en" else "en")


def retranslate_bindings(cls) -> None:
    """Rebuild a Textual DOMNode class's footer key hints in the current
    language. Bindings are normally baked into `cls.BINDINGS` once at
    import time and cached on `cls._merged_bindings`; this recomputes
    both from `cls._BINDING_SPEC` (key, action, i18n_key) so the footer
    reflects a language change without restarting the app.
    """
    cls.BINDINGS = [(key, action, t(i18n_key)) for key, action, i18n_key in cls._BINDING_SPEC]
    cls._merged_bindings = cls._merge_bindings()
