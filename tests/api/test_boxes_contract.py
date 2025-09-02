import pytest
import allure
from utils.api_config import api_config

@pytest.mark.api
@allure.title("Boxes contract — minimal keys present on first item")
async def test_boxes_contract_minimal(api_request):
    url = api_config.get_url("open_api/boxes")
    r = await api_request.get(url)
    raw_response = await r.text()
    allure.attach(raw_response, "boxes.raw.json", allure.attachment_type.JSON)
    assert r.ok
    data = await r.json()
    assert isinstance(data, list), "Response must be a list"
    if data:
        b = data[0]
        assert {"name", "status", "location"}.issubset(b), "First item missing required fields"
        assert {"latitude", "longitude"}.issubset(b["location"]), "Location missing coordinates"