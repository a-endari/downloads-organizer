from pathlib import Path
from .organizer import DownloadsOrganizer


def run() -> int:
    downloads = Path.home() / "Downloads"
    organizer = DownloadsOrganizer(downloads)

    results = organizer.scan()
    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")
    return 0
