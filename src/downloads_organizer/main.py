from pathlib import Path
from .organizer import DownloadsOrganizer


def main() -> None:
    downloads = Path.home() / "Downloads"

    organizer = DownloadsOrganizer(downloads)
    organizer.scan()


if __name__ == "__main__":
    main()
