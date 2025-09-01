import pytest

SCHEMA = {"name": str, "status": (str, int), "location": dict}
LOC = {"latitude": (int, float), "longitude": (int, float)}

@pytest.mark.api
def test_schema_all_items(api_request):
    r = api_request.get("/open_api/boxes")
    items = r.json()
    assert isinstance(items, list)
    for i, it in enumerate(items):
        for k, t in SCHEMA.items():
            assert k in it, f"missing {k} at {i}"
            assert isinstance(it[k], t)
        for k, t in LOC.items():
            assert k in it["location"], f"missing location.{k} at {i}"
            assert isinstance(it["location"][k], t)
