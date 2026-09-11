<div align="center">

# 📂 Downloads Organizer

> **A lightweight, privacy-first Downloads folder organizer written in Python.**

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=for-the-badge)](#-quick-start)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline-success?style=for-the-badge)](#-why-no-ai)
[![Stars](https://img.shields.io/github/stars/a-endari/downloads-organizer?style=for-the-badge)](https://github.com/a-endari/downloads-organizer/stargazers)

[**Try it Now**](#-quick-start) • [**See It in Action**](#-how-it-looks-in-action) • [**Contribute**](#-contributing) • [**Report Issues**](https://github.com/a-endari/downloads-organizer/issues)

</div>

---

## 🎯 The Problem

Your Downloads folder is a digital junk drawer:

- 📄 Hundreds of PDFs, documents, and receipts
- 🖼️ Screenshots mixed with photos
- 💻 Code snippets alongside installers
- 📦 Archives and compressed files everywhere

You tell yourself: *"I'll organize this this weekend"*... and never do.

**Downloads Organizer solves this in one command.**

---

## ✨ Why Download This?

| Feature | Benefit |
|---------|---------|
| 🚀 **One Command** | `downloads-organizer organize` — that's it |
| 🔒 **100% Private** | No cloud, no telemetry, no AI hallucinations |
| ⚡ **Lightning Fast** | Runs in milliseconds, not seconds |
| 🎯 **Smart Sorting** | 9 intelligent categories + custom rules |
| 🍎 **macOS Native** | Treats `.app` bundles as single files |
| 📋 **Safe by Default** | `--dry-run` mode previews changes first |
| 🛡️ **Zero Dependencies** | Pure Python 3.13 standard library |
| 🤖 **No AI Nonsense** | Deterministic, predictable rules every time |

---

## 📂 How It Works

### Before

```text
Downloads/
├── quarterly_report.pdf
├── vacation_photo.png
├── installer.dmg
├── test_script.py
├── Archive_Files/
├── Slack.app
└── random_notes.txt
```

### One Command Later ⬇️

```bash
$ downloads-organizer organize
```

### After

```text
Downloads/
├── Documents/
│   ├── quarterly_report.pdf
│   └── random_notes.txt
├── Pictures/
│   └── vacation_photo.png
├── Programs/
│   ├── installer.dmg
│   └── Slack.app  ✨ Recognized as a macOS app!
├── Code/
│   └── test_script.py
└── Other Folders/
    └── Archive_Files/
```

**Your Downloads folder, organized.** No fluff, no confusion.

---

## 📊 What Gets Sorted

Downloads Organizer automatically categorizes files into 9 intelligent folders:

| Category | Folder | Common Files |
|----------|--------|--------------|
| 📄 | `Documents` | `.pdf`, `.doc`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.md`, `.csv` |
| 🖼️ | `Pictures` | `.jpg`, `.png`, `.webp`, `.gif`, `.heic`, `.avif`, `.svg` |
| 🎵 | `Audio` | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, `.ogg` |
| 🎬 | `Video` | `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`, `.m4v` |
| 💻 | `Code` | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.toml`, `.cpp`, `.rs` |
| ⚙️ | `Programs` | `.exe`, `.dmg`, `.pkg`, `.deb`, `.app`, `.msi`, `.apk` |
| 📦 | `Archives` | `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.bz2`, `.iso` |
| 📚 | `Ebooks` | `.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2` |
| 📁 | `Other Files` / `Other Folders` | Everything else |

---

## 🚀 Installation

### Option 1: From Source (Recommended for Development)

```bash
git clone https://github.com/a-endari/downloads-organizer.git
cd downloads-organizer
pip install -e .
```

### Option 2: Install from PyPI (Coming Soon)

```bash
pip install downloads-organizer
```

---

## 📖 Quick Start

### 1. **See what's in your Downloads**

```bash
downloads-organizer
```

Shows a summary of files ready to be organized.

### 2. **Preview the changes (Dry Run)**

```bash
downloads-organizer organize --dry-run
```

Displays what *would* move without actually moving anything.

### 3. **Run the organization**

```bash
downloads-organizer organize
```

Moves files into their categories.

### 4. **Organize specific categories only**

```bash
downloads-organizer organize --only Documents
downloads-organizer organize --only Code,Programs
```

### 5. **Get help**

```bash
downloads-organizer --help
```

---

## ⚙️ Configuration

Want custom rules? Create a `config.toml` in your config directory:

**Config File Locations:**
- **macOS/Linux:** `~/.config/downloads-organizer/config.toml`
- **Windows:** `%APPDATA%\downloads-organizer\config.toml`

**Example `config.toml`:**

```toml
[ignore]
# Files that should never be moved
files = [".DS_Store", "desktop.ini", ".gitkeep"]

# Directories that should stay put
directories = ["In_Progress", "Keep_Here", "Current_Projects"]
```

---

## 🔒 Privacy & Security

- ✅ **No network calls** — Everything happens offline on your machine
- ✅ **No telemetry** — Your file names never leave your computer
- ✅ **No cloud services** — No accounts, no logins, no tracking
- ✅ **Safe by default** — Always preview with `--dry-run` first
- ✅ **Open source** — Read the code, audit the logic

---

## 🤔 Why Not AI?

I *could* have built this with a machine learning model or cloud API. Instead, I chose **deterministic rules** because:

- ⚡ **Instant** — Runs in milliseconds, not seconds
- 🔒 **Private** — Your files never leave your computer
- 🎯 **Predictable** — `tax_return_2024.pdf` always goes to Documents
- 💰 **Free** — No API costs, no subscriptions, no hidden fees
- 🔁 **Reliable** — Rules don't hallucinate or change unpredictably

---

## 🛠️ Under the Hood

Built with engineering best practices:

- **Layered Architecture** — Clean separation between CLI, business logic, and system calls
- **Type-Safe** — Full type hints for IDE support and static analysis
- **Standard Library Only** — Zero runtime dependencies (just Python 3.13+)
- **Tested** — Comprehensive unit and integration tests
- **Conventional Commits** — Clean, readable Git history

See the [contributing guide](#-contributing) for architecture details.

---

## 🗺️ Roadmap

- [x] **Core Organization** — Fast file & folder categorization
- [x] **Safe Preview** — Non-destructive `--dry-run` mode
- [x] **Filtering** — Organize specific categories with `--only`
- [x] **Bundle Safety** — macOS `.app` bundle recognition
- [x] **Config System** — Custom ignore rules via TOML
- [ ] **Auto-Scheduler** — Background daemon for automatic organization
- [ ] **Duplicate Finder** — Detect and warn about duplicates
- [ ] **Interactive Mode** — Step-by-step `--interactive` prompts
- [ ] **Web Dashboard** — Visual organization stats and history

---

## 🤝 Contributing

We'd love your help! Whether you're fixing bugs, adding features, or improving docs:

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/a-endari/downloads-organizer.git
cd downloads-organizer
pip install -e ".[dev]"
pytest  # Run tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

Licensed under the **MIT License** — use it, fork it, modify it freely.

See the [LICENSE](LICENSE) file for details.

---

## 🎉 Show Your Support

If this tool saves you time or keeps your Downloads folder clean, consider:

- ⭐ **Star this repo** — It helps others discover it
- 🐛 **Report issues** — Found a bug? [Let us know](https://github.com/a-endari/downloads-organizer/issues)
- 💬 **Share feedback** — Ideas for improvements? [Start a discussion](https://github.com/a-endari/downloads-organizer/discussions)
- 📢 **Tell a friend** — Share it with colleagues who need an organized Downloads folder

---

## 💡 Pro Tips

- **Run regularly** — Add to your weekly habits or schedule with a cron job
- **Preview first** — Always use `--dry-run` on first run to verify behavior
- **Check config** — Review your ignore list to prevent important files from moving
- **Customize categories** — Modify the config to match your workflow

---

## 🎯 The Ultimate Vision

**Eventually, this tool will opinionatedly clean up your Downloads folder completely automatically in the background — without you ever noticing (or even having to permit it).**

Until then, one command per week keeps the chaos away. 🧹

---

<div align="center">

### Made with 💙 by [a-endari](https://github.com/a-endari)

[Star on GitHub](https://github.com/a-endari/downloads-organizer) • [Report Issue](https://github.com/a-endari/downloads-organizer/issues) • [Start Discussion](https://github.com/a-endari/downloads-organizer/discussions)

</div>
