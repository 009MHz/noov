import pytest

@pytest.mark.mobile
def test_android_login(android_driver):
    # Example sanity: app launched, main screen visibility
    assert android_driver.current_package is not None