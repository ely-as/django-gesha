from importlib.metadata import metadata
from pathlib import Path


def test_npm_pkg_description_matches_python_pkg_description(npm_package: dict) -> None:
    assert npm_package["description"] == metadata("django-gesha")["summary"]


def test_npm_pkg_main_exists(base_dir: Path, npm_package: dict) -> None:
    path_to_main = base_dir / npm_package["main"]
    assert path_to_main.exists()
