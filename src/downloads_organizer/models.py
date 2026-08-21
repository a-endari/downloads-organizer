from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Category(StrEnum):
    """Built-in file categories. User config can define additional ones."""

    DOCUMENT = "Documents"
    PICTURE = "Pictures"
    AUDIO = "Music"
    VIDEO = "Video"
    CODE = "Code"
    PROGRAM = "Programs"
    ARCHIVE = "Archives"
    EBOOK = "Ebooks"
    OTHER = "Other Files"
    OTHER_FOLDERS = "Other Folders"

    @property
    def key(self) -> str:
        """Return the stable configuration key for this category."""
        return self.name.lower()

    @classmethod
    def values(cls) -> list[str]:
        """Return the display names of all categories."""
        return list(cls)

    @classmethod
    def default_categories(cls) -> dict[str, str]:
        """Return the built-in key -> folder name mapping."""

        return {category.key: category.value for category in cls}


@dataclass(slots=True, frozen=True)
class ScanResult:
    """Represents a scanned file and its destination category."""

    source: Path
    category: str


@dataclass(slots=True)
class MoveResult:
    """Represents a planned or completed move of a source file to its destination."""

    source: Path
    destination: Path
    category: str
