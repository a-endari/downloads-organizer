from importlib.resources import files
from pathlib import Path

import downloads_organizer.config as config_module
import pytest


def test_packaged_config_template_is_available() -> None:
    template = files("downloads_organizer").joinpath("templates").joinpath("config.toml")

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
