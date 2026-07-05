from pathlib import Path
from .rules import FileCategorizer


class DownloadsOrganizer:
    """Scan directories and determine where files belong."""

    def __init__(self, source_directory: Path) -> None:
        self.source_directory = source_directory
        self.categorizer = FileCategorizer()

    def scan(self) -> None:
        """Scan the directory and print file categories."""

        for item in self.source_directory.iterdir():
            if item.is_dir():
                continue
            category = self.categorizer.get_category(item)

            print(f"{item.name:<30} -> {category}")
