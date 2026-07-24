from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Category(StrEnum):
    """Supported file categories."""

    DOCUMENT = "Documents"
    PICTURE = "Pictures"
    AUDIO = "Audio"
    VIDEO = "Video"
    CODE = "Code"
    PROGRAM = "Programs"
    ARCHIVE = "Archives"
    OTHER = "Other"

    @classmethod
    def values(cls) -> list[str]:
        """Return the display names of all categories."""

        return list(cls)

    @classmethod
    def from_string(cls, value: str) -> "Category":
        """Return the matching category from a user-provided string."""

        normalized = value.strip().casefold()

        for category in cls:
            if category.value.casefold() == normalized:
                return category

        available = ", ".join(cls.values())

        raise ValueError(f"Unknown category '{value}'. Available categories: {available}")


@dataclass(slots=True, frozen=True)
class ScanResult:
    """Represents a scanned file and its destination category."""

    source: Path
    category: Category


@dataclass(slots=True)
class MoveResult:
    source: Path
    destination: Path
    category: Category
