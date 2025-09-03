import json
import time
from typing import Dict, List, Optional, Tuple
from playwright.async_api import APIResponse
from sources.api.__base import BaseService


class HomeClient:
    """API client for noovo/boxes endpoints."""
    
    def __init__(self, api_client: BaseService):
        self.api_client = api_client
        self.endpoint = "open_api/boxes"
        self._required_fields = {"name", "status", "location"}
        self._required_location_fields = {"latitude", "longitude"}
    
    async def get_noovo_list(self) -> APIResponse:
        """Get list of noovo items."""
        return await self.api_client.get(self.endpoint)
    
    async def get_noovo_by_id(self, noovo_id: str) -> APIResponse:
        """Get specific noovo item by ID."""
        return await self.api_client.get(f"{self.endpoint}/{noovo_id}")
    
    async def get_parsed_response(self, response: Optional[APIResponse] = None, measure_time: bool = False) -> Tuple[APIResponse, Optional[List[Dict]], float]:
        """Get and parse response with optional timing."""
        start_time = time.time() if measure_time else 0
        
        if response is None:
            response = await self.get_noovo_list()
        
        response_time = time.time() - start_time if measure_time else 0
        
        try:
            data = await response.json()
            return response, data, response_time
        except (json.JSONDecodeError, ValueError):
            return response, None, response_time
    
    async def get_validated_data(self) -> Tuple[APIResponse, List[Dict], List[str]]:
        """Get and validate noovo data structure."""
        response, data, _ = await self.get_parsed_response()
        validation_errors = []
        
        if not data:
            validation_errors.append("Failed to parse response as JSON")
            return response, [], validation_errors
        
        if not isinstance(data, list):
            validation_errors.append(f"Expected list response, got {type(data)}")
            return response, [], validation_errors
        
        return response, data, validation_errors
    
    async def get_first_item(self) -> Tuple[APIResponse, Optional[Dict]]:
        """Get first noovo item from the list."""
        response, data, _ = await self.get_parsed_response()
        
        if data and isinstance(data, list) and len(data) > 0:
            return response, data[0]
        return response, None
    
    def get_content_type(self, response: APIResponse) -> str:
        """Extract content type from response headers."""
        return response.headers.get("content-type", "")
    
    def validate_item_structure(self, item: Dict) -> List[str]:
        """Validate item structure and return errors."""
        errors = []
        missing_fields = self._required_fields - set(item.keys())
        if missing_fields:
            errors.append(f"Missing required fields: {missing_fields}")
        
        if "location" in item and item["location"]:
            location = item["location"]
            if not isinstance(location, dict):
                errors.append(f"Location should be dict, got {type(location)}")
            else:
                missing_loc_fields = self._required_location_fields - set(location.keys())
                if missing_loc_fields:
                    errors.append(f"Missing location fields: {missing_loc_fields}")
        
        return errors
    
    def extract_coordinates(self, item: Dict) -> Tuple[Optional[float], Optional[float], List[str]]:
        """Extract coordinates from item location."""
        errors = []
        latitude, longitude = None, None
        
        if "location" not in item:
            errors.append("No location field found")
            return latitude, longitude, errors
        
        location = item["location"]
        if not location:
            errors.append("Location field is empty")
            return latitude, longitude, errors
        
        if not isinstance(location, dict):
            errors.append(f"Location should be dict, got {type(location)}")
            return latitude, longitude, errors
        
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        
        return latitude, longitude, errors
    
    def validate_coordinates(self, latitude: Optional[float], longitude: Optional[float]) -> List[str]:
        """Validate coordinate values."""
        errors = []
        
        if latitude is not None:
            if not isinstance(latitude, (int, float)):
                errors.append(f"Latitude should be numeric, got {type(latitude)}")
            elif not -90 <= latitude <= 90:
                errors.append(f"Latitude should be between -90 and 90, got: {latitude}")
        
        if longitude is not None:
            if not isinstance(longitude, (int, float)):
                errors.append(f"Longitude should be numeric, got {type(longitude)}")
            elif not -180 <= longitude <= 180:
                errors.append(f"Longitude should be between -180 and 180, got: {longitude}")
        
        return errors
    
    async def execute_workflow(self) -> Tuple[APIResponse, Optional[Dict], APIResponse]:
        """Execute workflow: get list, then get first item details."""
        list_response, data, _ = await self.get_parsed_response()
        
        if not data or not isinstance(data, list) or len(data) == 0:
            detail_response = await self.get_noovo_by_id("non-existent")
            return list_response, None, detail_response
        
        first_item = data[0]
        item_id = first_item.get("id", "test-noovo-id")
        detail_response = await self.get_noovo_by_id(item_id)
        
        return list_response, first_item, detail_response
    
    @property
    def required_fields(self) -> set:
        """Get required fields for noovo items."""
        return self._required_fields
    
    @property
    def required_location_fields(self) -> set:
        """Get required location fields."""
        return self._required_location_fields
