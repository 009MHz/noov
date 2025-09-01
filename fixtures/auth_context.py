import pytest, json
from pathlib import Path
from libs.config_loader import load_settings

@pytest.fixture(scope="session")
async def auth_storage(browser):
    s = load_settings()
    path = Path(s.storage_state_path)
    if path.exists():
        return str(path)
    ctx = await browser.new_context()
    page = await ctx.new_page()
    # TODO: Implement domain login once; fill credentials from env
    await page.goto("https://app.example.com/login")
    await page.get_by_label("Email").fill("${USER_EMAIL}")
    await page.get_by_label("Password").fill("${USER_PASSWORD}")
    await page.get_by_role("button", name="Sign in").click()
    await page.wait_for_url("**/dashboard")
    await ctx.storage_state(path=str(path))
    await ctx.close()
    return str(path)

@pytest.fixture(scope="function")
async def session_context(browser, auth_storage):
    ctx = await browser.new_context(storage_state=auth_storage)
    yield ctx
    await ctx.close()