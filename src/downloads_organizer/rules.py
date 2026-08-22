import re
from fnmatch import fnmatch
from pathlib import Path

from .config import RulesConfig
from .models import Category


def _build_default_rules(
    category_extensions: dict[Category, set[str]],
) -> dict[str, str]:
    """Flatten category->extensions into extension->category, erroring on overlap."""
    rules: dict[str, str] = {}
    for category, extensions in category_extensions.items():
        for extension in extensions:
            if extension in rules:
                raise ValueError(
                    f"Extension '{extension}' is assigned to both "
                    f"{rules[extension]!r} and {category.key!r}."
                )
            rules[extension] = category.key
    return rules


class FileCategorizer:
    """Determine the category of a file based on its extension."""

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".odt",
        ".rtf",
        ".txt",
        ".md",
        ".tex",
        ".pages",
        ".csv",
        ".tsv",
        ".xls",
        ".xlsx",
        ".ods",
        ".ppt",
        ".djvu",
        ".pptx",
        ".key",
    }

    EBOOK_EXTENSIONS = {
        ".epub",
        ".mobi",
        ".azw",
        ".azw3",
        ".fb2",
    }

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
        ".bmp",
        ".svg",
        ".tif",
        ".tiff",
        ".jfif",
        ".heic",
        ".heif",
        ".avif",
        ".ico",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".mkv",
        ".mov",
        ".avi",
        ".wmv",
        ".webm",
        ".m4v",
        ".flv",
    }

    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
        ".m4a",
        ".wma",
    }

    ARCHIVE_EXTENSIONS = {
        ".zip",
        ".tbz2",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".tgz",
        ".iso",
    }

    PROGRAM_EXTENSIONS = {
        ".exe",
        ".msi",
        ".dmg",
        ".pkg",
        ".app",
        ".apk",
        ".deb",
        ".rpm",
        ".appimage",
    }

    CODE_EXTENSIONS = {
        ".py",
        ".ipynb",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".html",
        ".css",
        ".java",
        ".kt",
        ".swift",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".rb",
        ".sql",
        ".sh",
        ".zsh",
        ".ps1",
        ".bat",
        ".cmd",
        ".json",
        ".toml",
        ".yaml",
        ".yml",
        ".xml",
        ".ini",
        ".cfg",
    }

    CATEGORY_EXTENSIONS = {
        Category.DOCUMENT: DOCUMENT_EXTENSIONS,
        Category.EBOOK: EBOOK_EXTENSIONS,
        Category.PICTURE: IMAGE_EXTENSIONS,
        Category.VIDEO: VIDEO_EXTENSIONS,
        Category.AUDIO: AUDIO_EXTENSIONS,
        Category.ARCHIVE: ARCHIVE_EXTENSIONS,
        Category.PROGRAM: PROGRAM_EXTENSIONS,
        Category.CODE: CODE_EXTENSIONS,
    }

    DEFAULT_RULES = _build_default_rules(CATEGORY_EXTENSIONS)

    def __init__(self, rules: RulesConfig | None = None) -> None:
        self.rules = RulesConfig() if rules is None else rules

        self.extensions = self.DEFAULT_RULES | {
            extension.lower(): category for extension, category in self.rules.extensions.items()
        }

        self._compiled_regex: list[tuple[re.Pattern[str], str]] = [
            (re.compile(pattern), category) for pattern, category in self.rules.regex.items()
        ]

    def get_category(self, file_path: Path) -> str:
        """
        Return the destination category for a file.

        Rules are checked in order of specificity: exact filename match,
        regex match, glob pattern match, extension match, falling back to
        Category.OTHER when nothing matches.
        """
        name = file_path.name

        if name in self.rules.filenames:
            return self.rules.filenames[name]

        for regex, category in self._compiled_regex:
            if regex.search(name):
                return category

        for pattern, category in self.rules.patterns.items():
            if fnmatch(name, pattern):
                return category

        extension = file_path.suffix.lower()
        return self.extensions.get(extension, Category.OTHER.key)


# Directory types that should be treated as files.
PACKAGE_EXTENSIONS = {
    ".app",
    ".bundle",
    ".framework",
}
