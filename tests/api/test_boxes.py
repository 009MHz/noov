import pytest, allure, json
from allure_commons.types import AttachmentType

@pytest.mark.api
@allure.title("GET /open_api/boxes returns list and minimal shape")
async def test_boxes_list_ok(api_request):
    resp = await api_request.get("/open_api/boxes")
    allure.attach(await resp.text(), "boxes.raw.json", AttachmentType.JSON)
    assert resp.ok
    data = await resp.json()
    allure.attach(json.dumps(data, indent=2), "boxes.pretty.json", AttachmentType.JSON)
    assert isinstance(data, list)
    if data:
        b = data[0]
        assert {"name", "status", "location"}.issubset(b)
        assert {"latitude", "longitude"}.issubset(b["location"])
