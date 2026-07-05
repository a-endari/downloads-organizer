from pathlib import Path

from .organizer import DownloadsOrganizer


def main() -> None:
    downloads = Path.home() / "Downloads"

    organizer = DownloadsOrganizer(downloads)

    results = organizer.scan()

    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")


if __name__ == "__main__":
    main()
