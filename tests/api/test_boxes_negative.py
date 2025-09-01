import pytest

@pytest.mark.api
def test_invalid_path_returns_non_200(api_request):
    r = api_request.get("/open_api/boxes/does-not-exist")
    assert not r.ok
