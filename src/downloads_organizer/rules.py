from pathlib import Path

from .models import Category


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
        "jfif",
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

    DEFAULT_RULES = {
        extension: category
        for category, extensions in CATEGORY_EXTENSIONS.items()
        for extension in extensions
    }

    def __init__(self, rules: dict[str, Category] | None = None) -> None:
        self.rules = rules or self.DEFAULT_RULES

    def get_category(self, file_path: Path) -> Category:
        """
        Return the destination category for a file.

        Unknown extensions are placed in 'Other'.
        """
        extension = file_path.suffix.lower()
        return self.rules.get(extension, Category.OTHER)


# Directory types that should be treated as files.
PACKAGE_EXTENSIONS = {
    ".app",
    ".bundle",
    ".framework",
}
