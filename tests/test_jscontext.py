import json

import pytest
from bs4 import BeautifulSoup
from django.test import Client, override_settings


@pytest.fixture
def client() -> Client:
    return Client()


def test_jscontext_tag_generates_script_html(client: Client) -> None:
    client = Client()
    response = client.get("/")
    soup = BeautifulSoup(response.content, "lxml")
    json_script = soup.find("script", id="js_context_data")
    assert json_script
    js_context = json.loads(json_script.text)
    assert "myString" in js_context


@override_settings(GESHA_JSCONTEXT_KEY="different_key")
def test_jscontext_tag_works_when_setting_GESHA_JSCONTEXT_KEY_is_changed(
    client: Client,
) -> None:
    client = Client()
    response = client.get("/")
    soup = BeautifulSoup(response.content, "lxml")
    json_script = soup.find("script", id="different_key")
    assert json_script
