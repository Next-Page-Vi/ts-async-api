#!/bin/sh
set -xe
uv run --no-sync ruff format .
uv run --no-sync mypy .
uv run --no-sync ruff check . --fix
uv run --no-sync pytest -vvv .
