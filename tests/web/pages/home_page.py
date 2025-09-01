from playwright.sync_api import Page, expect

class HomePage:
    """Page object for the Noovoleum home page."""
    URL = "https://noovoleum.com/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.language_toggle = page.locator("#languageToggle")
        self.tagline = page.locator("text=Making everybody a green energy champion")

    def goto(self) -> None:
        """Navigate to the home page."""
        self.page.goto(self.URL)

    def assert_loaded(self) -> None:
        """Assert that key elements on the page are visible."""
        expect(self.language_toggle).to_be_visible()
        expect(self.tagline).to_be_visible()
