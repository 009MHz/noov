import pytest
from libs.config_loader import load_settings
from web.pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.smoke
async def test_login(session_context):
    s = load_settings()
    page = await session_context.new_page()
    lp = LoginPage(page)
    await lp.open(s.base_url)
    # already authenticated via storageState; assert dashboard
    await page.wait_for_url("**/dashboard")