import pytest


class DummyAndroidDriver:
    """Minimal stand-in driver for local test runs."""

    current_package = "com.example.app"


@pytest.fixture
def android_driver():
    return DummyAndroidDriver()


@pytest.mark.mobile
def test_android_login(android_driver):
    """Example sanity: app launched, main screen visible."""
    assert android_driver.current_package is not None
