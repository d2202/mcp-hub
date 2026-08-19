import json

from mcp_hub import i18n, settings


def test_default_language_is_en(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_PATH", tmp_path / "settings.json")
    i18n.load_language()
    assert i18n.get_language() == "en"


def test_t_returns_english_by_default(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_PATH", tmp_path / "settings.json")
    i18n.load_language()
    assert i18n.t("help_title") == "mcp-hub help"


def test_set_language_switches_and_persists(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", settings_path)
    i18n.load_language()

    i18n.set_language("ru")

    assert i18n.get_language() == "ru"
    assert i18n.t("help_title") == "Справка mcp-hub"
    assert json.loads(settings_path.read_text()) == {"language": "ru"}


def test_load_language_reads_persisted_choice(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(json.dumps({"language": "ru"}))
    monkeypatch.setattr(settings, "SETTINGS_PATH", settings_path)

    i18n.load_language()

    assert i18n.get_language() == "ru"


def test_toggle_language_flips_between_en_and_ru(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_PATH", tmp_path / "settings.json")
    i18n.load_language()

    i18n.toggle_language()
    assert i18n.get_language() == "ru"

    i18n.toggle_language()
    assert i18n.get_language() == "en"


def test_set_language_preserves_other_settings_keys(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", settings_path)
    settings.save(theme="textual-light")

    i18n.set_language("ru")

    assert json.loads(settings_path.read_text()) == {
        "theme": "textual-light",
        "language": "ru",
    }
