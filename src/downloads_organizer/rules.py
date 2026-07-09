from pathlib import Path

from .models import Category


class FileCategorizer:
    """Determine the category of a file based on its extension."""

    DEFAULT_RULES: dict[str, Category] = {
        ".pdf": Category.DOCUMENT,
        ".doc": Category.DOCUMENT,
        ".docx": Category.DOCUMENT,
        ".txt": Category.DOCUMENT,
        ".jpg": Category.PICTURE,
        ".webp": Category.PICTURE,
        ".svg": Category.PICTURE,
        ".jpeg": Category.PICTURE,
        ".png": Category.PICTURE,
        ".gif": Category.PICTURE,
        ".mp4": Category.VIDEO,
        ".mkv": Category.VIDEO,
        ".mov": Category.VIDEO,
        ".mp3": Category.AUDIO,
        ".flac": Category.AUDIO,
        ".wav": Category.AUDIO,
        ".zip": Category.ARCHIVE,
        ".rar": Category.ARCHIVE,
        ".7z": Category.ARCHIVE,
        ".py": Category.CODE,
        ".js": Category.CODE,
        ".html": Category.CODE,
        ".css": Category.CODE,
        ".exe": Category.PROGRAM,
        ".apk": Category.PROGRAM,
        ".dmg": Category.PROGRAM,
    }

    def __init__(self, rules: dict[str, Category] | None = None) -> None:
        self.rules = rules or self.DEFAULT_RULES

    def get_category(self, file_path: Path) -> Category:
        """
        Return the destination category for a file.

        Unknown extensions are placed in 'Other'.
        """
        extension = file_path.suffix.lower()
        return self.rules.get(extension, Category.OTHER)
