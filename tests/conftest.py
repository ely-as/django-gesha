from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def base_dir() -> Iterator[Path]:
    """Base directory of this repository."""
    yield Path(__file__).parent.parent


@pytest.fixture
def npm_package(base_dir: Path) -> Iterator[dict]:
    """package.json data for the django-gesha npm package."""
    with open(base_dir / "package.json", "r") as f:
        yield json.load(f)


@pytest.fixture
def npm_package_lock(base_dir: Path) -> Iterator[dict]:
    """package-lock.json data for the django-gesha npm package."""
    with open(base_dir / "package-lock.json", "r") as f:
        yield json.load(f)
