import pytest
import allure
from playwright.async_api import APIRequestContext
from sources.api.clients.reqres_client import ReqresClient


@pytest.fixture(scope="class")
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
        response = await reqres_api.get_users(page=1)

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        first_user = data["data"][0]
        assert "id" in first_user
        assert "email" in first_user
        assert "first_name" in first_user
        assert "last_name" in first_user

    @allure.title("Get single user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_single_user_success(self, reqres_api: ReqresClient):
        response = await reqres_api.get_user_by_id(2)

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "data" in data

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
        response = await reqres_api.create_user("John", "Developer")

        assert response.ok
        assert response.status == 201

        data = await response.json()
        assert data["name"] == "John"
        assert data["job"] == "Developer"
        assert "id" in data
        assert "createdAt" in data

    @allure.title("Update user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_update_user_success(self, reqres_api: ReqresClient):
        response = await reqres_api.update_user(2, "Jane", "Manager")

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert data["name"] == "Jane"
        assert data["job"] == "Manager"
        assert "updatedAt" in data

    @allure.title("Delete user")
    @allure.story("Users")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_delete_user_success(self, reqres_api: ReqresClient):
        response = await reqres_api.delete_user(2)

        assert response.ok
        assert response.status == 204

    @allure.title("Get resources list")
    @allure.story("Resources")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_resources_success(self, reqres_api: ReqresClient):
        response = await reqres_api.get_resources()

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        first_resource = data["data"][0]
        assert "id" in first_resource
        assert "name" in first_resource
        assert "year" in first_resource
        assert "color" in first_resource

    @allure.title("Get single resource")
    @allure.story("Resources")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_single_resource_success(self, reqres_api: ReqresClient):
        response = await reqres_api.get_resource_by_id(2)

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "data" in data

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
        response = await reqres_api.login_user("eve.holt@reqres.in", "cityslicka")

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "token" in data
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

    @allure.title("User registration")
    @allure.story("Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_register_success(self, reqres_api: ReqresClient):
        response = await reqres_api.register_user("eve.holt@reqres.in", "pistol")

        assert response.ok
        assert response.status == 200

        data = await response.json()
        assert "id" in data
        assert "token" in data
        assert isinstance(data["id"], int)
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0
