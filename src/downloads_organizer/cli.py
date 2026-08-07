import argparse
import sys
from pathlib import Path

from downloads_organizer.config import load_config
from .models import Category
from .organizer import DownloadsOrganizer
from .constants import DEFAULT_DOWNLOADS_DIR


def get_organizer(directory: Path) -> DownloadsOrganizer:
    directory = directory.expanduser()
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    config = load_config()
    return DownloadsOrganizer(directory, config=config)


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
    only: Category | None = None,
) -> None:
    organizer = get_organizer(directory)

    if dry_run:
        move_results = organizer.plan_moves(only=only)

    else:
        move_results = organizer.organize(only=only)

    if not move_results:
        print("No files to organize.")

        return

    verb = "Would move" if dry_run else "Moved"
    count = len(move_results)
    noun = "file" if count == 1 else "files"
    print(f"{verb} {count} {noun}.")
    if verbose:
        for move in move_results:
            print(f"{move.source.name} -> {move.destination.relative_to(directory)}")


def _insert_default_command(argv: list[str], commands: set[str]) -> list[str]:
    """Allow 'stats' to be omitted: bare dir/no-arg invocations imply 'stats'."""
    if argv and (argv[0] in commands or argv[0] in ("-h", "--help")):
        return argv
    return ["stats", *argv]


def run() -> int:
    parser = argparse.ArgumentParser(
        prog="downloads-organizer",
        description="Organize files in your Downloads folder.",
    )
    subparser = parser.add_subparsers(
        dest="command",
    )

    stat_parser = subparser.add_parser(
        "stats",
        help="Show statistics about a directory.",
    )

    stat_parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=DEFAULT_DOWNLOADS_DIR,
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
        default=DEFAULT_DOWNLOADS_DIR,
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

    organize_parser.add_argument(
        "--only",
        metavar="CATEGORY",
        help=(
            "Only organize files from a single category.\n"
            f"Available categories: {', '.join(Category.values())}"
        ),
    )
    commands = set(subparser.choices)
    argv = _insert_default_command(sys.argv[1:], commands)
    args = parser.parse_args(argv)

    try:
        if args.command is None or args.command == "stats":
            handle_stats(args.directory)

        elif args.command == "organize":
            only: Category | None = None

            if args.only is not None:
                try:
                    only = Category.from_string(args.only)
                except ValueError as error:
                    parser.error(str(error))

            handle_organize(
                args.directory,
                dry_run=args.dry_run,
                verbose=args.verbose,
                only=only,
            )
    except (FileNotFoundError, NotADirectoryError) as error:
        print(error)
        return 1
    return 0
