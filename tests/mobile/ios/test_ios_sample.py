import os
import pytest

appium = pytest.importorskip("appium", reason="Appium not installed")


@pytest.fixture
def ios_driver():
    app = os.environ.get("IOS_APP")
    if not app:
        pytest.skip("IOS_APP environment variable not set")
    caps = {
        "platformName": "iOS",
        "automationName": "XCUITest",
        "app": app,
    }
    server = os.environ.get("APPIUM_SERVER", "http://localhost:4723/wd/hub")
    driver = appium.webdriver.Remote(server, caps)
    yield driver
    driver.quit()


def test_launch_ios_app(ios_driver):
    assert ios_driver.session_id
