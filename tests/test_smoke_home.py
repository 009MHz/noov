import pytest
import allure
import time
from sources.pages.pg_home import HomePage
from elements.el_home import HomeElements
import logging

logger = logging.getLogger(__name__)


@allure.epic("Noovoleum Website Smoke Tests")
@allure.feature("Homepage Functionality")
class TestSmokeHome:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixture"""
        self.page = HomePage(driver)
        self.elements = HomeElements()
        # Don't store driver as self.driver - use it through the page object or parameter

    @allure.story("Page Load and Basic Elements")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_page_load_and_basic_elements(self, driver):
        """TC001: Verify page loads correctly and essential elements are present"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()

        with allure.step("Wait for preloader to disappear"):
            preloader_disappeared = self.page.wait_for_preloader_to_disappear()
            assert preloader_disappeared, "Preloader did not disappear within timeout"

        with allure.step("Verify page title"):
            title = self.page.get_page_title()
            assert "noovoleum" in title.lower(), f"Page title does not contain 'noovoleum': {title}"

        with allure.step("Verify main logo is displayed"):
            assert self.page.is_logo_displayed(), "Main logo is not displayed"

        with allure.step("Verify language toggle button"):
            assert self.page.is_language_toggle_displayed(), "Language toggle button is not displayed"
            toggle_text = self.page.get_language_toggle_text()
            assert toggle_text == self.elements.TestData.LANGUAGE_TOGGLE_TEXT, \
                f"Language toggle text incorrect. Expected: {self.elements.TestData.LANGUAGE_TOGGLE_TEXT}, Got: {toggle_text}"

        with allure.step("Verify banner content"):
            is_valid, checks = self.page.verify_banner_content()
            assert is_valid, f"Banner content verification failed: {checks}"

            tagline = self.page.get_tagline_text()
            assert self.elements.TestData.EXPECTED_TAGLINE in tagline, \
                f"Expected tagline not found. Got: {tagline}"

        with allure.step("Take screenshot of loaded page"):
            self.page.take_screenshot("page_loaded_successfully")

    @allure.story("Language Toggle")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_language_toggle_functionality(self, driver):
        """TC002: Verify language toggle button functionality"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Verify initial URL is Indonesian version"):
            current_url = self.page.get_current_url()
            assert self.elements.URLs.BASE_URL in current_url, \
                f"Not on Indonesian page. Current URL: {current_url}"

        with allure.step("Click language toggle button"):
            self.page.click_language_toggle()

        with allure.step("Verify redirect to English version"):
            redirect_success = self.page.verify_english_page_redirect()
            assert redirect_success, "Did not redirect to English version"

        with allure.step("Verify English page loads"):
            self.page.wait_for_page_load()
            current_url = self.page.get_current_url()
            assert self.elements.URLs.ENGLISH_URL in current_url, \
                f"Not redirected to English URL. Current URL: {current_url}"

    @allure.story("UCOllect Process Steps")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_ucollect_process_steps(self, driver):
        """TC003: Verify all 4 UCOllect process steps are displayed correctly"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Scroll to UCOllect section"):
            self.page.scroll_to_ucollect_section()

        with allure.step("Verify UCOllect logo is displayed"):
            assert self.page.is_ucollect_logo_displayed(), "UCOllect logo is not displayed"

        with allure.step("Verify all 4 process steps"):
            all_valid, step_results = self.page.verify_all_process_steps()
            assert all_valid, f"Process steps verification failed: {step_results}"

        with allure.step("Take screenshot of process steps"):
            self.page.take_screenshot("ucollect_process_steps")

    @allure.story("App Download Links")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_app_download_functionality(self, driver):
        """TC004: Verify mobile app download functionality"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Scroll to app download section"):
            self.page.scroll_to_app_download_section()

        with allure.step("Verify app download title is displayed"):
            assert self.page.is_app_download_title_displayed(), "App download title is not displayed"
            title = self.page.get_app_download_title()
            assert "UCOllect" in title, f"App title does not mention UCOllect: {title}"

        with allure.step("Verify app download description"):
            description = self.page.get_app_download_description()
            assert len(description) > 0, "App download description is empty"

        with allure.step("Verify App Store button is displayed"):
            assert self.page.is_app_store_button_displayed(), "App Store button is not displayed"

        with allure.step("Verify Google Play button is displayed"):
            assert self.page.is_google_play_button_displayed(), "Google Play button is not displayed"

        with allure.step("Verify App Store link URL"):
            assert self.page.verify_app_store_link_url(), "App Store link URL is incorrect"

        with allure.step("Verify Google Play link URL"):
            assert self.page.verify_google_play_link_url(), "Google Play link URL is incorrect"

        with allure.step("Test App Store button click"):
            original_windows = driver.window_handles
            self.page.click_app_store_button()
            time.sleep(2)

            # Check if new tab opened or redirected
            if len(driver.window_handles) > len(original_windows):
                driver.switch_to.window(driver.window_handles[-1])
                current_url = self.page.get_current_url()
                assert "onelink.me" in current_url, f"App Store link did not redirect correctly: {current_url}"
                driver.close()
                driver.switch_to.window(original_windows[0])

        with allure.step("Take screenshot of app download section"):
            self.page.take_screenshot("app_download_section")

    @allure.story("Contact Form")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_contact_form_functionality(self, driver):
        """TC005: Verify contact form validation and submission"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Scroll to contact section"):
            self.page.scroll_to_contact_section()

        with allure.step("Verify contact form is displayed"):
            assert self.page.is_contact_form_displayed(), "Contact form is not displayed"

        with allure.step("Verify contact form title"):
            title = self.page.get_contact_title()
            assert len(title) > 0, "Contact form title is empty"

        with allure.step("Test form with valid data"):
            self.page.fill_contact_form(
                self.elements.TestData.VALID_NAME,
                self.elements.TestData.VALID_EMAIL,
                self.elements.TestData.VALID_MESSAGE
            )

            # Click send button
            self.page.click_send_message_button()
            time.sleep(2)  # Wait for form processing

        with allure.step("Test empty form submission"):
            self.page.clear_contact_form()
            self.page.click_send_message_button()
            time.sleep(1)

        with allure.step("Take screenshot of contact form"):
            self.page.take_screenshot("contact_form_section")

    @allure.story("Footer Information")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_footer_information_and_links(self, driver):
        """TC006: Verify footer content and social media links"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Scroll to footer section"):
            self.page.scroll_to_footer_section()

        with allure.step("Verify footer logo is displayed"):
            assert self.page.is_footer_logo_displayed(), "Footer logo is not displayed"

        with allure.step("Verify social media link URLs"):
            assert self.page.verify_linkedin_link_url(), "LinkedIn URL is incorrect"
            assert self.page.verify_instagram_link_url(), "Instagram URL is incorrect"
            assert self.page.verify_email_link(), "Email link is incorrect"

        with allure.step("Test social media links"):
            original_windows = driver.window_handles

            # Test LinkedIn link
            self.page.click_linkedin_link()
            time.sleep(2)
            if len(driver.window_handles) > len(original_windows):
                driver.close()
                driver.switch_to.window(original_windows[0])

        with allure.step("Verify copyright text"):
            copyright_text = self.page.get_copyright_text()
            assert "2024" in copyright_text, f"Copyright year not found: {copyright_text}"
            assert "noovoleum" in copyright_text.lower(), f"Company name not in copyright: {copyright_text}"

        with allure.step("Take screenshot of footer"):
            self.page.take_screenshot("footer_section")

    @allure.story("Page Navigation and Scrolling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_navigation_and_scrolling(self, driver):
        """TC007: Verify smooth scrolling and navigation behavior"""
        with allure.step("Navigate to homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()

        with allure.step("Test scrolling through entire page"):
            self.page.scroll_through_entire_page()

        with allure.step("Verify navbar remains visible during scroll"):
            # Scroll down and check if navbar is still present
            self.page.scroll_to_contact_section()
            assert self.page.is_displayed(self.elements.Header.NAVBAR), "Navbar not visible during scroll"

        with allure.step("Test logo click navigation"):
            self.page.click_logo()
            time.sleep(1)
            # Verify page scrolled to top or refreshed
            current_url = self.page.get_current_url()
            assert self.elements.URLs.BASE_URL in current_url, "Logo click did not work correctly"

        with allure.step("Take screenshot after navigation test"):
            self.page.take_screenshot("navigation_complete")

    @allure.story("Performance and Loading")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_performance_and_loading(self, driver):
        """TC008: Verify website performance and loading times"""
        with allure.step("Navigate to homepage and measure load time"):
            start_time = time.time()
            self.page.navigate_to_homepage()
            self.page.wait_for_page_load()
            self.page.wait_for_preloader_to_disappear()
            load_time = time.time() - start_time

        with allure.step("Verify page loads within acceptable time"):
            assert load_time < 30, f"Page load time too slow: {load_time}s > 30s"

        with allure.step("Verify all images are loaded"):
            images_loaded, failed_images = self.page.verify_all_images_loaded()
            assert images_loaded, f"Some images failed to load: {failed_images}"

        with allure.step("Take screenshot after performance test"):
            self.page.take_screenshot("performance_test_complete")


@allure.epic("Noovoleum Website Smoke Tests")
@allure.feature("End-to-End User Journey")
class TestE2EUserJourney:
    """End-to-end user journey tests"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup test fixture"""
        self.page = HomePage(driver)
        self.elements = HomeElements()

    @allure.story("Complete User Journey")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_complete_user_journey(self, driver):
        """Test complete user journey from landing to contact form submission"""
        with allure.step("User lands on homepage"):
            self.page.navigate_to_homepage()
            self.page.wait_for_preloader_to_disappear()
            self.page.take_screenshot("user_lands_on_page")

        with allure.step("User reads main content and tagline"):
            tagline = self.page.get_tagline_text()
            description = self.page.get_description_text()
            assert len(tagline) > 0 and len(description) > 0, "Main content not visible"

        with allure.step("User scrolls to learn about UCOllect process"):
            self.page.scroll_to_ucollect_section()
            all_valid, _ = self.page.verify_all_process_steps()
            assert all_valid, "UCOllect process steps not properly displayed"
            self.page.take_screenshot("user_views_process_steps")

        with allure.step("User checks mobile app download options"):
            self.page.scroll_to_app_download_section()
            assert self.page.is_app_store_button_displayed(), "App Store button not visible"
            assert self.page.is_google_play_button_displayed(), "Google Play button not visible"
            self.page.take_screenshot("user_views_app_download")

        with allure.step("User decides to contact company"):
            self.page.scroll_to_contact_section()
            assert self.page.is_contact_form_displayed(), "Contact form not accessible"

        with allure.step("User fills and submits contact form"):
            self.page.submit_contact_form_with_test_data()
            self.page.take_screenshot("user_submits_contact_form")

        with allure.step("User checks company information in footer"):
            self.page.scroll_to_footer_section()
            assert self.page.is_footer_logo_displayed(), "Footer information not available"
            self.page.take_screenshot("user_views_company_info")

        with allure.step("Complete user journey successful"):
            allure.attach(
                "User successfully completed the entire journey from landing to contact submission",
                name="Journey Summary",
                attachment_type=allure.attachment_type.TEXT
            )
