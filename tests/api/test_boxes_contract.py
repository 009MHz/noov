import pytest, allure

@pytest.mark.api
@allure.title("Boxes contract — minimal keys present on first item")
async def test_boxes_contract_minimal(api_request):
    r = await api_request.get("/open_api/boxes")
    assert r.ok
    data = await r.json()
    assert isinstance(data, list)
    if data:
        b = data[0]
        assert {"name", "status", "location"}.issubset(b)
        assert {"latitude", "longitude"}.issubset(b["location"])