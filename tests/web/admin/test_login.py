import pytest
import allure
import re
import os
from playwright.async_api import expect, Page
from sources.web.admin.login_page import LoginPage
from allure import severity_level
from utils.allure_helpers import step


@pytest.fixture(scope='function')
async def login_page(page):
    login_page = LoginPage(page)
    await login_page.open()
    return login_page


@pytest.fixture(scope='class')
def credentials():
    """Centralized fixture for all environment variables used in tests"""
    return {
        # User credentials
        "user_email": os.getenv("USER_EMAIL"),
        "user_password": os.getenv("USER_PASSWORD"),
        
        # Admin credentials
        "admin_email": os.getenv("ADMIN_EMAIL"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        
        # 2FA credentials
        "user_2fa_email": os.getenv("USER_2FA_EMAIL"),
        "user_2fa_password": os.getenv("USER_2FA_PASSWORD"),
        "user_2fa_code": os.getenv("USER_2FA_CODE"),
        
        # Test data
        "invalid_email": os.getenv("INVALID_TEST_EMAIL", "invalid@example.com"),
        "invalid_format_email": os.getenv("INVALID_FORMAT_EMAIL", "test@example"),
        "invalid_tfa_code": os.getenv("INVALID_TFA_CODE", "000000"),
        "test_email": os.getenv("TEST_EMAIL", "test@example.com")
    }


@allure.epic("Admin Portal")
@allure.feature("Authentication")
@pytest.mark.ui
class TestLogin:
    @allure.title("Successful login without 2FA")
    @allure.description("User logs in with valid credentials and no 2FA")
    @allure.severity(severity_level.CRITICAL)
    async def test_login_success_without_2fa(self, login_page, page: Page, credentials):
        if not credentials["user_email"] or not credentials["user_password"]:
            pytest.skip("User credentials not configured in environment variables")
        
        with step("Verify login page elements"):
            await expect(login_page.logo).to_be_visible()
            await expect(login_page.welcome_text).to_be_visible()
            await expect(login_page.sign_in_text).to_be_visible()
            
        with step("Login with valid credentials without 2FA"):
            await login_page.login(
                email=credentials["user_email"], 
                password=credentials["user_password"]
            )

        with step("Verify successful redirect to secure area"):
            await expect(page).to_have_url(re.compile(r"/profile"))

    @allure.title("Successful login with 2FA")
    @allure.description("User logs in with valid credentials and valid 2FA code")
    @allure.severity(severity_level.CRITICAL)
    @pytest.mark.skip(reason="Need valid 2FA code for automated testing")
    async def test_login_success_with_2fa(self, login_page, page: Page, credentials):
        if not all([
            credentials["user_2fa_email"], 
            credentials["user_2fa_password"], 
            credentials["user_2fa_code"]
        ]):
            pytest.skip("2FA test credentials not configured in environment variables")
            
        with step("Login with valid credentials and 2FA"):
            await login_page.login(
                email=credentials["user_2fa_email"], 
                password=credentials["user_2fa_password"], 
                tfa_code=credentials["user_2fa_code"]
            )

        with step("Verify successful redirect to secure area"):
            await page.wait_for_url(re.compile(r"/dashboard"))
            await expect(page).to_have_url(re.compile(r"/dashboard"))
    
    @allure.title("Login with invalid credentials")
    @allure.description("User attempts login with incorrect email or password")
    @allure.severity(severity_level.NORMAL)
    async def test_login_with_invalid_credentials(self, login_page, page: Page, credentials):
        if not credentials["user_email"]:
            pytest.skip("User email not configured in environment variables")
            
        with step("Login with invalid email"):
            await login_page.login(
                email=credentials["invalid_email"], 
                password="WrongPassword"
            )
            
        with step("Validate visual indicators show authentication failed"):
            await expect(login_page.email_invalid_err).to_be_visible()
            
        with step("Login with invalid password"):
            await login_page.login(
                email=credentials["user_email"],
                password="WrongPassword"
            )
            
        with step("Validate visual indicators show authentication failed"):
            await expect(login_page.password_invalid_err).to_be_visible()
            
        with step("Verify user stays on login page"):
            await expect(page).to_have_url(re.compile(r"/login"))
            await expect(login_page.login_button).to_be_visible()
    
    @allure.title("Login with invalid 2FA code")
    @allure.description("User attempts login with correct email/password but incorrect 2FA code")
    @allure.severity(severity_level.NORMAL)
    async def test_login_with_invalid_2fa(self, login_page, page: Page, credentials):
        if not credentials["admin_email"] or not credentials["admin_password"]:
            pytest.skip("Admin credentials not configured in environment variables")
            
        with step("Login with valid credentials but invalid 2FA"):
            await login_page.login(
                email=credentials["admin_email"],
                password=credentials["admin_password"],
                tfa_code=credentials["invalid_tfa_code"]
            )
            
        with step("Validate visual indicators show authentication failed"):
            await expect(login_page.tfa_invalid_err).to_be_visible()
        
        with step("Verify user stays on login page"):
            await expect(page).to_have_url(re.compile(r"/login"))
            await expect(login_page.login_button).to_be_visible()
            
    
    @allure.title("Login form validation - empty fields")
    @allure.description("Verify form validation when submitting with empty fields")
    @allure.severity(severity_level.NORMAL)
    async def test_login_empty_fields_validation(self, login_page: LoginPage):
        with step("Click login with empty fields"):
            await login_page.click_login()
            
        with step("Verify validation errors"):
            await expect(login_page.email_empty_err).to_be_visible()
            await expect(login_page.password_empty_err).to_be_visible()
    
    @allure.title("Login form validation - invalid email format")
    @allure.description("Verify form validation when using invalid email format")
    @allure.severity(severity_level.NORMAL)
    async def test_login_invalid_email_format(self, login_page, page: Page, credentials):
        with step("Enter invalid email format"):
            await login_page.fill_email(credentials["invalid_format_email"])
            await login_page.fill_password("TestPassword123")
            await login_page.click_login()
            
        with step("Verify email validation is indicated"):
            await expect(login_page.email_invalid_err).to_be_visible()

        with step("Verify we're still on login page"):
            await expect(page).to_have_url(re.compile(r"/login"))

    @allure.title("Login page refresh clears inputs")
    @allure.description("Verify that refreshing the login page clears all inputs")
    @allure.severity(severity_level.MINOR)
    async def test_login_page_refresh_clears_inputs(self, login_page, page: Page, credentials):
        with step("Fill form fields"):
            await login_page.fill_email(credentials["test_email"])
            await login_page.fill_password("TestPassword123")
            await login_page.fill_2fa_code(credentials["invalid_tfa_code"])
            
        with step("Reload page and verify inputs are cleared"):
            await page.reload()
            
            # Check that fields are empty using expect
            await expect(login_page.email_input).to_have_value("")
            await expect(login_page.password_input).to_have_value("")
            await expect(login_page.tfa_input).to_have_value("")
    
