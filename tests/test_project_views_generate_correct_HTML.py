"""
Functional tests which confirm that the {% jscontext %} template tag is generating the
correct HTML in conjunction with correctly configured views, and can also be modified by
settings overrides.
"""
from __future__ import annotations

import json
from collections.abc import Iterator

import django
import pytest
from bs4 import BeautifulSoup
from django.test import Client, override_settings


def request_soup(method: str, path: str) -> BeautifulSoup:
    """Perform an HTTP request against the Django test client and return a
    `BeautifulSoup` object.

    This is a function (rather than a @pytest.fixture) so the output can be modified
    using django.test.override_settings as a context manager.
    """
    response = Client().generic(method, path)
    return BeautifulSoup(response.content, "lxml")


# defined in test_project/fake/urls.py
paths_to_test: list[str] = [
    "/",  # tests JSContextMixin
    "/func-based/",  # tests create_js_context_data()
]

if django.VERSION[:2] >= (3, 1):
    paths_to_test.append("/async/")


@pytest.fixture(params=paths_to_test)
def path(request: pytest.FixtureRequest) -> Iterator[str]:
    yield request.param


# Tests for {% jscontext %} generating correct <script> elements


def test_jscontext_tag_generates_script_html(path: str) -> None:
    soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    assert json_script
    js_context = json.loads(json_script.text)
    assert "myString" in js_context


def test_jscontext_tag_works_when_setting_GESHA_JSCONTEXT_KEY_is_changed(
    path: str,
) -> None:
    with override_settings(GESHA_JSCONTEXT_KEY="different_key"):
        soup = request_soup("GET", path)
    json_script = soup.find("script", id="different_key")
    assert json_script


# Tests for the JSON within the <script> elements


def test_JSON_paths_are_empty_by_default(path: str) -> None:
    soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert js_context["_gesha"]["paths"] == {}


def test_JSON_paths_are_empty_when_GESHA_ALLOWED_URL_NAMES_is_empty_list(
    path: str,
) -> None:
    with override_settings(GESHA_ALLOWED_URL_NAMES=[]):
        soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert js_context["_gesha"]["paths"] == {}


def test_JSON_paths_are_filtered_when_GESHA_ALLOWED_URL_NAMES_is_set(
    path: str,
) -> None:
    with override_settings(GESHA_ALLOWED_URL_NAMES=["fake:test"]):
        soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert len(js_context["_gesha"]["paths"]) == 1
