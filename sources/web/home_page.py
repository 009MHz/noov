from playwright.async_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # Modern, resilient locators
        self.language_toggle = page.locator("#languageToggle")
        self.logo = page.get_by_alt_text("noovoleum logo")
        self.hero_text = page.get_by_text("Making everybody a green energy champion")
        # Contact form
        self.btn_send = page.locator("#send-message-btn")
        self.err_name = page.locator("#userNameError")
        self.err_email = page.locator("#userEmailError")
        self.err_message = page.locator("#userMessageError")
        self.input_name = page.get_by_placeholder("Your Name")
        self.input_email = page.get_by_placeholder("Email Address")
        self.input_message = page.get_by_placeholder("Write Your Message Here")

    async def open(self, base_url: str = "https://noovoleum.com"):
        # Prefer network idle only if app is SPA-heavy; otherwise 'load' is fine.
        await self.page.goto(base_url, wait_until="domcontentloaded")
        # Guard against race conditions by asserting key UI is visible
        await expect(self.logo).to_be_visible()
        await expect(self.hero_text).to_be_visible()
        return self

    async def open_contact(self, base_url: str = "https://noovoleum.com#contact"):
        await self.page.goto(base_url, wait_until="domcontentloaded")
        # Ensure contact form is ready before interacting
        await expect(self.btn_send).to_be_enabled()
        return self

    async def fill_contact_form(self, name: str, email: str, message: str):
        await self.input_name.fill(name)
        await self.input_email.fill(email)
        await self.input_message.fill(message)

    async def submit_contact(self):
        await self.btn_send.click()

    async def expect_validation_errors(self):
        await expect(self.err_name).to_be_visible()
        await expect(self.err_email).to_be_visible()
        await expect(self.err_message).to_be_visible()
