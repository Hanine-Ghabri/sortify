# file-sorter

A tiny command-line tool that organizes a messy folder (hello, Downloads) into
subfolders like `Images/`, `Documents/`, and `Archives/` based on file type.

## Features
- Sorts by extension into 8 categories, plus `Other`
- `--dry-run` previews changes before touching anything
- Never overwrites: name clashes become `report (1).pdf`
- Skips hidden files and subfolders
- Zero dependencies (Python 3.9+ standard library only)

## Usage
```bash
python file_sorter.py ~/Downloads --dry-run   # preview
python file_sorter.py ~/Downloads             # do it
```

Example output:
```
Would move: vacation.jpg -> Images/vacation.jpg
Would move: invoice.pdf -> Documents/invoice.pdf

2 file(s) planned.
```

## Customize
Edit the `CATEGORIES` dictionary at the top of `file_sorter.py` to add
extensions or new categories.

## Tests
```bash
pip install pytest
pytest
```

## License
MIT
