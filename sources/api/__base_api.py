import json
import allure
from typing import Dict, Any, Optional, Union
from playwright.async_api import APIRequestContext, APIResponse
from allure_commons.types import AttachmentType
from utils.api_config import api_config


class BaseAPIClient:
    def __init__(self, request_context: APIRequestContext):
        """Initialize the API client with a Playwright request context."""
        self.request = request_context
        self.base_url = api_config.base_url

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> APIResponse:
        url = api_config.get_url(endpoint)
        return await self._make_request(
            "GET", url, params=params, headers=headers, **kwargs
        )

    async def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> APIResponse:
        url = api_config.get_url(endpoint)
        return await self._make_request(
            "POST", url, data=data, json_data=json_data, headers=headers, **kwargs
        )

    async def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> APIResponse:
        url = api_config.get_url(endpoint)
        return await self._make_request(
            "PUT", url, data=data, json_data=json_data, headers=headers, **kwargs
        )

    async def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> APIResponse:
        url = api_config.get_url(endpoint)
        return await self._make_request(
            "PATCH", url, data=data, json_data=json_data, headers=headers, **kwargs
        )

    async def delete(
        self, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs
    ) -> APIResponse:
        url = api_config.get_url(endpoint)
        return await self._make_request("DELETE", url, headers=headers, **kwargs)

    async def _make_request(self, method: str, url: str, **kwargs) -> APIResponse:
        # Use allure step for better reporting
        allure.step(f"{method} {url}")

        # Attach request details for better debugging
        await self._attach_request_details(method, url, kwargs)

        # Make the request using Playwright's built-in methods
        if method == "GET":
            response = await self.request.get(url, **kwargs)
        elif method == "POST":
            response = await self.request.post(url, **kwargs)
        elif method == "PUT":
            response = await self.request.put(url, **kwargs)
        elif method == "PATCH":
            response = await self.request.patch(url, **kwargs)
        elif method == "DELETE":
            response = await self.request.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Attach response details for better reporting
        await self._attach_response_details(response)

        return response

    async def _attach_request_details(
        self, method: str, url: str, kwargs: Dict[str, Any]
    ) -> None:
        """
        Attach request details to Allure report for better debugging.

        Args:
            method: HTTP method
            url: Full URL
            kwargs: Request options
        """
        request_info = {
            "method": method,
            "url": url,
            "headers": kwargs.get("headers", {}),
            "params": kwargs.get("params", {}),
        }

        # Add payload information
        if kwargs.get("json_data"):
            request_info["json"] = kwargs["json_data"]
        elif kwargs.get("data"):
            request_info["data"] = kwargs["data"]

        allure.attach(
            json.dumps(request_info, indent=2),
            f"Request Details - {method}",
            AttachmentType.JSON,
        )

    async def _attach_response_details(self, response: APIResponse) -> None:
        try:
            # Attach response status and headers
            response_info = {
                "status": response.status,
                "status_text": response.status_text,
                "url": response.url,
                "headers": dict(response.headers),
                "ok": response.ok,
            }

            allure.attach(
                json.dumps(response_info, indent=2),
                f"Response Info - {response.status}",
                AttachmentType.JSON,
            )

            # Attach response body
            response_text = await response.text()

            # Try to format as JSON if possible
            try:
                json_data = json.loads(response_text)
                allure.attach(
                    json.dumps(json_data, indent=2),
                    f"Response Body - {response.status}",
                    AttachmentType.JSON,
                )
            except (json.JSONDecodeError, ValueError):
                # Not JSON, attach as text
                allure.attach(
                    response_text,
                    f"Response Body - {response.status}",
                    AttachmentType.TEXT,
                )

        except Exception as e:
            allure.attach(
                f"Failed to attach response details: {str(e)}",
                "Response Attachment Error",
                AttachmentType.TEXT,
            )
