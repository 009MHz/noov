import pytest
import allure
from sources.web.home_page import HomePage
from allure import severity_level as severity


@pytest.fixture(scope='function')
async def home(page):
    home = HomePage(page)
    await home.open()
    return home


@allure.epic("Marketing Site")
@allure.feature("Home/ Footer")
@pytest.mark.ui
class TestFooter:
    @allure.title("Validate Footer Links Navigation ")
    @allure.severity(severity.NORMAL)
    @pytest.mark.parametrize(
        "link_type, path",
        [
            ("Self Declaration", "/self-declaration"),
            ("Privacy Policy", "/privacy-policy"),
            ("Terms and Conditions", "/terms-and-conditions-2024"),
        ]
    )
    async def test_footer_link_navigation(self, home, context, link_type, path):
        allure.step(f"Click {link_type} link and wait for new tab")
        async with context.expect_page() as new_page_info:
            if link_type == "Self Declaration":
                await home.click_self_declaration()
            elif link_type == "Privacy Policy":
                await home.click_privacy_policy()
            elif link_type == "Terms and Conditions":
                await home.click_terms_conditions()
        
        allure.step(f"Switch to the new opened tab")
        new_page = await new_page_info.value
        await new_page.wait_for_load_state("networkidle")
        
        allure.step(f"Verify the URL redirection")
        assert new_page.url.endswith(path), f"Expected URL to end with {path}, but got {new_page.url}"
