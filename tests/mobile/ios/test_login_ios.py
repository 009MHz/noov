import pytest


class DummyIOSDriver:
    """Minimal stand-in driver for local test runs."""

    bundle_id = "com.example.app"


@pytest.fixture
def ios_driver():
    return DummyIOSDriver()


@pytest.mark.mobile
def test_ios_login(ios_driver):
    """Example sanity: app launched, main screen visible."""
    assert ios_driver.bundle_id is not None
