# 📂 Downloads Organizer

> A modern, cross-platform Python command-line application for safely cleaning up a cluttered Downloads folder.

Downloads Organizer is a Python CLI application that automatically organizes downloaded files into sensible categories
while preserving downloaded folders. Rather than acting as a general-purpose file manager, it focuses on solving one
problem well: turning a messy Downloads folder into a clean, organized workspace.

The project is also designed as a professional software engineering portfolio. Alongside practical functionality, it
demonstrates modern Python development practices, clean architecture, maintainable code, thoughtful CLI design, and an
incremental engineering workflow.

---

## 🎯 Project Philosophy

Downloads Organizer is intentionally opinionated.

Instead of becoming another file manager with hundreds of options, the project focuses on one task:

> **Clean up a cluttered Downloads folder safely, intelligently, and predictably.**

Whenever a new feature is considered, the first question is:

> **Does this directly improve the experience of organizing a Downloads folder?**

If the answer is "not really," the feature probably doesn't belong in this project.

This philosophy keeps the application focused, maintainable, and easy to understand.

---

## ✨ Current Features

### 📁 File Organization

- Organize both loose files and loose folders into categorized folders
- Automatic file categorization based on file extension
- Organize loose folders into the `Other Folders` category
- Safely treats macOS package directories (`.app`, `.bundle`, `.framework`) as single files
- Automatic creation of destination directories
- Safe collision handling
- Cross-platform filesystem support

### 📂 Built-in Categories

| Category | Folder Name | Common Extensions / Descriptions |
| --- | --- | --- |
| **Documents** | `Documents` | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.md`, `.csv`, `.pages` |
| **Pictures** | `Pictures` | `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.svg`, `.heic`, `.avif` |
| **Audio** | `Audio` | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, `.ogg` |
| **Video** | `Video` | `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`, `.m4v` |
| **Code** | `Code` | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.toml`, `.cpp`, `.rs` |
| **Programs** | `Programs` | `.exe`, `.dmg`, `.pkg`, `.deb`, `.msi`, `.apk`, `.appimage` |
| **Archives** | `Archives` | `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.bz2`, `.iso` |
| **Ebooks** | `Ebooks` | `.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2` |
| **Other Files** | `Other Files` | Files with unrecognized or rare extensions |
| **Other Folders** | `Other Folders` | Loose directories (excluding macOS package bundles) |

### 💻 Command Line Experience

- Modern `argparse` interface
- Helpful error messages
- Case-insensitive category names
- Filter organization by category
- Implicit `stats` default command
- Dry-run preview mode
- Verbose output

### 🛡 Safety

- Preview operations before moving files
- Strong typing throughout the application
- Uses `pathlib` for safe filesystem operations
- Designed around planning before execution

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/a-endari/downloads-organizer.git
cd downloads-organizer
```

Create and activate a virtual environment:

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project in editable mode:

```bash
pip install -e .
```

After installation you can use either command:

```bash
downloads-organizer
```

---

## 🖥 Usage

Show an overview of your Downloads folder.

```bash
downloads-organizer stats
# or simply:
downloads-organizer
```

Preview changes without moving any files:

```bash
downloads-organizer organize ~/Downloads --dry-run
```

Organize a Downloads folder:

```bash
downloads-organizer organize ~/Downloads
```

Organize only one category:

```bash
downloads-organizer organize ~/Downloads --only Documents
```

Enable verbose output:

```bash
downloads-organizer organize ~/Downloads --verbose
```

Category names are case-insensitive.

The following commands are equivalent:

```text
Documents
documents
DOCUMENTS
DoCuMeNtS
```

---

## 📸 Example

Before:

```text
Downloads/
├── report.pdf
├── holiday.jpg
├── setup.exe
├── archive.zip
├── script.py
├── notes.epub
└── IMG_847239.JPG
```

After:

```text
Downloads/
├── Documents/
│   └── report.pdf
├── Pictures/
│   ├── holiday.jpg
│   └── IMG_847239.JPG
├── Programs/
│   └── setup.exe
├── Archives/
│   └── archive.zip
├── Code/
│   └── script.py
└── Ebooks/
    └── notes.epub
```

---

## 📁 Project Structure

```text
downloads-organizer/
├── src/
│   └── downloads_organizer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── constants.py
│       ├── logger.py
│       ├── main.py
│       ├── models.py
│       ├── organizer.py
│       ├── rules.py
│       ├── scheduler.py
│       └── utils.py
├── tests/
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

As the project grows, new modules are introduced only when they have a clear responsibility. The codebase intentionally
avoids creating files "just in case" they might be needed later.

---

## 🏗 Architecture

The application follows a layered architecture to separate responsibilities and keep the business logic independent from
the command-line interface.

```text
CLI
│
├── organizer.py
├── models.py
├── config.py
└── pathlib/shutil
```

### Layer Responsibilities

| Layer                 | Responsibility                                                          |
| --------------------- | ----------------------------------------------------------------------- |
| **CLI**               | Parse command-line arguments, validate user input, and display results. |
| **Application Layer** | Connect the command-line interface to the business logic.               |
| **Business Logic**    | Scan files, categorize them, and perform organization.                  |
| **Models**            | Represent application data using dataclasses and enums.                 |
| **Filesystem**        | Interact safely with the operating system using `pathlib` and `shutil`. |

