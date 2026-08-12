from pathlib import Path

from downloads_organizer.config import Config
from downloads_organizer.organizer import DownloadsOrganizer


def test_ignored_file_is_not_moved(tmp_path: Path) -> None:
    source = tmp_path / ".DS_Store"
    source.write_text("test")

    config = Config(ignored_files={".DS_Store"})
    organizer = DownloadsOrganizer(tmp_path, config=config)

    organizer.organize()

    assert source.exists()
    assert not (tmp_path / "Other" / ".DS_Store").exists()


def test_ignored_directory_is_not_moved(tmp_path: Path) -> None:
    source = tmp_path / "__pycache__"
    source.mkdir()

    (source / "cache.pyc").write_text("test")

    config = Config(ignored_directories={"__pycache__"})
    organizer = DownloadsOrganizer(tmp_path, config=config)

    organizer.organize()

    assert source.is_dir()
    assert (source / "cache.pyc").exists()
    assert not (tmp_path / "Other Folders" / "__pycache__").exists()


def test_existing_category_directory_is_preserved(tmp_path: Path) -> None:
    documents = tmp_path / "Documents"
    documents.mkdir()

    existing_file = documents / "existing.pdf"
    existing_file.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    assert documents.is_dir()
    assert existing_file.exists()
    assert not (tmp_path / "Other Folders" / "Documents").exists()


def test_file_without_extension_goes_to_other(tmp_path: Path) -> None:
    source = tmp_path / "README"
    source.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    destination = tmp_path / "Other Files" / "README"

    assert destination.exists()
    assert not source.exists()


def test_unknown_extension_goes_to_other(tmp_path: Path) -> None:
    source = tmp_path / "something.xyz"
    source.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    destination = tmp_path / "Other Files" / "something.xyz"

    assert destination.exists()
    assert not source.exists()


def test_organize_file(tmp_path: Path) -> None:
    source = tmp_path / "report.pdf"
    source.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    assert not source.exists()
    assert (tmp_path / "Documents" / "report.pdf").exists()


def test_organize_folder(tmp_path: Path) -> None:
    source = tmp_path / "Some Folder"
    source.mkdir()

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    destination = tmp_path / "Other Folders" / "Some Folder"

    assert destination.is_dir()
    assert not source.exists()


def test_organize_folder_preserves_contents(tmp_path: Path) -> None:
    source = tmp_path / "Project"
    source.mkdir()

    file = source / "notes.txt"
    file.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    destination = tmp_path / "Other Folders" / "Project"

    assert not source.exists()
    assert (destination / "notes.txt").read_text() == "test"


def test_app_bundle_is_organized_as_file(tmp_path: Path) -> None:
    app = tmp_path / "ImageOptim.app"
    app.mkdir()

    contents = app / "Contents"
    contents.mkdir()

    (contents / "Info.plist").write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    destination = tmp_path / "Programs" / "ImageOptim.app"

    assert destination.is_dir()
    assert (destination / "Contents" / "Info.plist").exists()
    assert not app.exists()


def test_plan_moves_does_not_move_files(tmp_path: Path) -> None:
    source = tmp_path / "report.pdf"
    source.write_text("test")

    organizer = DownloadsOrganizer(tmp_path)

    moves = organizer.plan_moves()

    assert source.exists()
    assert len(moves) == 1


def test_duplicate_file_gets_renamed(tmp_path: Path) -> None:
    source = tmp_path / "report.pdf"
    source.write_text("new")

    documents = tmp_path / "Documents"
    documents.mkdir()
    existing = documents / "report.pdf"
    existing.write_text("old")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    assert existing.read_text() == "old"
    assert (documents / "report (1).pdf").exists()


def test_organize_multiple_files(tmp_path: Path) -> None:
    (tmp_path / "report.pdf").write_text("pdf")
    (tmp_path / "photo.jpg").write_text("jpg")
    (tmp_path / "song.mp3").write_text("mp3")

    organizer = DownloadsOrganizer(tmp_path)

    organizer.organize()

    assert (tmp_path / "Documents" / "report.pdf").exists()
    assert (tmp_path / "Pictures" / "photo.jpg").exists()
    assert (tmp_path / "Audio" / "song.mp3").exists()
