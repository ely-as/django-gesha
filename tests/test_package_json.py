"""
Test that the NPM package information stays aligned with the Python package information.
"""
import json
import re
from importlib.metadata import metadata
from pathlib import Path

import gesha

BASE_DIR: Path = Path(__file__).parent.parent
PATH_TO_PACKAGE_JSON: Path = BASE_DIR / "package.json"

# for npm versions, adapted from
# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
NPM_VERSION_PATTERN = r"""
    (?P<release>
        (?P<major>0|[1-9]\d*)\.
        (?P<minor>0|[1-9]\d*)\.
        (?P<patch>0|[1-9]\d*)
    )
    (?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
    (?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?
"""

# for py versions, copied from
# https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
PY_VERSION_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""

RE_NPM_VERSION = re.compile(r"^\s*" + NPM_VERSION_PATTERN + r"\s*$", re.VERBOSE)
RE_PY_VERSION = re.compile(
    r"^\s*" + PY_VERSION_PATTERN + r"\s*$",
    re.VERBOSE | re.IGNORECASE,
)


def load_package_json() -> dict:
    with open(PATH_TO_PACKAGE_JSON, "r") as f:
        return json.load(f)


def load_python_package_metadata() -> dict:
    return {k.lower(): v for k, v in metadata("django-gesha").items()}  # type: ignore[attr-defined]


def test_npm_version_is_semver() -> None:
    npm_info = load_package_json()
    assert re.match(RE_NPM_VERSION, npm_info["version"])


def test_npm_version_aligns_with_py_version() -> None:
    npm_info = load_package_json()
    # get version components
    npm_version = re.match(RE_NPM_VERSION, npm_info["version"]).groupdict()  # type: ignore[union-attr]
    py_version = re.match(RE_PY_VERSION, gesha.__version__).groupdict()  # type: ignore[union-attr]
    # compare release segment (note: the py version can be truncated)
    assert npm_version["release"].startswith(py_version["release"])
    # compare pre-release segment
    py_pre = (py_version["pre_l"] or "") + (py_version["pre_n"] or "")
    assert npm_version["prerelease"] == py_pre


def test_npm_description_matches_py_description() -> None:
    npm_info = load_package_json()
    py_info = load_python_package_metadata()
    assert npm_info["description"] == py_info["summary"]


def test_npm_main_exists() -> None:
    npm_info = load_package_json()
    path_to_main = BASE_DIR / npm_info["main"]
    assert path_to_main.exists()
