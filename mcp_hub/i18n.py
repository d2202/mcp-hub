from mcp_hub import settings

STRINGS: dict[str, dict[str, str]] = {
    "key_quit": {"en": "Quit", "ru": "Выход"},
    "key_back": {"en": "Back", "ru": "Назад"},
    "key_add_server": {"en": "Add server", "ru": "Добавить сервер"},
    "key_edit_server": {"en": "Edit selected", "ru": "Редактировать выбранное"},
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
    "label_env": {
        "en": "Env (KEY=value, space-separated)",
        "ru": "Переменные окружения (KEY=value, через пробел)",
    },
    "wizard_targets_prompt": {
        "en": "Target agents (detected only):",
        "ru": "Целевые агенты (только найденные):",
    },
    "btn_add": {"en": "Add", "ru": "Добавить"},
    "btn_save": {"en": "Save", "ru": "Сохранить"},
    "btn_yes": {"en": "Yes", "ru": "Да"},
    "btn_no": {"en": "No", "ru": "Нет"},
    "confirm_remove": {
        "en": "Remove server '{name}'? A .bak copy of the config is kept.",
        "ru": "Удалить сервер '{name}'? Сохранится .bak копия конфига.",
    },
    "confirm_overwrite": {
        "en": "A server named '{name}' already exists. Overwrite it?",
        "ru": "Сервер с именем '{name}' уже существует. Перезаписать?",
    },
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
            "  e      - edit the selected server (from a server list)\n"
            "  r      - remove the selected server (from a server list)\n"
            "  l      - toggle language (English / Russian)\n"
            "  ?      - this help screen\n"
            "  ctrl+p - command palette (change theme and more)\n"
            "  escape - go back\n"
            "  q      - quit\n\n"
            "Every add or remove writes a .bak copy of the config file "
            "before changing it. The chosen language and theme are "
            "remembered for the next run."
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
            "  e      - редактировать выбранный сервер (из списка серверов)\n"
            "  r      - удалить выбранный сервер (из списка серверов)\n"
            "  l      - переключить язык (English / Русский)\n"
            "  ?      - этот экран справки\n"
            "  ctrl+p - палитра команд (смена темы и не только)\n"
            "  escape - назад\n"
            "  q      - выход\n\n"
            "Перед каждой записью/удалением делается .bak копия конфига. "
            "Выбранные язык и тема запоминаются до следующего запуска."
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
    language = settings.load().get("language")
    if language in ("en", "ru"):
        _current_language = language


def set_language(language: str) -> None:
    global _current_language
    _current_language = language
    settings.save(language=language)


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
