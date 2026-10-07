from pathlib import Path

import pytest

from file_sorter import category_for, sort_folder, unique_destination


def test_category_for_known_and_unknown():
    assert category_for(Path("photo.JPG")) == "Images"
    assert category_for(Path("notes.txt")) == "Documents"
    assert category_for(Path("mystery.xyz")) == "Other"


def test_sort_moves_files(tmp_path):
    (tmp_path / "a.png").write_text("x")
    (tmp_path / "b.pdf").write_text("x")
    sort_folder(tmp_path)
    assert (tmp_path / "Images" / "a.png").exists()
    assert (tmp_path / "Documents" / "b.pdf").exists()


def test_dry_run_changes_nothing(tmp_path):
    (tmp_path / "a.png").write_text("x")
    moves = sort_folder(tmp_path, dry_run=True)
    assert len(moves) == 1
    assert (tmp_path / "a.png").exists()
    assert not (tmp_path / "Images").exists()


def test_no_overwrite(tmp_path):
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "a.png").write_text("old")
    (tmp_path / "a.png").write_text("new")
    sort_folder(tmp_path)
    assert (tmp_path / "Images" / "a.png").read_text() == "old"
    assert (tmp_path / "Images" / "a (1).png").read_text() == "new"


def test_hidden_files_skipped(tmp_path):
    (tmp_path / ".hidden").write_text("x")
    assert sort_folder(tmp_path) == []


def test_not_a_directory(tmp_path):
    with pytest.raises(NotADirectoryError):
        sort_folder(tmp_path / "missing")


def test_unique_destination(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("1")
    assert unique_destination(f).name == "x (1).txt"
