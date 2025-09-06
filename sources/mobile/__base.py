"""
Optimized base mobile screen class for Android and iOS mobile testing.

This module provides the BaseMobileScreen class with only the most common functionality
that is actually used across mobile screen objects. Focused on essentials only.
"""

from typing import List, Optional, Tuple, Dict, Any, Sequence
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.mobile_config import aify
import allure


class BaseMobileScreen:
    """
    Optimized base class for mobile screen objects.

    Provides only the essential common functionality:
    - Element finding with fallback strategies
    - Core interactions (tap, type, visibility)
    - Basic waits
    - Essential navigation
    - Screenshot utilities
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the base mobile screen.

        Args:
            driver: Appium WebDriver instance
            timeout: Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # Core Element Finding (Essential)
    def _find(self, selectors: List[Tuple[str, str]]) -> Optional[AppiumWebElement]:
        """
        Try multiple selectors and return the first matching element.

        Args:
            selectors: List of (by_method, value) tuples to try in order

        Returns:
            WebElement if found, None otherwise
        """
        for by, value in selectors:
            try:
                return self.driver.find_element(by, value)
            except (NoSuchElementException, TimeoutException):
                continue
        return None

    def _find_all(self, selectors: List[Tuple[str, str]]) -> Sequence[AppiumWebElement]:
        """
        Try multiple selectors and return elements from the first matching selector.

        Args:
            selectors: List of (by_method, value) tuples to try in order

        Returns:
            Sequence of WebElements (empty list if none found)
        """
        for by, value in selectors:
            try:
                elements = self.driver.find_elements(by, value)
                if elements:  # Only return if we found at least one element
                    return elements
            except (NoSuchElementException, TimeoutException):
                continue
        return []

    # Core Interactions (Essential)
    @aify
    def _tap(self, element: AppiumWebElement):
        """Tap an element."""
        element.click()

    @aify
    def _type(self, element: AppiumWebElement, text: str, clear_first: bool = True):
        """Type text into an element."""
        if clear_first:
            element.clear()
        element.send_keys(text)

    @aify
    def _text(self, element: AppiumWebElement) -> str:
        """Get text from an element."""
        return element.text

    @aify
    def _visible(self, element: AppiumWebElement) -> bool:
        """Check if element is displayed."""
        try:
            return element.is_displayed()
        except:
            return False

    # Essential Waits
    @aify
    def _wait_visible(self, by: str, value: str, timeout: Optional[int] = None) -> bool:
        """Wait for element to be visible."""
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        try:
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    # Basic Navigation (Essential)
    @aify
    def _goto(self, url: str):
        """Navigate to URL (for web contexts in mobile browsers)."""
        self.driver.get(url)

    # Essential Page State
    @aify
    def _title(self) -> str:
        """Get current page title (for web contexts)."""
        try:
            return self.driver.title
        except:
            return ""

    @aify
    def _url(self) -> str:
        """Get current page URL (for web contexts)."""
        try:
            return self.driver.current_url
        except:
            return ""

    @aify
    def _source(self) -> str:
        """Get current page source."""
        return self.driver.page_source

    @aify
    def _contexts(self) -> List[str]:
        """Get available contexts (native, webview, etc.)."""
        try:
            return list(self.driver.contexts)
        except:
            return ["NATIVE_APP"]

    # Essential Screenshot Support
    @aify
    def _screenshot(self, filename: Optional[str] = None) -> str:
        """Take screenshot and return the file path."""
        if filename:
            filepath = f"reports/screenshots/{filename}.png"
        else:
            import time
            timestamp = int(time.time())
            filepath = f"reports/screenshots/mobile_screen_{timestamp}.png"

        self.driver.save_screenshot(filepath)
        return filepath

    @aify
    def _screenshot_bytes(self) -> bytes:
        """Get screenshot as bytes."""
        return self.driver.get_screenshot_as_png()

    async def attach_screenshot_to_allure(self, name: str = "Mobile Screenshot"):
        """Take screenshot and attach to Allure report."""
        screenshot_path = await self._screenshot()
        try:
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=name,
                    attachment_type=allure.attachment_type.PNG,
                )
        except FileNotFoundError:
            # Fallback: take screenshot as bytes
            screenshot_bytes = await self._screenshot_bytes()
            allure.attach(
                screenshot_bytes, name=name, attachment_type=allure.attachment_type.PNG
            )
