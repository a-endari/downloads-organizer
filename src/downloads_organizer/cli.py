import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from downloads_organizer.config import (
    Config,
    default_config_path,
    edit_config,
    init_config,
    load_config,
)

from .organizer import DownloadsOrganizer


def get_organizer(directory: Path) -> DownloadsOrganizer:
    directory = directory.expanduser()
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")

    if not directory.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    config = load_config()
    return DownloadsOrganizer(directory, config=config)


def truncate_filename(name: str, max_length: int = 45) -> str:
    """Shorten a filename in the middle without changing its extension."""
    if max_length <= 0 or len(name) <= max_length:
        return name

    suffix = Path(name).suffix
    available = max_length - len(suffix) - 3

    if available <= 0:
        return name[:max_length]

    left_length = available // 2
    right_length = available - left_length

    return f"{name[:left_length]}...{name[-right_length - len(suffix) : -len(suffix)]}{suffix}"


def handle_stats(directory: Path) -> None:
    """Display a summary of files in the selected directory."""
    organizer = get_organizer(directory)
    results = organizer.scan()

    category_counts: dict[str, int] = {}

    for result in results:
        category_counts[result.category] = category_counts.get(result.category, 0) + 1

    print()
    print("Downloads Organizer")
    print("===================")
    print()

    print("Directory")
    print(f"  {directory.expanduser().resolve()}")
    print()

    count = len(results)
    noun = "file" if count == 1 else "files"

    print("Summary")
    print(f"  {count} {noun}")
    print()

    if not results:
        print("Nothing to organize. Your Downloads folder is clean!")
        return

    print("Files by category")

    for category, count in sorted(category_counts.items()):
        folder = organizer.config.categories.get(category, category)
        print(f"  {folder:<15} {count}")

    print()
    print("Next steps")
    print("  Preview changes:   downloads-organizer organize --dry-run")
    print("  More information:  downloads-organizer organize -h")


def resolve_category(value: str, categories: dict[str, str]) -> str:
    """Resolve a user-provided category name to its internal category key."""
    normalized = value.strip().casefold()

    if normalized in categories:
        return normalized

    for key, folder in categories.items():
        if folder.casefold() == normalized:
            return key

    available = ", ".join(f"{key} ({folder})" for key, folder in categories.items())

    raise ValueError(
        f"Unknown category '{value}'. Available categories: {available}",
    )


def handle_organize(
    directory: Path,
    *,
    dry_run: bool,
    verbose: bool,
    only: str | None = None,
    clean_empty: bool = False,
) -> None:
    organizer = get_organizer(directory)

    if dry_run:
        move_results = organizer.plan_moves(only=only)
        empty_directories = (
            organizer.empty_category_directories(only=only) if clean_empty else []
        )
    else:
        move_results = organizer.organize(only=only)
        empty_directories = (
            organizer.clean_empty_category_directories(only=only) if clean_empty else []
        )

    if not move_results and not empty_directories:
        print("No files or folders to organize.")
        return

    if move_results:
        verb = "Would move" if dry_run else "Moved"
        count = len(move_results)
        noun = "file" if count == 1 else "files"
        print(f"{verb} {count} {noun}.")

    if empty_directories:
        verb = "Would remove" if dry_run else "Removed"
        count = len(empty_directories)
        noun = "directory" if count == 1 else "directories"
        print(f"{verb} {count} {noun}.")

    if verbose:
        groups: dict[Path, list[Path]] = {}

        for move in move_results:
            destination_folder = move.destination.relative_to(directory).parent
            groups.setdefault(destination_folder, []).append(move.source)

        no = 1
        print("Details:\n")

        if empty_directories:
            print("Directories to be removed:" if dry_run else "Removed directories:")
            for directory_path in empty_directories:
                print(f" {no:04d} - {directory_path.relative_to(directory)}")
                no += 1
            print()

        for destination_folder, sources in sorted(groups.items()):
            print(f'Files going into "{destination_folder}" folder:')

            for source in sources:
                print(
                    f" {no:04d} - {truncate_filename(source.name, organizer.config.truncate_length)}"
                )
                no += 1

        print()


def _insert_default_command(argv: list[str], commands: set[str]) -> list[str]:
    """Allow 'stats' to be omitted: bare dir/no-arg invocations imply 'stats'."""
    global_options = {"-h", "--help", "--version"}

    if argv and (argv[0] in commands or argv[0] in global_options):
        return argv

    return ["stats", *argv]


