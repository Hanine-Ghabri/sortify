#!/usr/bin/env python3
"""file-sorter: organize a messy folder into subfolders by file type."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".key", ".odp"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a"},
    "Video": {".mp4", ".mov", ".mkv", ".avi", ".webm"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".sh", ".java", ".c", ".cpp"},
}


def category_for(path: Path) -> str:
    """Return the category folder name for a file, based on its extension."""
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return "Other"


def unique_destination(dest: Path) -> Path:
    """Avoid overwriting: report.pdf -> report (1).pdf -> report (2).pdf ..."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def sort_folder(folder: Path, dry_run: bool = False) -> list[tuple[Path, Path]]:
    """Move files in `folder` into category subfolders. Returns the planned moves."""
    if not folder.is_dir():
        raise NotADirectoryError(f"{folder} is not a directory")

    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        target_dir = folder / category_for(item)
        dest = unique_destination(target_dir / item.name)
        moves.append((item, dest))
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
    return moves


def main() -> None:
    parser = argparse.ArgumentParser(description="Sort files into folders by type.")
    parser.add_argument("folder", type=Path, help="folder to organize")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="show what would happen without moving anything")
    args = parser.parse_args()

    moves = sort_folder(args.folder, dry_run=args.dry_run)
    verb = "Would move" if args.dry_run else "Moved"
    for src, dest in moves:
        print(f"{verb}: {src.name} -> {dest.parent.name}/{dest.name}")
    print(f"\n{len(moves)} file(s) {'planned' if args.dry_run else 'organized'}.")


if __name__ == "__main__":
    main()
