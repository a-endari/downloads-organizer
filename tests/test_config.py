from importlib.resources import files
from pathlib import Path

import pytest

import downloads_organizer.config as config_module
from downloads_organizer.config import Config


def test_packaged_config_template_is_available() -> None:
    template = (
        files("downloads_organizer").joinpath("templates").joinpath("config.toml")
    )

    assert template.is_file()
    assert "downloads_directory" in template.read_text(encoding="utf-8")


def test_init_config_creates_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "downloads_organizer" / "config.toml"

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    created_path = config_module.init_config()

    assert created_path == destination
    assert destination.is_file()
    assert "downloads_directory" in destination.read_text(encoding="utf-8")


def test_config_has_empty_ignored_directories_by_default() -> None:
    config = Config()

    assert config.ignored_directories == set()


def test_plural_category_alias_resolves_to_internal_key(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "config.toml"
    destination.write_text(
        '[rules.extensions]\n".pdf" = "documents"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    config = config_module.load_config()

    assert config.rules.extensions[".pdf"] == "document"


def test_category_alias_resolves_after_folder_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "config.toml"
    destination.write_text(
        '[categories.documents]\nfolder = "My Documents"\n\n'
        '[rules.extensions]\n".pdf" = "documents"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    config = config_module.load_config()

    assert config.rules.extensions[".pdf"] == "document"
    assert config.categories["document"] == "My Documents"


def test_canonical_internal_key_resolves_correctly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "config.toml"
    destination.write_text(
        '[rules.extensions]\n".pdf" = "document"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    config = config_module.load_config()

    assert config.rules.extensions[".pdf"] == "document"


def test_custom_category_resolves_correctly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "config.toml"
    destination.write_text(
        '[categories.games]\nfolder = "Games"\n\n'
        '[rules.extensions]\n".game" = "games"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    config = config_module.load_config()

    assert config.rules.extensions[".game"] == "games"
    assert config.categories["games"] == "Games"


def test_invalid_category_raises_value_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "config.toml"
    destination.write_text(
        '[rules.extensions]\n".xyz" = "nonexistent"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        config_module,
        "default_config_path",
        lambda: destination,
    )

    with pytest.raises(ValueError, match="Unknown category"):
        config_module.load_config()
