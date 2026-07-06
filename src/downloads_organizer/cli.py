import argparse
from pathlib import Path
from .organizer import DownloadsOrganizer


def run() -> int:
    parser = argparse.ArgumentParser(
        prog="downloads-organizer", description="Organize files in your Downloads folder."
    )
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
    )
    scan_parser = subparser.add_parser(
        "scan",
        help="Scan a directory without moving files.",
    )
    args = parser.parse_args()
    downloads = Path.home() / "Downloads"
    organizer = DownloadsOrganizer(downloads)

    results = organizer.scan()
    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")
    return 0
