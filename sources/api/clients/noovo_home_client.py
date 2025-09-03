import json
import time
from typing import Dict, List, Optional, Any, Tuple
from playwright.async_api import APIResponse
from sources.api.__base import BaseService


class HomeClient:
    """Home API page object with action logic only."""
    
    def __init__(self, api_client: BaseService):
        """Initialize with base API client."""
        self.api_client = api_client
        self.endpoint = "open_api/boxes"  # Using existing boxes endpoint
    
    async def get_noovo_list(self) -> APIResponse:
        """Get the list of noovo items."""
        return await self.api_client.get(self.endpoint)
    
    async def get_noovo_by_id(self, noovo_id: str) -> APIResponse:
        """Get specific noovo item by ID."""
        return await self.api_client.get(f"{self.endpoint}/{noovo_id}")
    
    async def get_parsed_noovo_list(self) -> Tuple[APIResponse, Optional[List[Dict]]]:
        """Get noovo list and parse JSON response."""
        response = await self.get_noovo_list()
        
        try:
            data = await response.json()
            return response, data
        except (json.JSONDecodeError, ValueError):
            return response, None
    
    async def get_response_time(self) -> Tuple[APIResponse, float]:
        """Measure response time for noovo list endpoint."""
        start_time = time.time()
        response = await self.get_noovo_list()
        end_time = time.time()
        
        response_time = end_time - start_time
        return response, response_time
    
    async def get_content_type(self) -> Tuple[APIResponse, str]:
        """Get response and extract content type header."""
        response = await self.get_noovo_list()
        content_type = response.headers.get("content-type", "")
        return response, content_type
    
    async def get_first_noovo_item(self) -> Tuple[APIResponse, Optional[Dict]]:
        """Get the first noovo item from the list."""
        response, data = await self.get_parsed_noovo_list()
        
        if data and isinstance(data, list) and len(data) > 0:
            return response, data[0]
        else:
            return response, None
    
    async def check_all_items_structure(self) -> Tuple[APIResponse, List[Dict], List[str]]:
        """Get all noovo items and return structure information for validation."""
        response, data = await self.get_parsed_noovo_list()
        validation_errors = []
        
        if not data:
            validation_errors.append("Failed to parse response as JSON")
            return response, [], validation_errors
        
        if not isinstance(data, list):
            validation_errors.append(f"Expected list response, got {type(data)}")
            return response, [], validation_errors
        
        return response, data, validation_errors
    
    async def get_item_coordinates(self, item: Dict) -> Tuple[Optional[float], Optional[float], List[str]]:
        """Extract coordinates from a noovo item."""
        validation_errors = []
        latitude, longitude = None, None
        
        if "location" not in item:
            validation_errors.append("No location field found")
            return latitude, longitude, validation_errors
        
        location = item["location"]
        if not location:
            validation_errors.append("Location field is empty")
            return latitude, longitude, validation_errors
        
        if not isinstance(location, dict):
            validation_errors.append(f"Location should be dict, got {type(location)}")
            return latitude, longitude, validation_errors
        
        # Extract latitude
        if "latitude" in location:
            latitude = location["latitude"]
        
        # Extract longitude  
        if "longitude" in location:
            longitude = location["longitude"]
        
        return latitude, longitude, validation_errors
    
    async def get_workflow_data(self) -> Tuple[APIResponse, Optional[Dict], APIResponse]:
        """Execute workflow: get list, then get first item details."""
        # Get list
        list_response, data = await self.get_parsed_noovo_list()
        
        if not data or not isinstance(data, list) or len(data) == 0:
            # Return empty detail response if no items
            detail_response = await self.get_noovo_by_id("non-existent")
            return list_response, None, detail_response
        
        # Get first item
        first_item = data[0]
        item_id = first_item.get("id", "test-noovo-id")
        
        # Get item details
        detail_response = await self.get_noovo_by_id(item_id)
        
        return list_response, first_item, detail_response
    
    def get_required_fields(self) -> set:
        """Get the set of required fields for noovo items."""
        return {"name", "status", "location"}
    
    def get_required_location_fields(self) -> set:
        """Get the set of required location fields."""
        return {"latitude", "longitude"}
