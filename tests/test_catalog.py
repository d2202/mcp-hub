from pathlib import Path

from mcp_hub.catalog import CATALOG_PATH, load_catalog


def test_bundled_catalog_loads_and_has_known_entries():
    specs = load_catalog()
    names = {s.name for s in specs}
    assert "filesystem" in names
    assert "github" in names


def test_load_catalog_from_custom_path(tmp_path):
    path = tmp_path / "catalog.yaml"
    path.write_text(
        "- name: demo\n"
        "  command: npx\n"
        "  args: [\"-y\", \"demo-mcp\"]\n"
        "  env: [\"API_KEY\"]\n"
    )
    specs = load_catalog(path)
    assert len(specs) == 1
    assert specs[0].name == "demo"
    assert specs[0].args == ["-y", "demo-mcp"]
    assert specs[0].env == {"API_KEY": ""}


def test_catalog_path_points_at_bundled_file():
    assert CATALOG_PATH.name == "catalog.yaml"
    assert Path(CATALOG_PATH).exists()
