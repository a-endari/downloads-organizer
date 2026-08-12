from pathlib import Path

DEFAULT_DOWNLOADS_DIR = Path.home() / "Downloads"

DEFAULT_IGNORED_FILES: set[str] = {
    ".DS_Store",
    ".localized",
    "desktop.ini",
    "Thumbs.db",
}
