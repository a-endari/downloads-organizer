from pathlib import Path

DEFAULT_CATEGORY = "Other"

DEFAULT_DOWNLOADS_DIR = Path.home() / "Downloads"

DEFAULT_RULES_FILE = Path("config") / "rules.json"

IGNORED_FILENAMES: set[str] = {
    ".DS_Store",
    ".localized",
    "desktop.ini",
    "Thumbs.db",
}
