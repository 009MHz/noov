import pytest
import allure
from playwright.async_api import APIRequestContext
from sources.api.clients.reqres_client import ReqresClient
from utils.allure_helpers import step


@pytest.fixture(scope="function")
async def reqres_api(api_request: APIRequestContext):
    return ReqresClient(api_request)


@allure.epic("API Testing")
@allure.feature("Reqres API")
@pytest.mark.api
class TestReqresAPI:

    @allure.title("Get users list")
    @allure.story("Users")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_get_users_success(self, reqres_api: ReqresClient):
        with step("Send GET request to users endpoint"):
            response = await reqres_api.get_users(page=1)

        with step("Validate response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate response structure"):
            data = await response.json()
            assert "data" in data
            assert isinstance(data["data"], list)
            assert len(data["data"]) > 0

        with step("Validate user data fields"):
            first_user = data["data"][0]
            assert "id" in first_user
            assert "email" in first_user
            assert "first_name" in first_user
            assert "last_name" in first_user

    @allure.title("Get single user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_single_user_success(self, reqres_api: ReqresClient):
        with step("Send GET request for specific user ID"):
            response = await reqres_api.get_user_by_id(2)

        with step("Validate response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate response structure"):
            data = await response.json()
            assert "data" in data

        with step("Validate user data integrity"):
            user = data["data"]
            assert user["id"] == 2
            assert "email" in user
        assert "first_name" in user
        assert "last_name" in user
        assert "avatar" in user

    @allure.title("Create user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_create_user_success(self, reqres_api: ReqresClient):
        with step("Send POST request to create new user"):
            response = await reqres_api.create_user("John", "Developer")

        with step("Validate creation response status"):
            assert response.ok
            assert response.status == 201

        with step("Validate created user data"):
            data = await response.json()
            assert data["name"] == "John"
            assert data["job"] == "Developer"
            assert "id" in data
            assert "createdAt" in data

    @allure.title("Update user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_update_user_success(self, reqres_api: ReqresClient):
        with step("Send PUT request to update user"):
            response = await reqres_api.update_user(2, "Jane", "Manager")

        with step("Validate update response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate updated user data"):
            data = await response.json()
            assert data["name"] == "Jane"
            assert data["job"] == "Manager"
            assert "updatedAt" in data

    @allure.title("Delete user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_delete_user_success(self, reqres_api: ReqresClient):
        with step("Send DELETE request for user"):
            response = await reqres_api.delete_user(2)

        with step("Validate deletion response status"):
            assert response.ok
            assert response.status == 204

    @allure.title("Get resources list")
    @allure.story("Resources")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_resources_success(self, reqres_api: ReqresClient):
        with step("Send GET request to resources endpoint"):
            response = await reqres_api.get_resources()

        with step("Validate response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate response structure"):
            data = await response.json()
            assert "data" in data
            assert isinstance(data["data"], list)
            assert len(data["data"]) > 0

        with step("Validate resource data fields"):
            first_resource = data["data"][0]
            assert "id" in first_resource
            assert "name" in first_resource
            assert "year" in first_resource
            assert "color" in first_resource

    @allure.title("Get single resource")
    @allure.story("Resources")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_single_resource_success(self, reqres_api: ReqresClient):
        with step("Send GET request for specific resource ID"):
            response = await reqres_api.get_resource_by_id(2)

        with step("Validate response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate response structure"):
            data = await response.json()
            assert "data" in data

        with step("Validate resource data integrity"):
            resource = data["data"]
            assert resource["id"] == 2
            assert "name" in resource
            assert "year" in resource
            assert "color" in resource
            assert "pantone_value" in resource

    @allure.title("User login")
    @allure.story("Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_login_success(self, reqres_api: ReqresClient):
        with step("Send POST request for user authentication"):
            response = await reqres_api.login_user("eve.holt@reqres.in", "cityslicka")

        with step("Validate authentication response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate authentication token"):
            data = await response.json()
            assert "token" in data
            assert isinstance(data["token"], str)
            assert len(data["token"]) > 0

    @allure.title("User registration")
    @allure.story("Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_register_success(self, reqres_api: ReqresClient):
        with step("Send POST request for user registration"):
            response = await reqres_api.register_user("eve.holt@reqres.in", "pistol")

        with step("Validate registration response status"):
            assert response.ok
            assert response.status == 200

        with step("Validate registration data"):
            data = await response.json()
            assert "id" in data
            assert "token" in data
            assert isinstance(data["id"], int)
            assert isinstance(data["token"], str)
            assert len(data["token"]) > 0
