# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

This is a **Python project template** — a boilerplate repository to copy when starting new Python projects. It is not a functional library; the `TEMPLATE/` directory and all `TODO` markers are placeholders to be replaced.

Features provided: pixi-based environment management, pytest, ruff/mypy/dprint linting, lefthook pre-commit hooks, Sphinx docs, GitHub CI (multi-OS, multi-Python, noGIL stress tests, mindeps, upstream nightly), codecov.io, ReadTheDocs, hatchling versioning, and a PyPI/conda-forge release guide.

## Development Environment

Requires [pixi](https://pixi.sh/). All tasks are defined in `pyproject.toml` under `[tool.pixi.feature.*.tasks]`.

## Commands

```bash
# Testing
pixi run tests                    # Run pytest
pixi run tests-cov                # Tests + coverage.xml + terminal report
pixi run coverage                 # tests-cov + HTML report in htmlcov/
pixi run smoke-test               # Import test (verify the library loads)

# Single test
pixi run pytest TEMPLATE/tests/test_helloworld.py::test_hello -v

# Linting (ruff, mypy, dprint, actionlint, shellcheck, codespell, blacken-docs, sphinx-lint, validate-pyproject)
pixi run lint
pixi run install-git-hooks        # Install lefthook pre-commit hooks (run once)

# Documentation
pixi run docs                     # Build Sphinx docs to build/html/
pixi run doc-requirements         # Regenerate doc/requirements.yml for ReadTheDocs

# Distribution
pixi run dist                     # Clean + build sdist/wheel + twine check
pixi run twine-upload             # Upload to PyPI
```

`open-coverage` and `open-docs` tasks use the `open` command (macOS only); use `xdg-open` on Linux.

To skip pre-commit hooks on a specific commit: `git commit -n`.

## Pixi Environments

Defined in `[tool.pixi.environments]` in `pyproject.toml`:

| Environment      | Purpose                                                   |
| ---------------- | --------------------------------------------------------- |
| `default`        | Python 3.14, full features (docs + tests + ipython)       |
| `py311`, `py314` | Specific Python version testing                           |
| `mindeps`        | Python 3.11 with minimum supported dependency versions    |
| `upstream`       | Python 3.14 with nightly pre-releases (ignores pixi.lock) |
| `nogil`          | Free-threading stress tests with `pytest-run-parallel`    |
| `lint`           | Linting only                                              |
| `docs`           | Documentation building                                    |
| `dist`           | sdist/wheel building                                      |
| `smoke`          | Import-only test                                          |

Run a task in a specific environment: `pixi run -e py311 tests`

## Key Configuration

- **Versioning**: hatch-vcs derives `__version__` from git tags; fallback is `"9999"` for untagged installs
- **Pytest config**: `[tool.pytest.ini_options]` in `pyproject.toml`; strict mode, warnings as errors, `slow` marker available
- **Mypy**: strict mode for `TEMPLATE/`; test files exempt from `disallow_untyped_defs`
- **dprint**: formats JSON/YAML/TOML/Markdown; skips `pixi.lock`, `dist/`, `doc/requirements.yml`
- **CI**: `pytest.yml` runs 5 OS × 4 environments matrix + upstream + nogil; linting checks for changed files after auto-fix (`git diff --exit-code`)

## Release

See `HOW_TO_RELEASE` for the step-by-step PyPI and conda-forge release process.
