from playwright.async_api import Page, expect
from typing import Optional
import re

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Header elements
        self.logo = page.get_by_role('img', name='logo', exact=True)
        self.welcome_text = page.get_by_text("Welcome Back !")
        self.sign_in_text = page.get_by_text("Sign in to continue.")
        
        # Form elements
        self.email_label = page.get_by_label("Email")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.email_empty_err = page.get_by_text('Please Enter Your Email')
        self.email_invalid_err = page.get_by_text('Invalid Email')

        self.password_label = page.get_by_label("Password")
        self.password_input = page.get_by_role('textbox', name='Enter Password')
        self.password_eye_icon = page.get_by_role('button', name='󰈉')
        self.password_empty_err = page.get_by_text('Please Enter Your Password')
        self.password_invalid_err = page.get_by_text('Invalid Password')

        self.tfa_label = page.get_by_label("2FA Code (if enabled)")
        self.tfa_input = page.get_by_role('textbox', name='Enter code from authenticator')
        self.tfa_invalid_err = page.get_by_text('Invalid OTP Code')
        
        self.login_button = page.get_by_role("button", name="Log In")

    async def open(self, base_url: str = "https://manage-dev.noovoleum.com/login"):
        await self.page.goto(base_url)
        await self.page.wait_for_load_state("load")
        return self

    async def fill_email(self, email: str):
        await self.email_input.fill(email)
    
    async def fill_password(self, password: str):
        await self.password_input.fill(password)
    
    async def fill_2fa_code(self, code: str):
        await self.tfa_input.fill(code)

    async def toggle_password_visibility(self):
        await self.password_eye_icon.click()
    
    async def click_login(self):
        await self.login_button.click()
    
    async def fill_credentials(self, email: str, password: str, tfa_code: Optional[str] = None):
        """Fill all login form fields in one go without submitting."""
        await self.fill_email(email)
        await self.fill_password(password)
        if tfa_code:
            await self.fill_2fa_code(tfa_code)

    async def login(self, email: str, password: str, tfa_code: Optional[str] = None):
        await self.fill_credentials(email, password, tfa_code)
        await self.click_login()