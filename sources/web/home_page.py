from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
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

    def open(self, base_url: str = "https://noovoleum.com"):
        self.page.goto(base_url)
        return self

    def open_contact(self, base_url: str = "https://noovoleum.com"):
        self.page.goto(base_url + "#contact")
        return self

    def toggle_language(self):
        self.language_toggle.click()
        return self

    def submit_contact(self, name: str = "", email: str = "", message: str = ""):
        if name:
            self.input_name.fill(name)
        if email:
            self.input_email.fill(email)
        if message:
            self.input_message.fill(message)
        self.btn_send.click()
        return self

    # Assertions inside PO for reuse in smoke/regression suites
    def assert_hero_and_logo(self):
        expect(self.logo).to_be_visible()
        expect(self.hero_text).to_be_visible()
        return self

    def assert_switched_to_indonesian(self):
        expect(self.page).to_have_url(lambda url: url.endswith("/id"))
        return self

    def assert_required_errors(self):
        expect(self.err_name).to_have_text("Name is required")
        expect(self.err_email).to_have_text("Email is required")
        expect(self.err_message).to_have_text("Message is required")
        return self

    def assert_invalid_email_error(self):
        expect(self.err_email).to_have_text("Email must be valid")
        return self
