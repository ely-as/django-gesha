import json

from bs4 import BeautifulSoup
from django.test import Client, override_settings


def request_soup(method: str, path: str) -> BeautifulSoup:
    response = Client().generic(method, path)
    return BeautifulSoup(response.content, "lxml")


def test_jscontext_tag_plus_JSContextMixin_generates_script_html() -> None:
    soup = request_soup("GET", "/")
    json_script = soup.find("script", id="js_context_data")
    assert json_script
    js_context = json.loads(json_script.text)
    assert "myString" in js_context


def test_jscontext_tag_plus_create_js_context_data_func_generates_script_html() -> None:
    soup = request_soup("GET", "/func-based/")
    json_script = soup.find("script", id="js_context_data")
    assert json_script
    js_context = json.loads(json_script.text)
    assert "myString" in js_context


def test_jscontext_tag_works_when_setting_GESHA_JSCONTEXT_KEY_is_changed() -> None:
    with override_settings(GESHA_JSCONTEXT_KEY="different_key"):
        soup = request_soup("GET", "/")
    json_script = soup.find("script", id="different_key")
    assert json_script


def test_paths_are_empty_when_GESHA_ALLOWED_URL_PATTERNS_is_empty() -> None:
    with override_settings(GESHA_ALLOWED_URL_PATTERNS=[]):
        soup = request_soup("GET", "/")
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert js_context["_gesha"]["paths"] == {}


def test_paths_are_filtered_when_GESHA_ALLOWED_URL_PATTERNS_is_set() -> None:
    with override_settings(GESHA_ALLOWED_URL_PATTERNS=["fake:test"]):
        soup = request_soup("GET", "/")
    json_script = soup.find("script", id="js_context_data")
    js_context = json.loads(json_script.text)  # type: ignore[union-attr]
    assert len(js_context["_gesha"]["paths"]) == 1
