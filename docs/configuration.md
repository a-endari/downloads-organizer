# Configuration Guide

Downloads Organizer uses a TOML configuration file for customization. The application works out of the box with sensible defaults — you only need a config file if you want to change something.

---

## Config File Location

| Platform | Path |
|----------|------|
| **macOS / Linux** | `~/.config/downloads-organizer/config.toml` |
| **Windows** | `%APPDATA%\downloads-organizer\config.toml` |

### Quick Commands

```bash
# Create default config file (opens in your editor)
downloads-organizer config --init

# Open existing config in editor
downloads-organizer config --edit

# Show config file path
downloads-organizer config --path

# Show effective configuration (merged with defaults)
downloads-organizer config --show
```

---

## How Configuration Works

Configuration is **merged** with built-in defaults. You don't need to copy the entire default config — only specify what you want to change.

**Merge behavior:**
- Categories: your entries override/add to defaults
- Ignore rules: your entries are *added* to built-in ignore lists
- Rules: your rules take precedence over built-in rules (see [Rule Precedence](#rule-precedence))

---

## Complete Configuration Reference

### General Settings

```toml
[general]
# Default downloads directory when none provided to CLI
# ~ is expanded to your home directory
downloads_directory = "~/Downloads"

# Maximum filename length in verbose output (0 = no truncation)
truncate_length = 45
```

---

### Categories

Categories define where files are moved. Each category has:
- **Key** — internal stable name (used by rules)
- **Folder** — actual directory name created in Downloads

```toml
[categories.documents]
folder = "Documents"

[categories.pictures]
folder = "Pictures"

[categories.audio]
folder = "Audio"

[categories.video]
folder = "Video"

[categories.code]
folder = "Code"

[categories.programs]
folder = "Programs"

[categories.archives]
folder = "Compressed"

[categories.ebooks]
folder = "Ebooks"

[categories.other_files]
folder = "Other Files"

[categories.other_folders]
folder = "Other Folders"
```

#### Custom Categories

Add your own categories — then reference them in rules:

```toml
[categories.games]
folder = "Games"

[categories.work]
folder = "Work Documents"
```

#### Rename Built-in Folders

Change a folder name without changing rules:

```toml
[categories.documents]
folder = "My Documents"  # Rules still use "documents" key

[categories.audio]
folder = "Music & Audio"
```

---

### Ignore Rules

Files and directories listed here are **never organized**. Built-in ignored files are always included; these settings *add* to them.

```toml
[ignore]
# Exact filenames to ignore
files = [
    ".DS_Store",
    ".localized",
    "desktop.ini",
    "Thumbs.db",
    ".gitkeep",
]

# Directory names to ignore (matched anywhere in path)
directories = [
    "In_Progress",
    "Keep_Here",
    "Current_Projects",
    ".git",
    "node_modules",
    "__pycache__",
]
```

> **Note:** Built-in ignored files (`.DS_Store`, `desktop.ini`, `Thumbs.db`, `.localized`) are always ignored. You don't need to list them.

---

### Rules

Rules assign files to categories. The value on the right must be a valid category key (built-in or custom).

```toml
[rules.extensions]
# Extension rules (case-insensitive, include leading dot)
".torrent" = "archives"
".blend" = "code"
".log" = "documents"

[rules.filenames]
# Exact filename matches (highest precedence)
"README" = "code"
"Dockerfile" = "code"
"LICENSE" = "documents"

[rules.patterns]
# Glob patterns (*, ? wildcards)
"invoice-*.pdf" = "documents"
"IMG_*.jpg" = "pictures"
"*.tmp" = "other_files"

[rules.regex]
# Python regular expressions
"^backup_[0-9]{8}\.zip$" = "archives"
"^screenshot.*\.png$" = "pictures"
```

#### Rule Precedence

When multiple rules could match, the organizer evaluates in this order:

1. **Exact filename** (`[rules.filenames]`) — highest priority
2. **Regular expression** (`[rules.regex]`)
3. **Glob pattern** (`[rules.patterns]`)
4. **File extension** (`[rules.extensions]`)
5. **Built-in fallback** — lowest priority

This means specific rules override general ones:

```toml
[rules.extensions]
".pdf" = "documents"      # General rule

[rules.filenames]
"invoice.pdf" = "work"    # Overrides .pdf rule for this specific file
```

---

## Category Aliases

When writing rules, you can use plural aliases for built-in categories:

| Canonical Key | Aliases |
|---------------|---------|
| `documents` | `document`, `documents` |
| `pictures` | `picture`, `pictures`, `images`, `image` |
| `audio` | `audio`, `music`, `sounds` |
| `video` | `video`, `videos`, `movies` |
| `code` | `code`, `scripts`, `source` |
| `programs` | `program`, `programs`, `apps`, `applications`, `installers` |
| `archives` | `archive`, `archives`, `compressed` |
| `ebooks` | `ebook`, `ebooks`, `books` |
| `other_files` | `other`, `other_files`, `files` |
| `other_folders` | `other_folders`, `folders` |

These work regardless of what you name your folders in the config.

---

## Complete Example

```toml
[general]
downloads_directory = "~/Downloads"
truncate_length = 50

[categories.documents]
folder = "Documents"

[categories.pictures]
folder = "Photos"

[categories.video]
folder = "Videos"

[categories.code]
folder = "Code"

[categories.archives]
folder = "Archives"

# Custom category
[categories.games]
folder = "Games"

[categories.work]
folder = "Work"

[ignore]
files = [".gitkeep", "README.md"]
directories = ["In_Progress", "Keep_Here", ".git"]

[rules.extensions]
".torrent" = "archives"
".blend" = "code"
".unitypackage" = "games"
".godot" = "games"

[rules.filenames]
"README" = "code"
"Dockerfile" = "code"
"CHANGELOG.md" = "documents"

[rules.patterns]
"invoice-*.pdf" = "work"
"receipt-*.pdf" = "work"
"screenshot*.png" = "pictures"
"screenrecording*.mov" = "video"
"*.tmp" = "other_files"

[rules.regex]
"^backup_[0-9]{8}\.zip$" = "archives"
"^meeting_notes_[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$" = "work"
```

---

## Tips

### Test Your Config

```bash
# Preview what would happen with your config
downloads-organizer organize --dry-run

# See the effective merged configuration
downloads-organizer config --show
```

### Per-Project Configs

You can use a custom config file for a specific directory:

```bash
downloads-organizer organize --config /path/to/custom/config.toml ~/Downloads/ProjectA
```

### Reset to Defaults

Delete or rename your config file to use built-in defaults:

```bash
mv ~/.config/downloads-organizer/config.toml ~/.config/downloads-organizer/config.toml.bak
```

---

## Built-in Defaults Reference

For reference, here are the built-in extension rules (used when no config overrides them):

<details>
<summary>Click to expand</summary>

```python
DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".rtf",
    ".odt",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".md",
    ".csv",
    ".tex",
    ".bib",
    ".odp",
    ".ods",
}
EBOOK_EXTENSIONS = {".epub", ".mobi", ".azw", ".azw3", ".fb2", ".lit", ".lrf"}
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".webp",
    ".heic",
    ".avif",
    ".svg",
    ".ico",
}
VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mpg",
    ".mpeg",
    ".3gp",
}
AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".m4a",
    ".wma",
    ".opus",
    ".aiff",
    ".alac",
}
ARCHIVE_EXTENSIONS = {
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".iso",
    ".dmg",
    ".pkg",
    ".deb",
    ".rpm",
}
PROGRAM_EXTENSIONS = {
    ".exe",
    ".msi",
    ".app",
    ".dmg",
    ".pkg",
    ".deb",
    ".rpm",
    ".apk",
    ".appimage",
}
CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".xml",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".rs",
    ".go",
    ".java",
    ".kt",
    ".swift",
    ".php",
    ".rb",
    ".pl",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".ps1",
    ".sql",
    ".r",
    ".m",
    ".jl",
}
```
</details>

---

## Need Help?

- Run `downloads-organizer --help` for CLI options
- Check the [GitHub Discussions](https://github.com/a-endari/downloads-organizer/discussions) for questions
- Report bugs at [GitHub Issues](https://github.com/a-endari/downloads-organizer/issues)
