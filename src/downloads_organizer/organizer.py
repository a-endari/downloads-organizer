import shutil
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

    def _get_category_directory(self, category: str) -> Path:
        """Return the directory for a category."""
        return self.source_directory / category

    def _ensure_directory(self, directory: Path) -> None:
        """Create a directory if it does not already exist."""
        directory.mkdir(exist_ok=True)

    def _get_destination_path(self, result: ScanResult) -> Path:
        destination = self._get_category_directory(result.category)
        return destination / result.source.name

    def organize(self) -> None:
        results = self.scan()

        for result in results:
            destination = self._get_category_directory(result.category)

            self._ensure_directory(destination)

            shutil.move(
                result.source,
                self._get_destination_path(result),
            )
