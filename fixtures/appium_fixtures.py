import pytest
from appium import webdriver
from libs.config_loader import load_settings

@pytest.fixture(scope="function")
def android_driver():
    s = load_settings()
    caps = {
        "platformName": "Android",
        "app": "apps/android/app-release.apk",
        "automationName": "UiAutomator2",
        "deviceName": "Pixel_7_API_34",
        "newCommandTimeout": 300,
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def ios_driver():
    caps = {
        "platformName": "iOS",
        "automationName": "XCUITest",
        "deviceName": "iPhone 15",
        "platformVersion": "17.5",
        "app": "apps/ios/App.app",
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    yield driver
    driver.quit()