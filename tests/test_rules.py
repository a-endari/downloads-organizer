from pathlib import Path

import pytest
from downloads_organizer.models import Category
from downloads_organizer.rules import FileCategorizer


@pytest.fixture
def categorizer() -> FileCategorizer:
    return FileCategorizer()


@pytest.mark.parametrize(
    ("filename", "expected_category"),
    [
        ("report.pdf", Category.DOCUMENT.key),
        ("photo.jpg", Category.PICTURE.key),
        ("photo.JFIF", Category.PICTURE.key),
        ("song.mp3", Category.AUDIO.key),
        ("video.mp4", Category.VIDEO.key),
        ("script.py", Category.CODE.key),
        ("archiev.zip", Category.ARCHIVE.key),
        ("book.epub", Category.EBOOK.key),
        ("unknown.xyz", Category.OTHER.key),
    ],
)
def test_categorize_extension(
    categorizer: FileCategorizer,
    filename: str,
    expected_category: str,
) -> None:
    assert categorizer.get_category(Path(filename)) == expected_category


def test_categorize_without_extension(categorizer: FileCategorizer) -> None:
    assert categorizer.get_category(Path("README")) == Category.OTHER.key


def test_categorize_is_case_insensitive(categorizer: FileCategorizer) -> None:
    assert categorizer.get_category(Path("REPORT.PDF")) == Category.DOCUMENT.key