One important design principle is that **business logic never prints directly to the terminal**. Instead, it returns
structured data that any future interface (CLI, TUI, or GUI) can present.

---

## 💡 Design Decisions

This project intentionally emphasizes software engineering practices over simply producing a working script.

### Python Standard Library First

Whenever practical, the project relies on Python's standard library instead of third-party packages.

This keeps the application lightweight while demonstrating a solid understanding of Python itself.

External libraries will only be introduced when they provide significant value rather than replacing fundamental Python
knowledge.

---

### `pathlib`

Filesystem operations are implemented using `pathlib` instead of `os.path`.

Benefits include:

- Object-oriented paths
- Better readability
- Cross-platform compatibility
- Cleaner APIs for filesystem operations

---

### `StrEnum`

File categories are represented using Python's `StrEnum`.

Compared to plain strings, this provides:

- Type safety
- Better IDE autocompletion
- Easier refactoring
- Centralized validation
- Cleaner command-line parsing

---

### Type Hints

The project uses type hints throughout the codebase.

This improves:

- Readability
- Static analysis
- IDE support
- Refactoring safety
- Long-term maintainability

Although Python remains dynamically typed, type hints significantly improve the development experience for larger
projects.

---

### Small, Incremental Commits

Development follows a small-step workflow.

Rather than implementing large features all at once, functionality is introduced through small, focused commits using
the Conventional Commits specification.

This produces a clean Git history that documents the evolution of the project.

---

### Refactoring as a Feature

The project treats refactoring as a normal part of development rather than something postponed until the end.

Features that don't support the application's purpose are intentionally removed when a simpler design emerges.

For example, recursive organization was deliberately abandoned after it became clear that it pushed the application
toward becoming a general-purpose file manager instead of a focused Downloads cleanup tool.

---

### Clean Architecture

The project emphasizes separation of concerns.

Examples include:

- Separating command-line parsing from business logic.
- Separating planning from execution.
- Returning structured results instead of printing directly.
- Keeping functions small and focused.
- Giving each module a single responsibility.

These decisions make the project easier to maintain, test, and extend in the future.

---

## 🧠 Development Philosophy

The primary objective is not simply to move files.

The goal is to build software that demonstrates professional engineering practices while solving a real-world problem.

Whenever possible, the project favors:

- Simplicity over complexity
- Readability over cleverness
- Maintainability over premature optimization
- Focus over feature creep

Every architectural decision is evaluated by asking:

> **Does this make the application easier to understand, maintain, and extend?**

If not, the simpler solution is usually preferred.

---

## 🗺 Roadmap

Downloads Organizer is being developed incrementally, with each milestone introducing new concepts while maintaining a clean, stable codebase.

### ✅ Completed

- Project structure using the `src` layout
- Modern packaging with `pyproject.toml`
- Command-line interface using `argparse`
- Automatic file categorization
- Safe file organization
- Dry-run mode
- Category filtering
- Verbose output
- `StrEnum`-based categories
- Modern `pathlib` filesystem operations
- Configuration system

---

### 🚧 In Progress

- Ignore patterns
- Improved collision handling

---

### 🔮 Planned Features

#### Downloads Health Check

Analyze a Downloads folder before organizing it.

Planned checks include:

- Empty directories
- Missing file extensions
- Poorly named files
- Duplicate files (name + size)
- Duplicate files (hash comparison)

Rather than immediately moving files, the application will present recommendations and ask for confirmation before
making changes.

---

#### Interactive Workflow

- Yes / No prompts
- Yes to All
- Skip All
- `--accept-all-changes`
- `--no-changes`

This allows both interactive and fully automated workflows.

---

#### Configuration

- TOML configuration files
- Custom categories
- Ignore patterns
- User preferences

---

#### User Experience

- Rich terminal output
- Textual TUI
- Better summaries
- Improved error messages

---

#### Quality

- Unit tests
- Integration tests
- GitHub Actions
- Continuous Integration
- Automated releases

---

## 🤝 Contributing

Although this project is primarily a personal portfolio and learning project, suggestions, bug reports, and constructive feedback are always welcome.

---

## 📋 Requirements

- Python **3.13** or newer
- macOS, Linux, or Windows
- No required third-party runtime dependencies

Development tools currently include:

- Ruff
- Git
- GitHub

Additional development tools such as `pytest` and GitHub Actions will be introduced as the project evolves.

---

## 📚 What This Project Demonstrates

This project showcases practical software engineering skills including:

- Modern Python
- Clean Architecture
- Command-line application development
- Filesystem programming
- Object-oriented design
- Type hints
- Enumerations
- Dataclasses
- Packaging
- Professional Git workflow
- Documentation
- Incremental software design

The emphasis is not simply on writing code that works, but on building software that remains maintainable,
understandable, and enjoyable to extend.

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## ⭐ Final Notes

Downloads Organizer is intentionally being built as both a useful utility and a demonstration of professional Python
development practices.

Rather than adding every possible feature, the project focuses on solving one problem well while continuously improving
its architecture, code quality, and user experience.

If you find the project useful or interesting, consider giving it a ⭐ on GitHub.

Feedback, ideas, and constructive criticism are always appreciated.
