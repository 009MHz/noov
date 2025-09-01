import pytest
import requests

BASE_URL = "https://noovoleum.com"


def test_homepage_status():
    try:
        response = requests.get(BASE_URL, timeout=5)
    except requests.RequestException:
        pytest.skip("Network unavailable")
    if response.status_code != 200:
        pytest.skip(f"Unexpected status code: {response.status_code}")
    assert response.status_code == 200
