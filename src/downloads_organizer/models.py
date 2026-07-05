from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ScanResult:
    """Represents a scanned file and its destination category."""

    source: Path
    category: str
