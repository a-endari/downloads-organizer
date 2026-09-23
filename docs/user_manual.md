# 📂 Downloads Organizer: Comprehensive User Manual

Welcome to the official manual for **Downloads Organizer**, a lightweight, high-performance, privacy-first command-line utility designed to clean up and structure your `Downloads` directory automatically.

---

## 1. Architecture & Design Principles

Downloads Organizer is engineered around absolute reliability, transparency, and speed:

- **Zero Dependencies:** Built exclusively on Python’s standard library (`shutil`, `pathlib`, `argparse`, `tomllib`, etc.), requiring no heavy third-party packages.
- **Deterministic Rules:** Uses explicit rules (extensions, exact names, glob patterns, and regular expressions) rather than unpredictable heuristics.
- **100% Offline & Private:** Zero network telemetry or cloud API dependencies; all file operations execute locally on your machine.
- **Bundle-Aware:** Automatically treats system directory packages (such as macOS `.app`, `.bundle`, or `.framework`) as single files rather than treating them as folders to be unpacked or sorted internally.

---

## 2. Installation & Requirements

### Requirements

- **Python Version:** Python 3.13 or higher.
- **Operating Systems:** macOS, Linux, and Windows.

### Installation Steps

Clone the repository and install it locally in editable mode:

```bash
git clone [https://github.com/a-endari/downloads-organizer.git](https://github.com/a-endari/downloads-organizer.git)
cd downloads-organizer
pip install -e .

```

---

## 3. Command-Line Interface (CLI) Reference

The core command structure follows:

```bash
downloads-organizer [command] [directory] [options]

```

(Note: If you run `downloads-organizer` with a directory path or no arguments at all, it implicitly defaults to the `stats` command).

### Commands

#### `stats [directory]`

Analyzes the target directory, aggregates file counts by category, and prints a summary breakdown without making any disk modifications.

- **Default Directory:** `~/Downloads` (or whatever `downloads_directory` is set to in your config).

#### `organize [directory] [options]`

Scans the target directory, evaluates rules, calculates destination paths, handles filename collision increments, and executes the file moves.

**Available Flags & Options:**

- `--dry-run`: Simulates the organization process, printing what _would_ happen without altering any files or folders.

- `-v`, `--verbose`: Displays detailed, numbered logs of every file and removed directory being processed, grouped by destination folder and truncated cleanly if filenames exceed `truncate_length`.

- `--only <category>`: Limits the operation or empty directory cleanup to a single specified category (accepts either the stable internal category key like `ebook` or the display folder name like `Ebooks`).

- `--clean-empty`: Cleans up empty category directories post-organization (or during a dry-run preview) while respecting `--only` filters.

#### `config [options]`

Manages configuration file generation and editing.

- `-I`, `--init`: Copies the default template configuration into your system's appropriate config directory.

- `-e`, `--edit`: Automatically locates or initializes your `config.toml` and opens it in your preferred editor (`EDITOR` environment variable, falling back to `nvim`, `vim`, `nano`, `code`, or `notepad`).

---

## 4. Default Categories & File Classification

Files and directories found directly inside your download root are classified into standard categories:

| Internal Category Key | Default Folder Name | Handled File Types / Descriptions                                           |
| --------------------- | ------------------- | --------------------------------------------------------------------------- |
| `documents`           | `Documents`         | `.pdf`, `.doc`, `.docx`, `.txt`, `.xlsx`, `.pptx`, `.md`, `.csv`, etc.      |
| `pictures`            | `Pictures`          | `.jpg`, `.png`, `.webp`, `.gif`, `.heic`, `.avif`, `.svg`, etc.             |
| `audio`               | `Music`             | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, `.ogg`, etc.                       |
| `video`               | `Videos`            | `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`, `.m4v`, etc.                       |
| `code`                | `Code Files`        | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.toml`, `.cpp`, `.rs`, etc. |
| `programs`            | `Programs`          | `.exe`, `.dmg`, `.pkg`, `.deb`, `.app`, `.msi`, `.apk`, etc.                |
| `archives`            | `Archives`          | `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.bz2`, `.iso`, etc.                  |
| `ebooks`              | `Ebooks`            | `.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2`, etc.                             |
| `other_files`         | `Other Files`       | Fallback category for loose files matching no specific rules                |
| `other_folders`       | `Other Folders`     | Fallback category for unexpected subdirectories                             |

---

## 5. Configuration, Custom Rules, & Precedence

You can fully customize categories, rules, and ignore lists by editing your local `config.toml` file.

### Configuration Paths

- **macOS / Linux:** `~/.config/downloads-organizer/config.toml`

- **Windows:** `%APPDATA%\downloads-organizer\config.toml`

### Rule Evaluation Precedence

When multiple matching rules conflict, the engine evaluates them in strict order of specificity (highest priority first):

1. **Exact Filename Rules** (`[rules.filenames]`)

2. **Regular Expression Rules** (`[rules.regex]`)

3. **Glob / Pattern Rules** (`[rules.patterns]`)

4. **File Extension Rules** (`[rules.extensions]`)

5. **Fallback Default** (`other_files` / `other_folders`)

### Collision Handling

If a destination file already exists with the same name, Downloads Organizer safely avoids overwriting it by appending an incremental numeric counter suffix (e.g., `document (1).pdf`, `document (2).pdf`).

### Default Ignored Files & Directories

Certain operating system artifacts are ignored automatically to prevent cluttering or corruption:

- **macOS:** `.DS_Store`, `.localized`

- **Windows:** `desktop.ini`, `Thumbs.db`

You can add custom files or directories to skip inside the `[ignore]` block of your configuration.

```toml
[ignore]
files = [".DS_Store", "custom-lock.lock"]
directories = ["ActiveProjects", "DoNotTouch"]

```

---

## 6. Example Configuration File (`config.toml`)

```toml
[general]
downloads_directory = "~/Downloads"
truncate_length = 45

[categories.games]
folder = "Games"

[ignore]
files = [".DS_Store", "desktop.ini"]
directories = ["KeepSafe"]

[rules.extensions]
".game" = "games"

[rules.filenames]
"README" = "code"

[rules.patterns]
"invoice-*.pdf" = "documents"

[rules.regex]
"^IMG_[0-9]{4,6}\\.jpg$" = "pictures"

```
