# Development Guide

This document is for developers who want to contribute to `anxiety` or run it from source for development purposes.

## 🛠️ Setup

### 1. Prerequisites

- **Python 3.14+**
- [**uv**](https://github.com/astral-sh/uv): Fast Python package management.

### 2. Clone the repository

```bash
git clone https://github.com/esteban03/anxiety.git
cd anxiety
```

### 3. Install core dependencies

```bash
uv sync
```

## 🚀 Running for Development

### Option A: Use `uv run` (Isolated)

Good for quick tests and ensuring you are using the project's exact lockfile.

```bash
uv run anxiety --help
```

### Option B: Editable Installation (Global Command)

The best way to develop. This installs the `anxiety` command globally but points to your local source code. Changes in the code are reflected immediately.

```bash
uv tool install --editable .
```

After this, you can run `anxiety` from anywhere in your terminal.

## 🧪 Testing

We use `pytest` for testing.

```bash
uv run pytest
```

## 🧹 Linting and Formatting

This project uses `ruff` via `uvx` (to run it without adding it as a dev dependency).

```bash
uvx ruff check .
uvx ruff format .
```

## 🛠️ Project Structure

- `anxiety/`: Main package source code.
- `tests/`: Test suite.
- `pyproject.toml`: Project configuration and dependencies.
- `uv.lock`: Deterministic dependency lockfile.
