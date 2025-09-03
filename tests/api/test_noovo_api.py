import pytest
import allure
from playwright.async_api import APIRequestContext
from sources.api.__base import BaseService
from sources.api.clients.noovo_home_client import HomeClient


@pytest.fixture(scope='function')
async def noovo_api(api_request: APIRequestContext):
    """Fixture to provide HomeClient instance for noovo API tests."""
    api_client = BaseService(api_request)
    return HomeClient(api_client)


@allure.epic("API Testing")
@allure.feature("Noovo API")
@pytest.mark.api
class TestNoovoAPI:
    """Test class for Noovo API endpoints following Page Object Model pattern."""
    
    @allure.title("Get noovo list validation")
    @allure.story("Get Noovo List")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_noovo_list_success(self, noovo_api: HomeClient):
        """Test successful retrieval of noovo list with structure validation."""
        # Action: Get noovo list and content type
        response, content_type = await noovo_api.get_content_type()
        
        # Assertions: Validate response status and headers
        assert response.ok, f"Expected successful response, got status {response.status}"
        assert response.status == 200, f"Expected status 200, got {response.status}"
        assert "application/json" in content_type.lower(), \
            f"Expected JSON content type, got: {content_type}"
        
        # Action: Parse response structure
        response, noovo_data, validation_errors = await noovo_api.check_all_items_structure()
        
        # Assertions: Validate structure parsing
        assert not validation_errors, f"Structure validation errors: {validation_errors}"
        assert isinstance(noovo_data, list), f"Expected list response, got {type(noovo_data)}"
        
        # Action: Get first item if data exists
        if noovo_data:
            response, first_item = await noovo_api.get_first_noovo_item()
            
            # Assertions: Validate first item structure
            assert first_item is not None, "First item should not be None"
            
            required_fields = noovo_api.get_required_fields()
            missing_fields = required_fields - set(first_item.keys())
            assert not missing_fields, \
                f"Missing required fields: {missing_fields}. Available: {set(first_item.keys())}"
            
            # Validate location structure if present
            if "location" in first_item and first_item["location"]:
                location = first_item["location"]
                assert isinstance(location, dict), f"Location should be dict, got {type(location)}"
                
                required_location_fields = noovo_api.get_required_location_fields()
                missing_location_fields = required_location_fields - set(location.keys())
                assert not missing_location_fields, \
                    f"Missing location fields: {missing_location_fields}"

    @allure.title("Get nonexistent item error handling")
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_nonexistent_item_error(self, noovo_api: HomeClient):
        """Test error handling for non-existent noovo item."""
        nonexistent_id = "non-existent-noovo-id-12345"
        
        # Action: Request non-existent item
        response = await noovo_api.get_noovo_by_id(nonexistent_id)
        
        # Assertions: Validate error response
        assert response.status in [404, 400], \
            f"Expected error status (404/400) for non-existent item, got {response.status}"
        assert not response.ok, "Response should not be successful for non-existent item"

    @allure.title("Noovo coordinate validation")
    @allure.story("Data Validation")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_coordinates_validation(self, noovo_api: HomeClient):
        """Test coordinate validation for noovo item locations."""
        # Action: Get all items and structure data
        response, noovo_data, validation_errors = await noovo_api.check_all_items_structure()
        
        # Assertions: Validate response and structure
        assert response.ok, f"Expected successful response, got status {response.status}"
        assert not validation_errors, f"Structure validation errors: {validation_errors}"
        assert isinstance(noovo_data, list), "Response should be a list"
        
        # Validate coordinates for each item
        for i, item in enumerate(noovo_data):
            # Action: Extract coordinates from item
            latitude, longitude, coord_errors = await noovo_api.get_item_coordinates(item)
            
            # Assertions: Validate coordinates if present
            if not coord_errors and latitude is not None:
                assert isinstance(latitude, (int, float)), \
                    f"Item {i}: Latitude should be numeric, got {type(latitude)}: {latitude}"
                assert -90 <= latitude <= 90, \
                    f"Item {i}: Latitude should be between -90 and 90, got: {latitude}"
            
            if not coord_errors and longitude is not None:
                assert isinstance(longitude, (int, float)), \
                    f"Item {i}: Longitude should be numeric, got {type(longitude)}: {longitude}"
                assert -180 <= longitude <= 180, \
                    f"Item {i}: Longitude should be between -180 and 180, got: {longitude}"

    @allure.title("API response time validation")
    @allure.story("Performance")
    @allure.severity(allure.severity_level.MINOR)
    async def test_response_time_performance(self, noovo_api: HomeClient):
        """Test API response time performance."""
        max_response_time = 5.0  # seconds
        
        # Action: Measure API response time
        response, response_time = await noovo_api.get_response_time()
        
        # Assertions: Validate response and performance
        assert response.ok, f"Expected successful response, got status {response.status}"
        assert response_time < max_response_time, \
            f"Response time {response_time:.2f}s exceeded maximum {max_response_time}s"
        
        # Attach performance data
        allure.attach(
            f"Response time: {response_time:.3f} seconds",
            "Performance Metrics",
            allure.attachment_type.TEXT
        )

    @allure.title("Multiple API requests workflow")
    @allure.story("Integration")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_multiple_requests_workflow(self, noovo_api: HomeClient):
        """Test workflow with multiple API requests."""
        # Action: Execute workflow (list + detail)
        list_response, first_item, detail_response = await noovo_api.get_workflow_data()
        
        # Assertions: Validate list response
        assert list_response.ok, f"List request failed with status {list_response.status}"
        
        if first_item is not None:
            # We have data, validate workflow
            assert isinstance(first_item, dict), "First item should be a dictionary"
            
            if detail_response.status == 200:
                # Assertions: Validate successful detail response
                assert detail_response.ok, "Detail request should be successful"
                
                # Action: Parse detail response
                detail_data = await detail_response.json()
                
                # Assertions: Validate detail structure
                assert isinstance(detail_data, dict), "Expected object response for item detail"
                
                required_fields = noovo_api.get_required_fields()
                available_fields = set(detail_data.keys())
                missing_fields = required_fields - available_fields
                assert not missing_fields, \
                    f"Item detail missing fields: {missing_fields}. Available: {available_fields}"
            
            elif detail_response.status == 404:
                # Assertions: Handle expected 404 for individual item endpoint
                assert not detail_response.ok, "404 response should not be ok"
            
            else:
                # Unexpected status
                raise AssertionError(f"Unexpected status for item detail: {detail_response.status}")
        else:
            # No data available, just ensure we got a response
            assert list_response.status == 200, "List response should be successful even if empty"

    @allure.title("All noovo structure validation")
    @allure.story("Structure Validation")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_all_noovo_structure(self, noovo_api: HomeClient):
        """Test structure validation for all noovo items using page object methods."""
        # Action: Get all items and check structure
        response, noovo_data, validation_errors = await noovo_api.check_all_items_structure()
        
        # Assertions: Validate response and structure
        assert response.ok, f"Expected successful response, got status {response.status}"
        assert not validation_errors, f"Structure validation errors: {validation_errors}"
        assert isinstance(noovo_data, list), "Response should be a list"
        
        # Validate structure for each item using helper method
        for i, item in enumerate(noovo_data):
            self._validate_item_structure_with_page_object(noovo_api, item, i)

    def _validate_item_structure_with_page_object(self, noovo_api: HomeClient, item_data: dict, item_index: int = 0) -> None:
        """
        Helper method for validating item structure using page object methods.
        Follows the pattern of helper methods in UI test classes.
        """
        # Use page object to get required fields
        required_fields = noovo_api.get_required_fields()
        missing_fields = required_fields - set(item_data.keys())
        assert not missing_fields, \
            f"Item {item_index} missing required fields: {missing_fields}. Available: {set(item_data.keys())}"
        
        # Validate location if present
        if "location" in item_data and item_data["location"]:
            location = item_data["location"]
            assert isinstance(location, dict), \
                f"Item {item_index}: Location should be dict, got {type(location)}"
            
            # Use page object to get required location fields
            required_location_fields = noovo_api.get_required_location_fields()
            missing_location_fields = required_location_fields - set(location.keys())
            assert not missing_location_fields, \
                f"Item {item_index}: Missing location fields: {missing_location_fields}"
