from dataclasses import dataclass, field
from pathlib import Path

import tomllib

DEFAULT_IGNORED_FILES: set[str] = {
    ".DS_Store",
    ".localized",
    "desktop.ini",
    "Thumbs.db",
}


@dataclass(slots=True)
class Config:
    """Application configuration."""

    ignored_files: set[str] = field(
        default_factory=lambda: DEFAULT_IGNORED_FILES.copy())
    ignored_directories: set[str] = field(default_factory=set)


def load_config(path: Path | None = None) -> Config:
    """Load configuration from a TOML file."""

    if path is None:
        return Config()

    with path.open("rb") as config_file:
        data = tomllib.load(config_file)

    ignore = data.get("ignore", {})
    ignored_files = DEFAULT_IGNORED_FILES.copy()
    ignored_files.update(ignore.get("files", []))

    ignored_directories = set(ignore.get("directories", []))

    return Config(
        ignored_files=ignored_files,
        ignored_directories=ignored_directories,
    )
