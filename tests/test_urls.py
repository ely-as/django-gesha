from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from django.urls import include, path

from gesha import types, urls


def view() -> None:
    return


# fmt: off
urlpatterns: types.URLPatterns = [
    path("", include((
        [
            path("", view, name="index"),
            path("a/<slug:a>/b/<int:b>/", view, name="two_args"),
            path("ns2/", include((
                [
                    path("b/", view, name="double_nested_namespace"),
                    path("/c/", view, name="leading_slash_in_namespaced_path"),
                ],
                "ns2"
            ))),
        ],
        "ns1"
    ))),
    path("unnamed-url/", view),
    path("unnamed-ns/", include(
        [
            path("a/", view, name="inside_unnamed_include")
        ]
    )),
]
# fmt: on

# NOTE: The following paths are expected to be generated by get_paths_dict() from the
# above urlpatterns
expected_paths: list[types.PathInfo] = [
    {
        "name": "ns1:index",
        "route": "/",
        "args": {},
    },
    {
        "name": "ns1:two_args",
        "route": "/a/<slug:a>/b/<int:b>/",
        "args": {
            "a": "slug",
            "b": "int",
        },
    },
    {
        "name": "ns1:ns2:double_nested_namespace",
        "route": "/ns2/b/",
        "args": {},
    },
    {
        "name": "ns1:ns2:leading_slash_in_namespaced_path",
        "route": "/ns2/c/",
        "args": {},
    },
    {
        "name": "inside_unnamed_include",
        "route": "/unnamed-ns/a/",
        "args": {},
    },
]


@pytest.fixture
def urlconf() -> Iterator[types.URLConf]:
    yield __name__


@pytest.fixture
def paths_dict(urlconf: types.URLConf) -> Iterator[types.Paths]:
    yield urls.get_paths_dict(urlconf)


@pytest.fixture(params=expected_paths)
def expected_path(request: pytest.FixtureRequest) -> Iterator[types.PathInfo]:
    yield request.param


def test_urls_have_correct_name(
    paths_dict: types.Paths, expected_path: types.PathInfo
) -> None:
    name = expected_path["name"]
    assert name in paths_dict
    assert paths_dict[name]["name"] == name


def test_urls_have_correct_route(
    paths_dict: types.Paths, expected_path: types.PathInfo
) -> None:
    name = expected_path["name"]
    if path_info := paths_dict.get(name):
        assert path_info["route"] == expected_path["route"]
    else:
        pytest.skip(f"'{name}' not found in 'paths_dict', see other failing test.")


def test_urls_have_correct_args(
    paths_dict: types.Paths, expected_path: types.PathInfo
) -> None:
    name = expected_path["name"]
    if path_info := paths_dict.get(name):
        for key, value in path_info["args"].items():
            assert value == expected_path["args"][key]
    else:
        pytest.skip(f"'{name}' not found in 'paths_dict', see other failing test.")


def test_paths_dict_does_not_contain_unnamed_urls(paths_dict: types.Paths) -> None:
    assert None not in paths_dict


def test_get_paths_dict_can_load_default_urlconf() -> None:
    paths_dict = urls.get_paths_dict()
    assert "fake:test" in paths_dict


get_args_expected_results: list[tuple[str, dict[str, str]]] = [
    ("/<int:num>", {"num": "int"}),
    ("/<int:num>/<slug:slug>", {"num": "int", "slug": "slug"}),  # 2 args, diff type
    ("/<int:num>/<int:id>", {"num": "int", "id": "int"}),  # 2 args, same type
]


@pytest.mark.parametrize("route,expected_result", get_args_expected_results)
def test_get_args_returns_expected_result(
    route: str, expected_result: dict[str, str]
) -> None:
    result = urls.get_args(route)
    for url_arg, converter_name in expected_result.items():
        assert url_arg in result
        assert result[url_arg] == converter_name


namejoin_expected_results: list[tuple[list[str], str]] = [
    ([], ""),
    ([""], ""),
    (["ns1", "", "viewname"], "ns1:viewname"),
    (["ns1", "", "", "viewname"], "ns1:viewname"),
    (["ns1", "ns2", "viewname"], "ns1:ns2:viewname"),
]


@pytest.mark.parametrize("args,expected_result", namejoin_expected_results)
def test_namejoin_returns_expected_result(
    args: list[str], expected_result: str
) -> None:
    assert urls.namejoin(*args) == expected_result


pathjoin_expected_results: list[tuple[list[str], str]] = [
    ([], "/"),
    (["foo"], "/foo"),
    (["/foo"], "/foo"),
    (["foo", "bar"], "/foo/bar"),
    # preferred by Django i.e. include() with trailing /, route with no starting /:
    (["foo/", "bar"], "/foo/bar"),
    # Django will warn against this (route starting with /), but still run:
    (["foo/", "/bar"], "/foo/bar"),
    (["foo", "", "bar"], "/foo/bar"),
    (["foo", "", "", "bar"], "/foo/bar"),
    (["foo/", "", "/bar"], "/foo/bar"),
]


@pytest.mark.parametrize("args,expected_result", pathjoin_expected_results)
def test_pathjoin_returns_expected_result(
    args: list[str], expected_result: str
) -> None:
    assert urls.pathjoin(*args) == expected_result


# Test caching


@pytest.fixture
def get_cache_info() -> Iterator[Callable]:
    """Fixture will ensure cache is cleared before unit test is run."""
    cache_func = urls._resolver_to_paths_dict
    cache_func.cache_clear()
    yield cache_func.cache_info


def test_get_paths_dict_result_is_cached(get_cache_info: Callable) -> None:
    urls.get_paths_dict()  # should get new result (1 miss)
    urls.get_paths_dict()  # should get cached result (1 hit)
    cache_info = get_cache_info()
    assert cache_info.hits == 1
    assert cache_info.misses == 1
    assert cache_info.currsize == 1


def test_get_paths_dict_result_is_reevaluated_if_urlconf_changes(
    get_cache_info: Callable, urlconf: types.URLConf
) -> None:
    urls.get_paths_dict()
    urls.get_paths_dict(urlconf)
    urls.get_paths_dict()
    urls.get_paths_dict(urlconf)
    cache_info = get_cache_info()
    assert cache_info.hits == 2
    assert cache_info.misses == 2
    assert cache_info.currsize == 2
