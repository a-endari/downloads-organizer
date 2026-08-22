import os
import shutil
import subprocess
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


def init_config(template: Path, *, force: bool = False) -> Path:
    """Create the user's configuration file from the supplied template."""
    destination = default_config_path()

    if destination.exists() and not force:
        raise FileExistsError(
            f"Configuration file already exists: {destination}",
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        template.read_text(encoding="utf-8"),
    )

    return destination


def _find_editor() -> str:
    """Return the first available editor from the user's environment or defaults."""
    configured_editor = os.environ.get("EDITOR")

    if configured_editor:
        return configured_editor

    if sys.platform == "win32":
        candidates = ("notepad",)
    else:
        candidates = ("nvim", "vim", "nano")

    for candidate in candidates:
        if shutil.which(candidate):
            return candidate

    raise RuntimeError(
        "No suitable text editor was found. "
        "Set the EDITOR environment variable to your preferred editor.",
    )


def edit_config(path: Path) -> None:
    """Open the configuration file in the user's preferred or fallback editor."""
    editor = _find_editor()
    subprocess.run([editor, str(path)], check=True)


def _load_categories(data: dict) -> dict[str, str]:
    """
    Load category key -> folder name mappings.

    Starts from the built-in categories, then merges in (and allows adding
    to, or overriding folder names for) any [categories.<key>] the user
    defines in TOML.
    """
    categories: dict[str, str] = Category.default_categories()
    categories_data = data.get("categories", {})

    category_aliases = {
        "documents": "document",
        "pictures": "picture",
        "audio": "audio",
        "video": "video",
        "code": "code",
        "programs": "program",
        "archives": "archive",
        "ebooks": "ebook",
        "other_files": "other",
        "other_folders": "other_folders",
    }

    for key, category_data in categories_data.items():
        folder = category_data.get("folder")
        if folder is None:
            continue

        internal_key = category_aliases.get(key, key)
        categories[internal_key] = folder

    return categories


def _parse_config_category(value: str, known_categories: dict[str, str]) -> str:
    """
    Resolve a TOML rule's category name into a category key.

    Accepts either a category key (e.g. "games") or a built-in display
    name (e.g. "Documents"), for convenience. Raises if the category was
    never declared in [categories] or among the built-ins.
    """
    normalized = value.strip().casefold()

    if normalized in known_categories:
        return normalized

    for key, folder in known_categories.items():
        if folder.casefold() == normalized:
            return key

    available = ", ".join(known_categories)
    raise ValueError(
        f"Unknown category '{value}' in configuration. "
        f"Define it under [categories.{normalized}] first, or use one of: {available}.",
    )


@dataclass(slots=True)
class RulesConfig:
    "User-configurable rules for classifying downloaded items."

    extensions: dict[str, str] = field(default_factory=dict)
    filenames: dict[str, str] = field(default_factory=dict)
    patterns: dict[str, str] = field(default_factory=dict)
    regex: dict[str, str] = field(default_factory=dict)


def _load_rules(data: dict, known_categories: dict[str, str]) -> RulesConfig:
    """Load user-defined classification rules."""
    rules_data = data.get("rules", {})

    return RulesConfig(
        extensions={
            extension.lower(): _parse_config_category(category, known_categories)
            for extension, category in rules_data.get("extensions", {}).items()
        },
        filenames={
            filename: _parse_config_category(category, known_categories)
            for filename, category in rules_data.get("filenames", {}).items()
        },
        patterns={
            pattern: _parse_config_category(category, known_categories)
            for pattern, category in rules_data.get("patterns", {}).items()
        },
        regex={
            pattern: _parse_config_category(category, known_categories)
            for pattern, category in rules_data.get("regex", {}).items()
        },
    )


@dataclass(slots=True)
class Config:
    """Resolved application configuration."""

    downloads_directory: Path = field(default_factory=lambda: DEFAULT_DOWNLOADS_DIR)
    categories: dict[str, str] = field(default_factory=Category.default_categories)
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
        general.get("downloads_directory", DEFAULT_DOWNLOADS_DIR),
    ).expanduser()

    categories = _load_categories(data)
    rules = _load_rules(data, categories)

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
