import pytest

pytest.importorskip("playwright.sync_api")
pytest.importorskip("pytest_playwright")

from tests.web.pages.home_page import HomePage


def test_home_page_loads(page):
    home = HomePage(page)
    home.goto()
    home.assert_loaded()
