import pytest
from utils.mobile_config import ensure_native_app_context
from tests.fixtures.appium_fixtures import android_driver

# This file ensures the android_driver fixture is available to all tests in this directory and below.
__all__ = ["android_driver"]

@pytest.fixture(autouse=True)
async def ensure_native_context_on_start(android_driver):
	"""
	Ensure NATIVE_APP context is set at the start of every test using android_driver.
	"""
	await ensure_native_app_context(android_driver)
