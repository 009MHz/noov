import pytest

@pytest.mark.api
def test_boxes_contract_minimal(api_request):
    r = api_request.get("/open_api/boxes")
    assert r.ok
    data = r.json()
    assert isinstance(data, list)
    if data:
        b = data[0]
        assert {"name", "status", "location"}.issubset(b)
        assert {"latitude", "longitude"}.issubset(b["location"])
