import argparse
from pathlib import Path
from .organizer import DownloadsOrganizer


def handle_scan(directory: Path) -> None:
    organizer = DownloadsOrganizer(directory)

    results = organizer.scan()

    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")


def handle_stats(directory: Path) -> None:
    organizer = DownloadsOrganizer(directory)

    results = organizer.scan()

    print(f"Directory : {directory}")
    print(f"Files     : {len(results)}")


def handle_organzie(directory: Path) -> None:
    organizer = DownloadsOrganizer(directory)

    results = organizer.scan()
    for result in results:
        print(f"{result.source.name}")

        print(f"  -> {result.category}")


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
        help="Directory to scan (defaults to your Downloads folder.)",
    )

    stat_parser = subparser.add_parser(
        "stats",
        help="Show statistics about a directory.",
    )

    stat_parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="Directory to analyze (defaults to your Downloads folder.)",
    )

    organize_parser = subparser.add_parser(
        "organize",
        help="Organize files into category folders.",
    )

    organize_parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="Directory to organize (defaults to your Downloads folder.)",
    )

    args = parser.parse_args()

    if args.command == "scan":
        handle_scan(args.directory)

    elif args.command == "stats":
        handle_stats(args.directory)

    elif args.command == "organize":
        handle_organzie(args.directory)
    return 0
