<div align="center">

# 📂 Downloads Organizer

> **A lightweight, privacy-first Downloads folder organizer written in Python.**

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=for-the-badge)](#-quick-start)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline-success?style=for-the-badge)](#-why-no-ai)

</div>

---

> [!IMPORTANT]
> ### 🔮 The Ultimate Goal
> **Eventually, this tool will opinionatedly clean up your Downloads folder completely automatically in the background—without you ever noticing *(or even having to permit it 😏)*.**  
> *(Work in progress!)*

Let’s be honest: the Downloads folder is usually where files go to get forgotten. 

Every few weeks, I’d open mine, see hundreds of loose PDFs, screenshots, installer `.dmg`s, and random code snippets, tell myself *"I'll clean this up this weekend,"* and promptly close the window.

Eventually, I got tired of doing archaeological digs just to find a receipt from last Tuesday. So I wrote **Downloads Organizer** to quietly handle it for me.

* **No cloud services.**  
* **No AI hype.**  
* **No API keys or background telemetry.**  
* **Just simple, deterministic Python.**

---

## ✨ Why I Built This

There are plenty of file management scripts out there, but most of them either try to do way too much or force you to spend 20 minutes setting up complex rules.

I wanted something simple with one clear goal:

> **Keep my Downloads folder clean without getting in my way.**

My long-term goal for this tool is lazy perfection: **install it once, forget it exists, and always have an organized folder when I open it.**

---

## 🎯 How I Designed It

I built this around a few core principles I care about:

- 🎯 **Single-minded** — It cleans `~/Downloads`. It won't touch the rest of your system.
- ⚡ **Predictable** — A PDF goes to `Documents/` every single time. No surprises.
- 🔒 **Private & Offline** — Everything stays on your machine. Zero network calls.
- 🪶 **Zero Dependencies** — Runs entirely on Python's standard library. No massive third-party packages.
- 🛡️ **Mac Package Safety** — Smart enough to treat macOS `.app`, `.bundle`, and `.framework` directories as single files and organize `.app` bundles cleanly into `Programs/`!
- 🤫 **Quiet** — It does its job and gets out of your way.

> [!NOTE]
> **Mac Package Support**: macOS `.app`, `.bundle`, and `.framework` directories are recognized as single file units. `.app` bundles are categorized directly into `Programs/` without disassembling their internal contents.

---

## 🚫 Why Not AI?

Lately, it feels like every CLI tool comes with a cloud API key or a local LLM attached to it. 

I didn't want to wait 3 seconds for an LLM to decide if `tax_return_2024.pdf` belongs in a folder named `Documents`. 

> [!TIP]
> **Why Deterministic Rule-Based Sorting Wins:**
> - ⚡ **Instant** — Runs in milliseconds.
> - 🔒 **Private** — Your personal file names never leave your computer.
> - 🔁 **Reliable** — It doesn't hallucinate or decide to rename your folders on a whim.
> - 💰 **Free** — No API credits, no subscriptions.

---

## 📂 Built-in Categories

Here's where your files automatically land:

| Category | Folder Name | Common Extensions / Descriptions |
| :--- | :--- | :--- |
| 📄 **Documents** | `Documents` | `.pdf`, `.doc`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.md`, `.csv`, `.pages` |
| 🖼️ **Pictures** | `Pictures` | `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.svg`, `.heic`, `.avif` |
| 🎵 **Audio** | `Audio` | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, `.ogg` |
| 🎬 **Video** | `Video` | `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`, `.m4v` |
| 💻 **Code** | `Code` | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.toml`, `.cpp`, `.rs` |
| ⚙️ **Programs** | `Programs` | `.exe`, `.dmg`, `.pkg`, `.deb`, `.app`, `.msi`, `.apk`, `.appimage` |
| 📦 **Archives** | `Archives` | `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.bz2`, `.iso` |
| 📚 **Ebooks** | `Ebooks` | `.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2` |
| 📁 **Other Files** | `Other Files` | Files with unrecognized or rare extensions |
| 📂 **Other Folders** | `Other Folders` | Loose directories (excluding macOS package bundles) |

---

## 📸 How It Looks in Action

### Before

```text
Downloads/
├── quarterly_report.pdf
├── photo.png
├── installer.dmg
├── test_script.py
├── UnsortedFolder/
└── Slack.app
```

⬇️ **`downloads-organizer organize`**

### After

```text
Downloads/
├── Documents/
│   └── quarterly_report.pdf
├── Pictures/
│   └── photo.png
├── Programs/
│   ├── installer.dmg
│   └── Slack.app              <-- Categorized as a Program!
├── Code/
│   └── test_script.py
└── Other Folders/
    └── UnsortedFolder/
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/a-endari/downloads-organizer.git
cd downloads-organizer

# 2. Install locally
pip install -e .

# 3. See what's sitting in your Downloads folder right now
downloads-organizer

# 4. Preview what will move without touching anything (Dry Run)
downloads-organizer organize --dry-run

# 5. Run the actual organization
downloads-organizer organize

# 6. Or just clean up one specific category
downloads-organizer organize --only Documents
```

---

## ⚙️ Custom Configuration

It works out of the box with reasonable defaults. If you want custom rules, you can drop a simple `config.toml` into your system config directory:

| OS | Configuration File Path |
| :--- | :--- |
| **macOS** | `~/.config/downloads-organizer/config.toml` |
| **Linux** | `~/.config/downloads-organizer/config.toml` |
| **Windows** | `%APPDATA%\downloads-organizer\config.toml` |

Example `config.toml`:

```toml
[ignore]
# Files or directories you don't want moved
files = [".DS_Store", "desktop.ini"]
directories = ["In_Progress", "Keep_Here"]
```

---

## 🗺️ Roadmap

- [x] **Core Organization** — Fast file & folder categorization
- [x] **Safe Preview** — Non-destructive `--dry-run` mode
- [x] **Filtering** — Case-insensitive category filtering (`--only`)
- [x] **Bundle Safety** — macOS `.app` bundle recognition & program categorization
- [x] **Config System** — Custom TOML ignore lists for files & directories
- [ ] **Auto-Scheduler** — Background organization daemon
- [ ] **Duplicate Finder** — Detection & warning for duplicate downloads
- [ ] **Interactive Mode** — Step-by-step `--interactive` prompts

---

<details>
<summary>🛠️ <b>Under the Hood (For Fellow Nerds)</b> — <i>Click to expand</i></summary>

<br>

Even though I made this lightweight for everyday use, I built it with strict engineering standards:

* **Layered Architecture**: Decoupled CLI input parsing from organization logic and system calls.
* **Standard Library First**: Built with pure Python 3.13 (`pathlib`, `StrEnum`, `dataclasses`) with zero runtime dependencies.
* **Fully Typed**: Annotated with type hints for cleaner IDE support and static analysis.
* **Conventional Commits**: Clean Git history following standard commit conventions.

</details>

---

## 📄 License

Licensed under the **MIT License**. Feel free to use it, fork it, or adapt it however you like.

---

## ⭐ Wrapping Up

I wrote this utility because I believe the best software is the software you don't have to think about. 

If this saves you a bit of manual file dragging or keeps your workspace feeling clean, drop a ⭐ on GitHub—it's always appreciated!
