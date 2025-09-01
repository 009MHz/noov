import pytest
from libs.config_loader import load_settings

@pytest.fixture(scope="function")
async def api(request, pw):
    s = load_settings(env=request.config.getoption("--env"))
    ctx = await pw.request.new_context(base_url=s.api_url,
                                       extra_http_headers={"Accept":"application/json"})
    yield ctx
    await ctx.dispose()