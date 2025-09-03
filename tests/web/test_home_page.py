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
@allure.feature("Homepage")
@pytest.mark.ui
class TestHomepage:
    @allure.title("Homepage Header validation")
    @allure.feature("Home/ Heading")
    @allure.severity(severity.NORMAL)
    async def test_homepage_logo_and_heading(self, home, platform):
        allure.step("Verify key header UI")
        await expect(home.logo).to_be_visible()
        await expect(home.hero_text).to_be_visible()
        
        allure.step("Verify language toggle")
        await expect(home.language_toggle).to_be_visible()
        await expect(home.language_toggle).to_contain_text("Indonesian")
        await expect(home.language_toggle).to_be_enabled()

    @allure.title("Homepage Mobile Banner validation")
    @allure.feature("Home/ Mobile Banner")
    @allure.severity(severity.NORMAL)
    async def test_homepage_mobile_banner(self, home, platform):
        allure.step("Verify mobile app banner")
        await expect(home.banner_mobile).to_be_visible()
        await expect(home.apple_btn).to_have_attribute("href", re.compile(r"noovoleum\.onelink\.me"))
        await expect(home.android_btn).to_have_attribute("href", re.compile(r"noovoleum\.onelink\.me"))

    @allure.title("Homepage Banner Steps validation")
    @allure.feature("Home/ Process Banner")
    @allure.severity(severity.CRITICAL)
    async def test_homepage_process_steps(self, home, platform):
        allure.step("Verify the steps banner")

        steps = [
            (home.step1_image, home.step1_desc, "Step 1"),
            (home.step2_image, home.step2_desc, "Step 2"),
            (home.step3_image, home.step3_desc, "Step 3"),
            (home.step4_image, home.step4_desc, "Step 4")
        ]
        
        for image, desc, step_name in steps:
            allure.step(f"Verify {step_name} content")
            await expect(image).to_be_visible()
            await expect(desc).to_be_visible()


    @allure.title("Homepage Contact Banner validation")
    @allure.feature("Home/ Contact Banner")
    @allure.severity(severity.CRITICAL)
    async def test_homepage_contact_section(self, home, platform): 
        allure.step("Verify submit form elements")
        await expect(home.header_submit).to_be_visible()
        await expect(home.input_name).to_be_visible()
        await expect(home.input_email).to_be_visible()
        await expect(home.input_message).to_be_visible()
        await expect(home.btn_send).to_be_visible()
        
        allure.step("Verify company information")
        await expect(home.info_logo).to_be_visible()
        await expect(home.company_sg_address).to_be_visible()
        await expect(home.company_id_address).to_be_visible()
        await expect(home.linkedin_link).to_have_attribute("href", re.compile(r"linkedin\.com/company/noovoleum"))
        await expect(home.instagram_link).to_have_attribute("href", re.compile(r"instagram\.com/noovoleumid"))
        await expect(home.email_link).to_be_visible()
        
    @allure.title("Homepage Footer validation")
    @allure.feature("Home/ Footer")
    @allure.severity(severity.MINOR)
    async def test_homepage_footer_section(self, home, platform): 
        allure.step("Verify footer elements")
        await expect(home.footer).to_be_visible()
        await expect(home.copyright_text).to_be_visible()
        await expect(home.self_declaration_link).to_have_attribute("href", re.compile(r"self-declaration"))
        await expect(home.privacy_policy_link).to_have_attribute("href", re.compile(r"privacy-policy"))
        await expect(home.terms_conditions_link).to_have_attribute("href", re.compile(r"terms-and-conditions-2024"))
