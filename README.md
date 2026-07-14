# 📂 Downloads Organizer

A modern, cross-platform Python command-line application for organizing downloaded files into categorized folders.

The project is built as a software engineering portfolio piece, emphasizing clean architecture, modern Python practices,
strong typing, and maintainable code rather than simply moving files.

---

## ✨ Features

### File Organization

- Organize files into categorized folders
- Built-in categories:
    - Documents
    - Pictures
    - Audio
    - Video
    - Code
    - Programs
    - Archives
    - Other
- Category filtering with `--only`
- Case-insensitive category names
- Automatic creation of destination folders

### Safety

- Dry-run mode (`--dry-run`)
- Scan directories without modifying files
- Uses `pathlib` for safe cross-platform path handling

### Statistics

- Scan a directory without moving files
- Display per-category statistics
- Count files before organizing

### Command Line Interface

- Modern `argparse` interface
- Helpful error messages
- Strongly typed category parsing
- Verbose output (`--verbose`)

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-name>/downloads-organizer.git
cd downloads-organizer
```

Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project

```bash
pip install -e .
```

---

## 🖥 Usage

Scan a directory

```bash
downloads-organizer scan ~/Downloads
```

Display statistics

```bash
downloads-organizer stats ~/Downloads
```

Organize files

```bash
downloads-organizer organize ~/Downloads
```

Preview changes without moving files

```bash
downloads-organizer organize ~/Downloads --dry-run
```

Organize only documents

```bash
downloads-organizer organize ~/Downloads --only Documents
```

Category names are case-insensitive.

These are equivalent:

```text
Documents
documents
DOCUMENTS
DoCuMeNtS
```

---

## 📁 Project Structure

```
downloads-organizer/
│
├── src/
│   └── downloads_organizer/
│       ├── cli.py
│       ├── models.py
│       ├── organizer.py
│       ├── rules.py
│       ├── statistics.py
│       └── __main__.py
│
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

### Module Overview

| Module          | Responsibility                              |
|-----------------|---------------------------------------------|
| `cli.py`        | Command-line interface and argument parsing |
| `models.py`     | Domain models, dataclasses, and enums       |
| `organizer.py`  | Core organization logic                     |
| `rules.py`      | File extension to category mapping          |
| `statistics.py` | Directory statistics                        |

---

## 🏗 Design Decisions

This project intentionally emphasizes software engineering practices.

### `pathlib`

Uses `pathlib` instead of `os.path` for modern, object-oriented filesystem operations.

### `dataclasses`

Uses dataclasses to reduce boilerplate while keeping models explicit and type-safe.

### `StrEnum`

Categories are represented using `StrEnum` instead of plain strings, providing:

- Better IDE support
- Type safety
- Easier refactoring
- Cleaner business logic

### Type Hints

The project uses type hints throughout to improve readability, maintainability, and static analysis.

### Minimal Dependencies

The project currently relies almost entirely on Python's standard library to demonstrate how much can be achieved
without external packages.

---

## 📋 Roadmap

### Completed

- [x] Scan command
- [x] Statistics command
- [x] Organize command
- [x] Dry-run mode
- [x] Verbose mode
- [x] Category filtering
- [x] `StrEnum` category model
- [x] Case-insensitive category parsing

### Planned

- [ ] Duplicate detection
- [ ] Recursive directory organization
- [ ] Ignore patterns
- [ ] Configuration file (TOML)
- [ ] Custom categories
- [ ] Rich terminal output
- [ ] Progress bars
- [ ] Undo support
- [ ] Logging
- [ ] Unit tests
- [ ] Continuous Integration (GitHub Actions)

---

## 🧪 Requirements

- Python 3.13+
- Windows
- macOS
- Linux

---

## 📄 License

This project is licensed under the MIT License.