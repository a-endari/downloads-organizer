import argparse
from pathlib import Path

from .organizer import DownloadsOrganizer


def get_organizer(directory: Path) -> DownloadsOrganizer:
    directory = directory.expanduser()
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    return DownloadsOrganizer(directory)


def handle_scan(directory: Path) -> None:
    organizer = get_organizer(directory)
    results = organizer.scan()

    for result in results:
        print(f"{result.source.name:<30} -> {result.category}")


def handle_stats(directory: Path) -> None:
    organizer = get_organizer(directory)
    results = organizer.scan()

    print(f"Directory : {directory.resolve()}")
    print(f"Files     : {len(results)}")


def handle_organize(
    directory: Path,
    *,
    dry_run: bool,
    verbose: bool,
) -> None:
    organizer = get_organizer(directory)
    move_results = organizer.plan_moves()
    if not move_results:
        print("No files to organize.")
        return
    if not dry_run:
        move_results = organizer.organize()

    verb = "Would move" if dry_run else "Moved"
    count = len(move_results)
    noun = "file" if count == 1 else "files"
    print(f"{verb} {count} {noun}.")
    if verbose:
        for move in move_results:
            print(f"{move.source.name} -> {move.destination.relative_to(directory)}")


def run() -> int:
    parser = argparse.ArgumentParser(
        prog="downloads-organizer",
        description="Organize files in your Downloads folder.",
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

    organize_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without moving files.",
    )

    organize_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output.",
    )
    args = parser.parse_args()

    try:
        if args.command == "scan":
            handle_scan(args.directory)

        elif args.command == "stats":
            handle_stats(args.directory)

        elif args.command == "organize":
            handle_organize(args.directory, dry_run=args.dry_run, verbose=args.verbose)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(error)
        return 1
    return 0
