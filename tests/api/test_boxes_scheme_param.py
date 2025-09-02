import pytest

SCHEMA = {"name": str, "status": (str, int), "location": dict}
LOC = {"latitude": (int, float), "longitude": (int, float)}

@pytest.mark.api
async def test_schema_all_items(api_request):
    resp = await api_request.get("/open_api/boxes")
    assert resp.ok
    items = await resp.json()
    assert isinstance(items, list)
    for i, it in enumerate(items):
        for k, t in SCHEMA.items():
            assert k in it, f"missing {k} at {i}"
            assert isinstance(it[k], t)
        loc = it["location"]
        for k, t in LOC.items():
            assert k in loc, f"missing location.{k} at {i}"
            assert isinstance(loc[k], t)