import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import tomllib

from .constants import DEFAULT_DOWNLOADS_DIR, DEFAULT_IGNORED_FILES
from .models import Category


def default_config_path() -> Path:
    """Return the OS-appropriate default config file location."""
    app_name = "downloads-organizer"

    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        base_dir = Path(base) if base else Path.home() / "AppData" / "Roaming"
    else:
        base = os.environ.get("XDG_CONFIG_HOME")
        base_dir = Path(base) if base else Path.home() / ".config"

    return base_dir / app_name / "config.toml"


def _load_categories(data: dict) -> dict[Category, str]:
    """Load configured category destination folder names."""
    categories_data = data.get("categories", {})

    categories: dict[Category, str] = {}

    for category in Category:
        category_data = categories_data.get(category.key, {})
        folder = category_data.get("folder", category.value)
        categories[category] = folder

    return categories


def _parse_config_category(value: str) -> Category:
    """Convert a TOML category name into a Category enum."""
    normalized = value.strip().casefold()

    for category in Category:
        if category.key == normalized:
            return category

    available = ", ".join(category.key for category in Category)
    raise ValueError(
        f"Invalid category '{value}' in configuration. Expected one of: {available}.",
    )


@dataclass(slots=True)
class RulesConfig:
    "User-configurable rules for classifying downloaded items."

    extensions: dict[str, Category] = field(default_factory=dict)
    filenames: dict[str, Category] = field(default_factory=dict)
    patterns: dict[str, Category] = field(default_factory=dict)
    regex: dict[str, Category] = field(default_factory=dict)


def _load_rules(data: dict) -> RulesConfig:
    """Load user-defined classification rules."""
    rules_data = data.get("rules", {})

    return RulesConfig(
        extensions={
            extension.lower(): _parse_config_category(category)
            for extension, category in rules_data.get("extensions", {}).items()
        },
        filenames={
            filename: _parse_config_category(category)
            for filename, category in rules_data.get("filenames", {}).items()
        },
        patterns={
            pattern: _parse_config_category(category)
            for pattern, category in rules_data.get("patterns", {}).items()
        },
        regex={
            pattern: _parse_config_category(category)
            for pattern, category in rules_data.get("regex", {}).items()
        },
    )


@dataclass(slots=True)
class Config:
    """Resolved application configuration."""

    downloads_directory: Path = DEFAULT_DOWNLOADS_DIR
    categories: dict[Category, str] = field(
        default_factory=lambda: {category: category.value for category in Category},
    )
    rules: RulesConfig = field(default_factory=RulesConfig)

    ignored_files: set[str] = field(
        default_factory=DEFAULT_IGNORED_FILES.copy,
    )
    ignored_directories: set[str] = field(default_factory=set)


def load_config(path: Path | None = None) -> Config:
    """Load configuration from TOML, falling back to application defaults."""

    if path is None:
        path = default_config_path()

    path = path.expanduser()

    if not path.exists():
        return Config()

    with path.open("rb") as config_file:
        data = tomllib.load(config_file)

    general = data.get("general", {})

    downloads_directory = Path(
        general.get("downloads_directory", str(DEFAULT_DOWNLOADS_DIR)),
    ).expanduser()

    categories = _load_categories(data)
    rules = _load_rules(data)

    ignore = data.get("ignore", {})

    ignored_files = DEFAULT_IGNORED_FILES.copy()
    ignored_files.update(ignore.get("files", []))

    ignored_directories = set(ignore.get("directories", []))

    return Config(
        downloads_directory=downloads_directory,
        categories=categories,
        rules=rules,
        ignored_files=ignored_files,
        ignored_directories=ignored_directories,
    )
