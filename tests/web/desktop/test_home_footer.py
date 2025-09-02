import re
import pytest
import allure
from playwright.async_api import expect
from sources.web.home_page import HomePage
from allure import severity_level as severity


@pytest.fixture(scope='function')
async def home(page):
    home = HomePage(page)
    await home.open()
    return home


@allure.epic("Marketing Site")
@allure.feature("Footer")
@pytest.mark.ui
class TestFooter:
    @allure.title("Footer Container and Copyright Text")
    @allure.feature("Footer/ Copyright")
    @allure.severity(severity.NORMAL)
    async def test_footer_copyright(self, home):
        allure.step("Verify footer container and copyright text")
        await expect(home.footer).to_be_visible()
        await expect(home.copyright_text).to_be_visible()
        await expect(home.copyright_text).to_contain_text("2024")
        await expect(home.copyright_text).to_contain_text("noovoleum")

    @allure.title("Footer Links Validation")
    @allure.feature("Footer/ Links")
    @allure.severity(severity.NORMAL)
    async def test_footer_links(self, home):
        allure.step("Verify footer links visibility")
        await expect(home.self_declaration_link).to_be_visible()
        await expect(home.privacy_policy_link).to_be_visible()
        await expect(home.terms_conditions_link).to_be_visible()
        
        allure.step("Verify footer links attributes")
        footer_links = [
            (home.self_declaration_link, "self-declaration"),
            (home.privacy_policy_link, "privacy-policy"),
            (home.terms_conditions_link, "terms-and-conditions-2024")
        ]
        
        for link, href_pattern in footer_links:
            allure.step(f"Verify link with pattern: {href_pattern}")
            await expect(link).to_have_attribute("href", re.compile(href_pattern))
            await expect(link).to_have_attribute("target", "_blank")
