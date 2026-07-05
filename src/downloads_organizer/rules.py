from pathlib import Path


class FileCategorizer:
    """Determine the category of a file based on its extension."""

    DEFAULT_RULES: dict[str, str] = {
        ".pdf": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".txt": "Documents",
        ".jpg": "Pictures",
        ".jpeg": "Pictures",
        ".png": "Pictures",
        ".gif": "Pictures",
        ".mp4": "Videos",
        ".mkv": "Videos",
        ".mov": "Videos",
        ".mp3": "Audio",
        ".wav": "Audio",
        ".zip": "Archives",
        ".rar": "Archives",
        ".7z": "Archives",
        ".py": "Code",
        ".js": "Code",
        ".html": "Code",
        ".css": "Code",
    }

    def __init__(self, rules: dict[str, str] | None = None) -> None:
        self.rules = rules or self.DEFAULT_RULES

    def get_category(self, file_path: Path) -> str:
        """
        Return the destination category for a file.

        Unknown extensions are placed in 'Other'.
        """
        extension = file_path.suffix.lower()
        return self.rules.get(extension, "Other")
