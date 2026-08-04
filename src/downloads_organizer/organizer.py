import shutil
from collections.abc import Iterator
from pathlib import Path

from downloads_organizer.config import Config
from .models import Category, MoveResult, ScanResult
from .rules import FileCategorizer, PACKAGE_EXTENSIONS


class DownloadsOrganizer:
    """Scan directories and determine where files belong."""

    def __init__(
        self,
        source_directory: Path,
        config: Config | None = None,
    ) -> None:
        self.source_directory = source_directory
        self.config = config or Config()
        self.categorizer = FileCategorizer()

    @staticmethod
    def _is_package(path: Path) -> bool:
        """Return True if the path is a filesystem package treated as a file."""
        return path.suffix.lower() in PACKAGE_EXTENSIONS

    def _iter_folders(self) -> Iterator[Path]:
        """Yield directories that should be moved."""
        for item in self.source_directory.iterdir():
            if not item.is_dir():
                continue

            if self._is_package(item):
                continue

            if item.name in self.config.ignored_directories:
                continue

            if item.name in Category.directory_names():
                continue

            yield item

    def _iter_files(self) -> Iterator[Path]:
        """Yield files from the source directory."""

        for item in self.source_directory.iterdir():
            if item.is_dir() and not self._is_package(item):
                continue

            if item.name in self.config.ignored_files:
                continue

            yield item

    def scan(self) -> list[ScanResult]:
        """Scan the directory and return categorized files."""

        results: list[ScanResult] = []

        for item in self._iter_files():
            category = self.categorizer.get_category(item)

            results.append(
                ScanResult(
                    source=item,
                    category=category,
                )
            )
        for folder in self._iter_folders():
            results.append(
                ScanResult(
                    source=folder,
                    category=Category.OTHER_FOLDERS,
                )
            )
        return results

    def _get_category_directory(self, category: Category) -> Path:
        """Return the directory for a category."""
        return self.source_directory / category

    @staticmethod
    def _ensure_directory(directory: Path) -> None:
        """Create a directory if it does not already exist."""
        directory.mkdir(exist_ok=True)

    def _get_destination_path(self, result: ScanResult) -> Path:
        destination = self._get_category_directory(result.category)
        candidate = destination / result.source.name

        if not candidate.exists():
            return candidate

        stem = result.source.stem
        suffix = result.source.suffix

        counter = 1

        while True:
            candidate = destination / f"{stem} ({counter}){suffix}"

            if not candidate.exists():
                return candidate

            counter += 1

    def plan_moves(
        self,
        *,
        only: Category | None = None,
    ) -> list[MoveResult]:
        results = self.scan()

        move_results: list[MoveResult] = []

        for result in results:
            if only is not None and result.category != only:
                continue
            destination_path = self._get_destination_path(result)

            move_results.append(
                MoveResult(
                    source=result.source,
                    destination=destination_path,
                    category=result.category,
                )
            )

        return move_results

    def organize(self, only: Category | None = None) -> list[MoveResult]:
        move_results = self.plan_moves(only=only)

        for move in move_results:
            self._ensure_directory(move.destination.parent)
            shutil.move(
                move.source,
                move.destination,
            )

        return move_results
