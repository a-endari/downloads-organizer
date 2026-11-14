# Contributing to Downloads Organizer

Thank you for your interest in contributing!

## Development Setup

```bash
# Fork and clone
git clone https://github.com/a-endari/downloads-organizer
cd downloads-organizer

# Install in editable mode with dev dependencies
pipx install -e ".[dev]"
# or with pip inside a virtualenv:
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

To run with coverage report:

```bash
pytest --cov=downloads_organizer --cov-report=term-missing
```

## Running the Linter

```bash
ruff check .
ruff format .
```

To auto-fix issues:

```bash
ruff check --fix .
```

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix    | When to use                            |
|-----------|----------------------------------------|
| `feat:`   | New feature                            |
| `fix:`    | Bug fix                                |
| `docs:`   | Documentation changes only             |
| `chore:`  | Build process, dependencies, CI        |
| `test:`   | Adding or fixing tests                 |
| `refactor:` | Code change that neither fixes a bug nor adds a feature |

**Examples:**
```
feat: add support for .epub files
fix: handle unicode filenames on Linux
docs: update README installation steps
chore: bump ruff to 0.10
```

## Pull Request Process

1. Create a branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes and ensure tests pass (`pytest`) and linting is clean (`ruff check .`).

3. Commit following the conventions above.

4. Open a Pull Request against `main`.

5. A maintainer will review and merge.

## Making a Release

1. Update version in `pyproject.toml`:
   ```toml
   version = "X.Y.Z"
   ```

2. Add a new section in `CHANGELOG.md` following the existing format.

3. Commit:
   ```bash
   git commit -m "chore: bump version to vX.Y.Z"
   ```

4. Create an annotated tag:
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```

The `ci.yml` GitHub Actions workflow will automatically build and publish to TestPyPI (and PyPI once enabled).