import pytest
import allure
from playwright.async_api import APIRequestContext
from sources.api.__base import BaseService
from sources.api.clients.noovo_home_client import HomeClient


@pytest.fixture(scope="function")
async def noovo_api(api_request: APIRequestContext):
    api_client = BaseService(api_request)
    return HomeClient(api_client)


@allure.epic("API Testing")
@allure.feature("Noovo API")
@pytest.mark.api
class TestNoovoAPI:
    
    def _assert_response_ok(self, response, context: str = ""):
        prefix = f"{context}: " if context else ""
        assert (
            response.status == 200
        ), f"{prefix}Expected status 200, got {response.status}"

    def _assert_json_content_type(self, noovo_api: HomeClient, response):
        content_type = noovo_api.get_content_type(response)
        assert (
            "application/json" in content_type.lower()
        ), f"Expected JSON content type, got: {content_type}"

    def _validate_item_structure(
        self, noovo_api: HomeClient, item: dict, index: int = 0
    ):
        errors = noovo_api.validate_item_structure(item)
        assert not errors, f"Item {index} validation errors: {errors}"

    @allure.title("Get noovo list validation")
    @allure.story("Get Noovo List")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_noovo_list_success(self, noovo_api: HomeClient):
        allure.step("Send GET request to noovo API")
        response, data, _ = await noovo_api.get_parsed_response()

        allure.step("Validate response status and content type")
        self._assert_response_ok(response)
        self._assert_json_content_type(noovo_api, response)

        allure.step("Validate response structure")
        response, noovo_data, validation_errors = await noovo_api.get_validated_data()

        assert (
            not validation_errors
        ), f"Structure validation errors: {validation_errors}"
        assert isinstance(
            noovo_data, list
        ), f"Expected list response, got {type(noovo_data)}"

        if noovo_data:
            allure.step("Validate first item data structure")
            response, first_item = await noovo_api.get_first_item()

            assert first_item is not None, "First item should not be None"
            self._validate_item_structure(noovo_api, first_item)

    @allure.title("Get nonexistent item error handling")
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_nonexistent_item_error(self, noovo_api: HomeClient):
        nonexistent_id = "non-existent-noovo-id-12345"

        allure.step("Send GET request for non-existent item")
        response = await noovo_api.get_noovo_by_id(nonexistent_id)

        allure.step("Validate error response")
        assert response.status in [
            404,
            400,
        ], f"Expected error status (404/400) for non-existent item, got {response.status}"
        assert (
            not response.ok
        ), "Response should not be successful for non-existent item"

    @allure.title("Noovo coordinate validation")
    @allure.story("Data Validation")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_coordinates_validation(self, noovo_api: HomeClient):
        allure.step("Get noovo data for coordinate validation")
        response, noovo_data, validation_errors = await noovo_api.get_validated_data()

        allure.step("Validate response and data structure")
        self._assert_response_ok(response)
        assert (
            not validation_errors
        ), f"Structure validation errors: {validation_errors}"
        assert isinstance(noovo_data, list), "Response should be a list"

        allure.step("Validate coordinates for all items")
        for i, item in enumerate(noovo_data):
            latitude, longitude, coord_errors = noovo_api.extract_coordinates(item)

            if not coord_errors:
                coord_validation_errors = noovo_api.validate_coordinates(
                    latitude, longitude
                )
                assert (
                    not coord_validation_errors
                ), f"Item {i} coordinate validation errors: {coord_validation_errors}"

    @allure.title("API response time validation")
    @allure.story("Performance")
    @allure.severity(allure.severity_level.MINOR)
    async def test_response_time_performance(self, noovo_api: HomeClient):
        max_response_time = 5.0

        allure.step("Measure API response time")
        response, _, response_time = await noovo_api.get_parsed_response(
            measure_time=True
        )

        allure.step("Validate response and performance")
        self._assert_response_ok(response)
        assert (
            response_time < max_response_time
        ), f"Response time {response_time:.2f}s exceeded maximum {max_response_time}s"

        allure.attach(
            f"Response time: {response_time:.3f} seconds",
            "Performance Metrics",
            allure.attachment_type.TEXT,
        )

    @allure.title("Multiple API requests workflow")
    @allure.story("Integration")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_multiple_requests_workflow(self, noovo_api: HomeClient):
        list_response, first_item, detail_response = await noovo_api.execute_workflow()

        self._assert_response_ok(list_response, "List request")

        if first_item is not None:
            assert isinstance(first_item, dict), "First item should be a dictionary"

            if detail_response.status == 200:
                assert detail_response.ok, "Detail request should be successful"

                detail_data = await detail_response.json()
                assert isinstance(
                    detail_data, dict
                ), "Expected object response for item detail"

                self._validate_item_structure(noovo_api, detail_data)

            elif detail_response.status == 404:
                assert not detail_response.ok, "404 response should not be ok"

            else:
                raise AssertionError(
                    f"Unexpected status for item detail: {detail_response.status}"
                )
        else:
            assert (
                list_response.status == 200
            ), "List response should be successful even if empty"

    @allure.title("All noovo structure validation")
    @allure.story("Structure Validation")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_all_noovo_structure(self, noovo_api: HomeClient):
        response, noovo_data, validation_errors = await noovo_api.get_validated_data()

        self._assert_response_ok(response)
        assert (
            not validation_errors
        ), f"Structure validation errors: {validation_errors}"
        assert isinstance(noovo_data, list), "Response should be a list"

        for i, item in enumerate(noovo_data):
            self._validate_item_structure(noovo_api, item, i)
