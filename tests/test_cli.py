from pathlib import Path

import pytest

import downloads_organizer.cli as cli_module


def test_config_show_displays_effective_defaults(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "config.toml"

    monkeypatch.setattr(
        cli_module,
        "default_config_path",
        lambda: config_path,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["downloads-organizer", "config", "--show"],
    )

    result = cli_module.run()

    output = capsys.readouterr().out

    assert result == 0
    assert "Downloads Organizer - Effective Configuration" in output
    assert "Configuration" in output
    assert "Built-in defaults (no config file found)" in output
    assert "General Settings" in output
    assert "Categories" in output
    assert "Ignored Files" in output
    assert "Ignored Directories" in output
    assert "Classification Rules" in output
    assert "Filename truncation: 45 characters" in output
    assert "None configured." in output
    assert not config_path.exists()


def test_config_show_displays_user_overrides_and_merged_defaults(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[general]
downloads_directory = "~/MyDownloads"
truncate_length = 60

[categories.documents]
folder = "My Documents"

[categories.games]
folder = "Games"

[rules.extensions]
".pdf" = "documents"

[rules.filenames]
"README" = "games"

[rules.patterns]
"*.zip" = "games"

[rules.regex]
'^invoice_.*\\.pdf$' = "documents"

[ignore]
files = ["custom.tmp"]
directories = ["Incomplete", "Temp"]
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        cli_module,
        "default_config_path",
        lambda: config_path,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["downloads-organizer", "config", "--show"],
    )

    result = cli_module.run()

    output = capsys.readouterr().out

    assert result == 0

    # Configuration information
    assert str(config_path) in output
    assert "Config file exists: Yes" in output
    assert "Built-in defaults + user overrides" in output

    # General settings
    assert str(Path("~/MyDownloads").expanduser()) in output
    assert "Filename truncation: 60 characters" in output

    # Categories
    assert "My Documents" in output
    assert "Games" in output

    # Ignored files: user-defined and built-in entries
    assert "custom.tmp" in output
    assert ".DS_Store" in output

    # Ignored directories
    assert "Incomplete" in output
    assert "Temp" in output

    # Classification rules use configured destination folder names
    assert ".pdf" in output
    assert "README" in output
    assert "*.zip" in output
    assert "^invoice_.*\\.pdf$" in output

    assert "→  My Documents" in output
    assert "→  Games" in output


def test_config_show_does_not_modify_existing_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "config.toml"
    original_content = """
[general]
truncate_length = 55
"""

    config_path.write_text(original_content, encoding="utf-8")

    monkeypatch.setattr(
        cli_module,
        "default_config_path",
        lambda: config_path,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["downloads-organizer", "config", "--show"],
    )

    result = cli_module.run()

    capsys.readouterr()

    assert result == 0
    assert config_path.read_text(encoding="utf-8") == original_content


def test_config_show_displays_empty_rule_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[general]
truncate_length = 45
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        cli_module,
        "default_config_path",
        lambda: config_path,
    )
    monkeypatch.setattr(
        "sys.argv",
        ["downloads-organizer", "config", "--show"],
    )

    result = cli_module.run()

    output = capsys.readouterr().out

    assert result == 0
    assert "File Extensions:" in output
    assert "Exact Filenames:" in output
    assert "Glob Patterns:" in output
    assert "Regular Expressions:" in output

    assert output.count("None configured.") >= 4
