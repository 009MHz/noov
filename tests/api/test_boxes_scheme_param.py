import pytest
from utils.api_config import api_config

SCHEMA = {"name": str, "status": (str, int), "location": dict}
LOC = {"latitude": (int, float), "longitude": (int, float)}

@pytest.mark.api
async def test_schema_all_items(api_request):
    url = api_config.get_url("open_api/boxes")
    resp = await api_request.get(url)
    assert resp.ok
    items = await resp.json()
    assert isinstance(items, list)
    for i, it in enumerate(items):
        for k, t in SCHEMA.items():
            assert k in it, f"missing {k} at {i}"
            assert isinstance(it[k], t), f"invalid type for {k} at {i}"
        loc = it["location"]
        for k, t in LOC.items():
            assert k in loc, f"missing location.{k} at {i}"
            assert isinstance(loc[k], t), f"invalid type for location.{k} at {i}"