import re

import pytest

import gesha

# Regex pattern for npm package versions, adapted from
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

# Regex pattern for Python package versions, copied from
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


def test_npm_pkg_version_is_semver(npm_package: dict) -> None:
    assert re.match(RE_NPM_VERSION, npm_package["version"])


def test_npm_pkg_version_aligns_with_python_pkg_version(npm_package: dict) -> None:
    npmver_str = npm_package["version"]
    pyver_str = gesha.__version__
    error_msg = (
        f"Python version '{pyver_str}' does not match npm version '{npmver_str}'"
    )
    # split package versions into their components
    npmver = re.match(RE_NPM_VERSION, npmver_str).groupdict()  # type: ignore[union-attr]
    pyver = re.match(RE_PY_VERSION, pyver_str).groupdict()  # type: ignore[union-attr]
    # py release segment can be truncated e.g. 0.1 instead of 0.1.0 - convert so it has
    # three parts (in semver three parts is mandatory)
    pyver_release = pyver["release"] + ".0" * max(0, 2 - pyver["release"].count("."))
    # compare release segment
    assert npmver["release"] == pyver_release, error_msg
    # compare pre-release segment
    pyver_prerelease = (pyver["pre_l"] or "") + (pyver["pre_n"] or "")
    assert npmver["prerelease"] == pyver_prerelease, error_msg


def test_npm_package_lock_json_has_same_version_as_package_json(
    npm_package: dict, npm_package_lock: dict
) -> None:
    pkgver = npm_package["version"]
    lockvers = (
        npm_package_lock["version"],
        npm_package_lock["packages"][""]["version"],
    )
    help_msg = "Try running `npm install --package-lock-only`"
    if lockvers[0] != lockvers[1]:
        pytest.fail(f"package-lock.json has 2 different versions. {help_msg}")
    if lockvers[0] != pkgver:
        pytest.fail(f"package.json and package-lock.json are out of sync. {help_msg}")
