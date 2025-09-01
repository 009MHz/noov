import json
import pytest
from allure_commons._allure import attach
from allure_commons.types import AttachmentType

@pytest.mark.api
async def test_boxes_ok(api_context):
    resp = await api_context.get("/open_api/boxes")
    # Attach response for debugging/reporting
    attach(await resp.text(), name="boxes.json", attachment_type=AttachmentType.JSON)
    assert resp.ok, f"Unexpected status {resp.status}: {await resp.text()}"

@pytest.mark.api
async def test_boxes_shape_minimal_contract(api_context):
    resp = await api_context.get("/open_api/boxes")
    data = await resp.json()
    assert isinstance(data, list)

    if data:  # soft contract on first item
        b = data[0]
        # required top-level fields
        for key in ["name", "status", "location"]:
            assert key in b, f"Missing {key}"
        # location sub-keys
        loc = b["location"]
        for key in ["latitude", "longitude"]:
            assert key in loc and isinstance(loc[key], (int, float)), f"Bad location.{key}"

@pytest.mark.api
async def test_boxes_not_found_path(api_context):
    r = await api_context.get("/open_api/boxes/does-not-exist")
    # Depending on backend routing; expect non-200:
    assert r.status != 200

@pytest.mark.api
async def test_boxes_cors_is_irrelevant_for_api_context(api_context):
    # Playwright Request API is server-to-server; just ensure JSON parses.
    r = await api_context.get("/open_api/boxes")
    _ = await r.json()
    assert r.ok
