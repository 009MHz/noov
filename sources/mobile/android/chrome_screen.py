"""
Simple Chrome screen for mobile automation.

This module provides a basic ChromeScreen class for automating Chrome browser
on mobile devices, focusing on simple search functionality.
"""

from typing import List, Optional
from selenium.webdriver.common.by import By
from appium.webdriver.webelement import WebElement as AppiumWebElement
from sources.mobile.__base import BaseMobileScreen
import allure


class ChromeScreen(BaseMobileScreen):
    """
    Simple Chrome browser screen for mobile automation.
    
    Provides basic Chrome browser interactions:
    - Open Google homepage
    - Search functionality  
    - Result verification
    """

    # Chrome search elements as class attributes (following LoginPage pattern)
    search_selector = (By.ID, "com.android.chrome:id/url_bar")
    results_selector = (By.XPATH, "//*[contains(text(), 'Appium')]")

    # Intent methods using shortened base class methods
    async def open_google(self):
            # Navigate to Google
            await self._goto("https://www.google.com")
            
            # Wait for page to load
            await self._wait_visible(By.TAG_NAME, "body", timeout=15)
            

    async def search_keyword(self, keyword: str):
        search_box = self._find([self.search_selector])
        if not search_box:
            return
        await self._tap(search_box)
        await self._type(search_box, keyword)
        search_box.submit()
    

    async def verify_results_not_empty(self) -> bool:
        
        """
        Verify that search results are displayed and not empty.
        Returns True if any visible result is found, False otherwise.
        """
        try:
            await self._wait_visible(By.TAG_NAME, "body", timeout=10)
            by, value = self.results_selector
            results = self._find_all([self.results_selector])
            for element in results:
                if await self._visible(element):
                    return True
            await self.attach_screenshot_to_allure("No Visible Results")
            return False
        except Exception as e:
            await self.attach_screenshot_to_allure(f"Results Verification Failed: {str(e)}")
            return False
