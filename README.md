# Downloads Organizer

A modern Python command-line application for automatically organizing files in the Downloads folder.

The project is designed as a learning-focused portfolio application that demonstrates professional Python development practices, including package organization, filesystem operations, automation, testing, logging, and clean software architecture.

> **Status:** 🚧 Under active development

---

## Features

Current features

- Scan directories without modifying files
- Categorize files by extension
- Ignore operating system files (e.g. `.DS_Store`, `.localized`)
- Clean project architecture using the `src` layout
- Type hints throughout the codebase
- Dataclass-based models

Planned features

- Move files safely
- JSON configuration
- Dry-run mode
- Undo previous operations
- Duplicate detection
- Logging
- Automated scheduling
- Unit tests
- GitHub Actions CI

---

## Example

```text
$ python -m downloads_organizer

resume.pdf                     -> Documents
photo.jpg                      -> Pictures
movie.mp4                      -> Videos
archive.zip                    -> Archives
```

---

## Project Structure

```text
downloads-organizer/
├── config/
├── docs/
├── examples/
├── logs/
├── src/
├── tests/
└── README.md
```

---

## Technologies

- Python 3.13+
- pathlib
- dataclasses
- argparse
- logging
- shutil
- json

Only the Python standard library is used whenever possible.

---

## Roadmap

- [x] Project structure
- [x] Package layout
- [x] File categorization
- [x] Read-only scanning
- [ ] JSON configuration
- [ ] Safe file moving
- [ ] Logging
- [ ] Dry-run mode
- [ ] Undo support
- [ ] Unit tests
- [ ] Scheduled execution
- [ ] GitHub Actions

---

## License

MIT
