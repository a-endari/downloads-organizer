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
        ("report.pdf", Category.DOCUMENT),
        ("photo.jpg", Category.PICTURE),
        ("photo.JFIF", Category.PICTURE),
        ("song.mp3", Category.AUDIO),
        ("video.mp4", Category.VIDEO),
        ("script.py", Category.CODE),
        ("archiev.zip", Category.ARCHIVE),
        ("book.epub", Category.EBOOK),
        ("unknown.xyz", Category.OTHER),
    ],
)
def test_categorize_extension(
    categorizer: FileCategorizer,
    filename: str,
    expected_category: Category,
) -> None:
    assert categorizer.get_category(Path(filename)) == expected_category


def test_categorize_without_extension(categorizer: FileCategorizer) -> None:
    assert categorizer.get_category(Path("README")) == Category.OTHER


def test_categorize_is_case_insensitive(categorizer: FileCategorizer) -> None:
    assert categorizer.get_category(Path("REPORT.PDF")) == Category.DOCUMENT
