from playwright.async_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.language_toggle = page.locator("#languageToggle")
        self.hero_heading = page.get_by_text("Making everybody a green energy champion")
        self.logo = page.get_by_alt_text("noovoleum logo")
        self.send_message_btn = page.locator("#send-message-btn")
        self.name_input = page.get_by_placeholder("Your Name")
        self.email_input = page.get_by_placeholder("Email Address")
        self.message_textarea = page.get_by_placeholder("Write Your Message Here")
        self.email_error = page.locator("#userEmailError")
        self.name_error = page.locator("#userNameError")
        self.message_error = page.locator("#userMessageError")

    async def goto(self, base_url: str):
        await self.page.goto(base_url)

    async def toggle_language(self):
        await self.language_toggle.click()
