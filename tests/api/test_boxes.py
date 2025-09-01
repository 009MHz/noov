import json
import pytest
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Playwright

BASE_API = "https://api.noovoleum.com"

@pytest.mark.api
@allure.title("GET /open_api/boxes returns list and minimal shape")
def test_boxes_list_ok(playwright: Playwright):
    request = playwright.request.new_context(base_url=BASE_API, extra_http_headers={"Accept": "application/json"})
    resp = request.get("/open_api/boxes")
    allure.attach(resp.text(), "boxes.raw.json", AttachmentType.JSON)
    assert resp.ok, f"Status {resp.status}: {resp.text()}"
    data = resp.json()
    allure.attach(json.dumps(data, indent=2), "boxes.pretty.json", AttachmentType.JSON)
    assert isinstance(data, list)
    if data:
        b = data[0]
        assert {"name", "status", "location"}.issubset(b.keys())
        assert {"latitude", "longitude"}.issubset(b["location"].keys())
    request.dispose()