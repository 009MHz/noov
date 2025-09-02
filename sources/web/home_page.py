from playwright.async_api import Page, expect
import re

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        
        # Loader element
        self.loader = page.locator(".loader-container")
        
        # Header elements
        self.language_toggle = page.locator("#languageToggle")
        self.logo = page.get_by_alt_text("noovoleum logo")
        self.hero_text = page.get_by_text("Making everybody a green energy champion")

        # Banner Mobile
        self.banner_mobile = page.locator("#about")
        self.apple_btn = self.banner_mobile.get_by_role('link').first
        self.android_btn = self.banner_mobile.get_by_role('link').nth(1)

        # Form Submit
        self.header_submit = page.get_by_text(re.compile(r"get in touch"))
        self.btn_send = page.get_by_role('link', name="Send Message")
        self.err_name = page.locator("#userNameError")
        self.err_email = page.locator("#userEmailError")
        self.err_message = page.locator("#userMessageError")
        self.input_name = page.get_by_role('textbox', name='Your Name')
        self.input_email = page.get_by_role("textbox", name="Email Address")
        self.input_message = page.get_by_role('textbox', name="Write Your Message Here")

        # Company Info
        self.info_logo = page.get_by_role('img', name='noovoleum white logo')
        self.company_sg_address = page.get_by_text(re.compile(r"NOOVOLEUM PTE\. LTD\..*189352 Singapore", re.DOTALL))
        self.company_id_address = page.get_by_text(re.compile(r"PT PMA Noovoleum Indonesia.*Jawa Barat", re.DOTALL))
        self.linkedin_link = page.get_by_role("link", name=" noovoleum")
        self.instagram_link = page.get_by_role('link').filter(has_text='noovoleumid')
        self.email_link = page.get_by_role('link').filter(has_text='contact@noovoleum.com')

    async def open(self, base_url: str = "https://noovoleum.com"):
        try:
            await expect(self.loader).to_be_hidden(timeout=10000)
        except:
            pass
        
        await self.page.goto(base_url, wait_until="domcontentloaded")
        return self

    async def fill_contact_form(self, name: str, email: str, message: str):
        await self.input_name.fill(name)
        await self.input_email.fill(email)
        await self.input_message.fill(message)

    async def click_send_message(self):
        await self.btn_send.click()

