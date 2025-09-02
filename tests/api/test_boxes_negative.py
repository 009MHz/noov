import pytest

@pytest.mark.api
async def test_boxes_invalid_path(api_request):
    r = await api_request.get("/open_api/invalid")
    assert r.status == 404 or not r.ok

@pytest.mark.api
async def test_boxes_method_not_allowed(api_request):
    r = await api_request.post("/open_api/boxes")
    assert r.status in (400, 405)