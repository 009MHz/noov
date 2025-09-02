import pytest
import allure
import json
from allure_commons.types import AttachmentType
from utils.api_config import api_config

@pytest.mark.api
@allure.title("GET /open_api/boxes returns list and minimal shape")
async def test_boxes_list_ok(api_request):
    url = api_config.get_url("open_api/boxes")
    response = await api_request.get(url)
    
    raw_response = await response.text()
    allure.attach(raw_response, "boxes.raw.json", AttachmentType.JSON)
    
    # Assert response status
    assert response.ok, f"Expected successful response, got status {response.status}"
    assert response.status == 200, f"Expected status 200, got {response.status}"
    
    # Parse and validate response data
    data = await response.json()
    allure.attach(json.dumps(data, indent=2), "boxes.pretty.json", AttachmentType.JSON)
    
    # Validate response structure
    assert isinstance(data, list), "Response should be a list"
    
    if data:
        box = data[0]
        # Validate box structure
        assert {"name", "status", "location"}.issubset(box.keys()), \
            f"Missing required fields. Got: {box.keys()}"
            
        # Validate location structure
        assert {"latitude", "longitude"}.issubset(box["location"].keys()), \
            f"Missing location coordinates. Got: {box['location'].keys()}"
