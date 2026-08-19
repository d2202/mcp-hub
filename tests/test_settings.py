import json

from mcp_hub import settings


def test_load_returns_empty_dict_when_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_PATH", tmp_path / "settings.json")
    assert settings.load() == {}


def test_save_creates_file_with_given_keys(tmp_path, monkeypatch):
    path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", path)

    settings.save(language="ru")

    assert json.loads(path.read_text()) == {"language": "ru"}


def test_save_merges_instead_of_overwriting(tmp_path, monkeypatch):
    path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", path)

    settings.save(language="ru")
    settings.save(theme="textual-light")

    assert json.loads(path.read_text()) == {
        "language": "ru",
        "theme": "textual-light",
    }


def test_load_ignores_malformed_json(tmp_path, monkeypatch):
    path = tmp_path / "settings.json"
    path.write_text("{not valid json")
    monkeypatch.setattr(settings, "SETTINGS_PATH", path)

    assert settings.load() == {}
