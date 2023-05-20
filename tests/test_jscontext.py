from __future__ import annotations

import json
from collections.abc import Iterator

import django
import pytest
from bs4 import BeautifulSoup
from django.test import Client, override_settings


def request_soup(method: str, path: str) -> BeautifulSoup:
    response = Client().generic(method, path)
    return BeautifulSoup(response.content, "lxml")


paths_to_test_for_presence_of_valid_script_html: list[str] = [
    "/",  # tests JSContextMixin
    "/func-based/",  # tests create_js_context_data()
]

if django.VERSION[:2] >= (3, 1):
    paths_to_test_for_presence_of_valid_script_html += [
        "/async/",  # tests async
    ]


@pytest.fixture(params=paths_to_test_for_presence_of_valid_script_html)
def path(request: pytest.FixtureRequest) -> Iterator[str]:
    yield request.param


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


def test_paths_are_empty_by_default(path: str) -> None:
    soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert js_context["_gesha"]["paths"] == {}


def test_paths_are_empty_when_GESHA_ALLOWED_URL_PATTERNS_is_empty_list(
    path: str,
) -> None:
    with override_settings(GESHA_ALLOWED_URL_PATTERNS=[]):
        soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert js_context["_gesha"]["paths"] == {}


def test_paths_are_filtered_when_GESHA_ALLOWED_URL_PATTERNS_is_set(path: str) -> None:
    with override_settings(GESHA_ALLOWED_URL_PATTERNS=["fake:test"]):
        soup = request_soup("GET", path)
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert len(js_context["_gesha"]["paths"]) == 1
