import argparse
import sys
from pathlib import Path

from downloads_organizer.config import (
    default_config_path,
    edit_config,
    init_config,
    load_config,
)

from .constants import DEFAULT_DOWNLOADS_DIR
from .models import Category
from .organizer import DownloadsOrganizer


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


def handle_config(args: argparse.Namespace) -> None:
    """Handle configuration management commands."""
    config_path = default_config_path()
    template_path = Path("config/config.toml")

    if args.init:
        try:
            created_path = init_config(template_path)
        except FileExistsError as error:
            print(error)
            return

        print(f"Created configuration file:\n  {created_path}")
        return

    if args.edit:
        if not config_path.exists():
            try:
                init_config(template_path)
            except FileExistsError:
                pass

        print(f"Opening configuration:\n  {config_path}")
        edit_config(config_path)
        return

    print(f"Configuration file:\n  {config_path}")


def run() -> int:
    config = load_config()
    parser = argparse.ArgumentParser(
        prog="downloads-organizer",
        description="Safely organize and manage your Downloads folder.",
        epilog=(
            "Examples:\n"
            "  downloads-organizer\n"
            "  downloads-organizer stats\n"
            "  downloads-organizer organize --dry-run\n"
            "  downloads-organizer organize --verbose\n"
            "  downloads-organizer config --edit\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparser = parser.add_subparsers(
        dest="command",
    )
    config_parser = subparser.add_parser(
        "config",
        help="Manage the Downloads Organizer configuration.",
    )

    config_parser.add_argument(
        "-I",
        "--init",
        action="store_true",
        help="Create the default configuration file.",
    )

    config_parser.add_argument(
        "-e",
        "--edit",
        action="store_true",
        help="Open the configuration file in your editor.",
    )

    stat_parser = subparser.add_parser(
        "stats",
        help="Analyze a directory without changing anything.",
        description=(
            "Show information about the contents of a directory.\n"
            "This command never modifies files."
        ),
    )

    stat_parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=config.downloads_directory,
        help="Directory to analyze (defaults to your Downloads folder.)",
    )

    organize_parser = subparser.add_parser(
        "organize",
        help="Organize files into category folders.",
        description=(
            "Organize files and folders in a Downloads directory "
            "according to your configured rules.\n\n"
            "Use --dry-run to preview changes without modifying anything."
        ),
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

        elif args.command == "config":
            handle_config(args)

    except (FileNotFoundError, NotADirectoryError) as error:
        print(error)
        return 1
    return 0
