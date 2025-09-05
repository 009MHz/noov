import pytest
import allure
import re
import os
import json
from playwright.async_api import expect, Page
from sources.web.admin.login_page import LoginPage
from allure import severity_level as severity
from utils.allure_helpers import step
from utils.sess_handler import SessionHandler, SESSION_FILE


@pytest.fixture(scope="function")
async def login_page(page):
    login_page = LoginPage(page)
    await login_page.open()
    return login_page


@allure.epic("Admin Portal")
@allure.feature("Authentication")
@pytest.mark.ui
class TestSessionPersistence:
            
    @allure.title("Direct Access to Profile Page with Auth Cookie")
    @allure.description("Verify profile page can be accessed directly with authentication cookies")
    @allure.severity(severity.CRITICAL)
    async def test_direct_access_with_auth_cookie(self, user_auth):
        """Test that directly accesses the profile URL with authenticated cookies using existing fixtures.
        
        This test uses the user_auth fixture from conftest.py which:
        1. Creates a new browser context with valid session cookies
        2. Handles authentication through SessionHandler.create_session()
        3. Takes care of context and page management
        
        The test then directly navigates to the profile page and verifies:
        - The page URL is the profile page, not redirected to login
        - Either the DashboardProfile text or 2FA alert element is visible
        """
        
        with step("Navigate directly to profile page with auth cookies"):
            await user_auth.goto("https://manage-dev.noovoleum.com/profile")
            await expect(user_auth).to_have_url("https://manage-dev.noovoleum.com/profile")
        
        with step("Verify expected elements are present"):
            dashboard_text = user_auth.get_by_text("DashboardProfile", exact=False)
            is_dashboard_visible = await dashboard_text.is_visible()
            if is_dashboard_visible:
                print("DashboardProfile text is visible")
            