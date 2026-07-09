from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Category(StrEnum):
    """Supported file categories."""

    DOCUMENT = "Documents"
    PICTURE = "Pictures"
    AUDIO = "Audio"
    VIDEO = "Videos"
    CODE = "Codes"
    PROGRAM = "Programs"
    ARCHIVE = "Archives"
    OTHER = "Other"


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
