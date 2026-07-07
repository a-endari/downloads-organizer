import argparse
from pathlib import Path
from .organizer import DownloadsOrganizer


def handle_scan(directory: Path) -> None:
    organizer = DownloadsOrganizer(directory)

    results = organizer.scan()

    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")


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
    scan_parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="Directory to scan (defaults to your Downloads foleder.)",
    )
    args = parser.parse_args()

    if args.command == "scan":
        handle_scan(args.directory)
    return 0
