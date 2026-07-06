from pathlib import Path

from .constants import IGNORED_FILENAMES
from .models import ScanResult
from .rules import FileCategorizer


class DownloadsOrganizer:
    """Scan directories and determine where files belong."""

    def __init__(self, source_directory: Path) -> None:
        self.source_directory = source_directory
        self.categorizer = FileCategorizer()

    def scan(self) -> list[ScanResult]:
        """Scan the directory and return categorized files."""

        results: list[ScanResult] = []

        for item in self.source_directory.iterdir():
            if item.is_dir():
                continue

            if item.name in IGNORED_FILENAMES:
                continue

            category = self.categorizer.get_category(item)

            results.append(
                ScanResult(
                    source=item,
                    category=category,
                )
            )
        return results
