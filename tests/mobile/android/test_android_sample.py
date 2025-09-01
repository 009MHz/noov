import os
import pytest

appium = pytest.importorskip("appium", reason="Appium not installed")


@pytest.fixture
def android_driver():
    app = os.environ.get("ANDROID_APP")
    if not app:
        pytest.skip("ANDROID_APP environment variable not set")
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "app": app,
    }
    server = os.environ.get("APPIUM_SERVER", "http://localhost:4723/wd/hub")
    driver = appium.webdriver.Remote(server, caps)
    yield driver
    driver.quit()


def test_launch_android_app(android_driver):
    assert android_driver.session_id
