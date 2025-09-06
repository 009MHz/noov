"""
Mobile testing fixtures for Appium-based Android and iOS testing.

This module provides lightweight pytest fixtures that use mobile_config
for device setup and configuration management.
"""

import os
import asyncio
import pytest
import allure
from appium.webdriver.webdriver import WebDriver
from utils.mobile_config import get_android_driver_options, get_ios_driver_options, get_appium_server_url


@pytest.fixture(scope="function")
async def android_driver():
    """
    Create Android WebDriver instance for mobile testing.
    
    Uses mobile_config for all configuration management.
    Provides async-compatible driver for Chrome browser automation.
    """
    # Get configuration from mobile_config
    options = get_android_driver_options()
    server_url = get_appium_server_url()
    
    def create_driver():
        """Create driver in sync context."""
        return WebDriver(server_url, options=options)
    
    # Create driver using async bridge
    driver = await asyncio.to_thread(create_driver)
    
    try:
        yield driver
    finally:
        # Cleanup driver
        await asyncio.to_thread(driver.quit)


@pytest.fixture(scope="function") 
async def ios_driver():
    """
    Create iOS WebDriver instance for mobile testing.
    
    Uses mobile_config for all configuration management.
    Provides async-compatible driver for Safari browser automation.
    """
    # Get configuration from mobile_config
    options = get_ios_driver_options()
    server_url = get_appium_server_url()
    
    def create_driver():
        """Create driver in sync context."""
        return WebDriver(server_url, options=options)
    
    driver = await asyncio.to_thread(create_driver)
    
    try:
        yield driver
    finally:
        await asyncio.to_thread(driver.quit)


@pytest.fixture(scope="function")
async def mobile_capabilities():
    """
    Provide mobile device capabilities for testing.
    
    Returns:
        Dict with device information and capabilities
    """
    return {
        "android": {
            "platform": "Android",
            "automation": "UiAutomator2", 
            "browser": "Chrome",
            "device": os.getenv("ANDROID_DEVICE", "Android Emulator")
        },
        "ios": {
            "platform": "iOS",
            "automation": "XCUITest",
            "browser": "Safari", 
            "device": os.getenv("IOS_DEVICE", "iPhone Simulator")
        }
    }


@pytest.fixture(scope="function")
def mobile_test_data():
    """
    Test data fixture for mobile testing.
    
    Returns:
        Dict with test data for mobile scenarios
    """
    return {
        "search_keywords": ["Appium", "Selenium", "Mobile Testing"],
        "urls": {
            "google": "https://www.google.com",
            "bing": "https://www.bing.com"
        },
        "timeouts": {
            "short": 5,
            "medium": 10,
            "long": 30
        }
    }


# Helper fixtures for screenshot handling
@pytest.fixture(scope="function")
async def mobile_screenshot_handler(request):
    """
    Mobile screenshot handler for test failures.
    
    Automatically captures screenshots on test failure for mobile tests.
    """
    yield
    
    # Capture screenshot on test failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        driver = None
        
        # Try to get driver from test arguments
        for fixture_name in ["android_driver", "ios_driver"]:
            if fixture_name in request.fixturenames:
                driver = request.getfixturevalue(fixture_name)
                break
        
        if driver:
            try:
                screenshot_bytes = await asyncio.to_thread(driver.get_screenshot_as_png)
                allure.attach(
                    screenshot_bytes,
                    name="Mobile Test Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture mobile screenshot: {e}")


# Hook to mark test results for screenshot handling
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for mobile screenshot handling."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
