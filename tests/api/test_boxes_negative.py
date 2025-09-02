import pytest
from utils.api_config import api_config

@pytest.mark.api
async def test_boxes_invalid_path(api_request):
    url = api_config.get_url("open_api/invalid")
    r = await api_request.get(url)
    assert r.status == 404 or not r.ok

@pytest.mark.api
async def test_boxes_method_not_allowed(api_request):
    url = api_config.get_url("open_api/boxes")
    r = await api_request.post(url, data={})
    assert r.status in (400, 404, 405), f"Expected status 400, 404, or 405, but got {r.status}"