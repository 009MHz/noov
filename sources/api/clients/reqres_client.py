from typing import Dict, List, Optional, Tuple
from playwright.async_api import APIResponse, APIRequestContext


class ReqresClient:
    """Simple API client for reqres.in endpoints."""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.base_url = "https://reqres.in/api"
        self.headers = {"x-api-key": "reqres-free-v1"}

    async def get_users(self, page: int = 1) -> APIResponse:
        """Get list of users."""
        return await self.request.get(
            f"{self.base_url}/users?page={page}", headers=self.headers
        )

    async def get_user_by_id(self, user_id: int) -> APIResponse:
        """Get single user by ID."""
        return await self.request.get(
            f"{self.base_url}/users/{user_id}", headers=self.headers
        )

    async def create_user(self, name: str, job: str) -> APIResponse:
        """Create new user."""
        data = {"name": name, "job": job}
        return await self.request.post(
            f"{self.base_url}/users", data=data, headers=self.headers
        )

    async def update_user(self, user_id: int, name: str, job: str) -> APIResponse:
        """Update user."""
        data = {"name": name, "job": job}
        return await self.request.put(
            f"{self.base_url}/users/{user_id}", data=data, headers=self.headers
        )

    async def delete_user(self, user_id: int) -> APIResponse:
        """Delete user."""
        return await self.request.delete(
            f"{self.base_url}/users/{user_id}", headers=self.headers
        )

    async def get_resources(self) -> APIResponse:
        """Get list of resources."""
        return await self.request.get(f"{self.base_url}/unknown", headers=self.headers)

    async def get_resource_by_id(self, resource_id: int) -> APIResponse:
        """Get single resource by ID."""
        return await self.request.get(
            f"{self.base_url}/unknown/{resource_id}", headers=self.headers
        )

    async def login_user(self, email: str, password: str) -> APIResponse:
        """Login user."""
        data = {"email": email, "password": password}
        return await self.request.post(
            f"{self.base_url}/login", data=data, headers=self.headers
        )

    async def register_user(self, email: str, password: str) -> APIResponse:
        """Register user."""
        data = {"email": email, "password": password}
        return await self.request.post(
            f"{self.base_url}/register", data=data, headers=self.headers
        )