def handle_config(args: argparse.Namespace) -> None:
    """Handle configuration management commands."""
    config_path = default_config_path()

    if args.init:
        try:
            created_path = init_config()
        except FileExistsError as error:
            print(error)
            return

        print(f"Created configuration file:\n  {created_path}")
        return

    if args.edit:
        if not config_path.exists():
            try:
                init_config()
            except FileExistsError:
                pass

        print(f"Opening configuration:\n  {config_path}")
        edit_config(config_path)
        return

    if args.path:
        print(config_path)
        return

    if args.show:
        config = load_config(config_path)
        _print_config(config, config_path)
        return

    print(f"Configuration file:\n  {config_path}")


def _print_section(title: str) -> None:
    """Print a formatted section heading."""
    print(title)
    print("-" * len(title))


def _format_category_name(key: str, categories: dict[str, str]) -> str:
    """Return the configured folder name for a category key."""
    return categories.get(key, key.replace("_", " ").title())


def _print_mapping(
    mapping: dict[str, str],
    categories: dict[str, str],
) -> None:
    """Print classification rules as source-to-destination mappings."""
    if not mapping:
        print("  None configured.")
        return

    width = max(len(source) for source in mapping)

    for source, category in sorted(mapping.items()):
        folder = _format_category_name(category, categories)
        print(f"  {source:<{width}}  →  {folder}")


def _print_config(config: Config, config_path: Path) -> None:
    """Print the effective configuration in a human-readable format."""
    config_path = config_path.expanduser()
    config_exists = config_path.exists()

    print()
    title = "Downloads Organizer - Effective Configuration"
    print(title)
    print("=" * len(title))
    print()

    _print_section("Configuration")
    print(f"  Config file:        {config_path}")
    print(f"  Config file exists: {'Yes' if config_exists else 'No'}")

    if config_exists:
        print("  Configuration:     Built-in defaults + user overrides")
    else:
        print("  Configuration:     Built-in defaults (no config file found)")

    print()

    _print_section("General Settings")
    print(f"  Downloads directory: {config.downloads_directory}")
    print(f"  Filename truncation: {config.truncate_length} characters")
    print()

    _print_section("Categories")

    for key, folder in sorted(config.categories.items()):
        label = key.replace("_", " ").title()
        print(f"  {label:<18} →  {folder}")

    print()

    _print_section("Ignored Files")

    if config.ignored_files:
        for filename in sorted(config.ignored_files):
            print(f"  {filename}")
    else:
        print("  None configured.")

    print()

    _print_section("Ignored Directories")

    if config.ignored_directories:
        for directory in sorted(config.ignored_directories):
            print(f"  {directory}")
    else:
        print("  None configured.")

    print()

    _print_section("Classification Rules")

    rule_sections = (
        ("File Extensions", config.rules.extensions),
        ("Exact Filenames", config.rules.filenames),
        ("Glob Patterns", config.rules.patterns),
        ("Regular Expressions", config.rules.regex),
    )

    for title, mapping in rule_sections:
        print()
        print(f"{title}:")
        _print_mapping(mapping, config.categories)

    print()


def run() -> int:
    try:
        package_version = version("ae-dlo")
    except PackageNotFoundError:
        package_version = "unknown"

    config = load_config()
    parser = argparse.ArgumentParser(
        prog="downloads-organizer",
        description="Safely organize and manage any Downloads folder.",
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

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {package_version}",
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

    config_parser.add_argument(
        "--path",
        action="store_true",
        help="Show the configuration file path.",
    )

    config_parser.add_argument(
        "--show",
        action="store_true",
        help="Show the effective configuration (merged with defaults).",
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
        default=config.downloads_directory,
        help="Directory to organize (defaults to your Downloads folder.)",
    )

    organize_parser.add_argument(
        "--clean-empty",
        action="store_true",
        help="Remove empty category folders after organizing.",
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
            "Use either the category key or folder name. "
            "Available categories: "
            + ", ".join(
                f"{key} ({folder})" for key, folder in config.categories.items()
            )
        ),
    )

    commands = set(subparser.choices)
    argv = _insert_default_command(sys.argv[1:], commands)
    args = parser.parse_args(argv)

    try:
        if args.command == "stats":
            handle_stats(args.directory)

        elif args.command == "organize":
            only: str | None = None

            if args.only is not None:
                try:
                    only = resolve_category(args.only, config.categories)
                except ValueError as error:
                    parser.error(str(error))

            handle_organize(
                args.directory,
                dry_run=args.dry_run,
                verbose=args.verbose,
                only=only,
                clean_empty=args.clean_empty,
            )

        elif args.command == "config":
            handle_config(args)

    except (FileNotFoundError, NotADirectoryError) as error:
        print(error)
        return 1

    return 0
