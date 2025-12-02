import pytest
from zendfi.client import ZendFi


@pytest.fixture
def client():
    return ZendFi(api_key="test_key", base_url="http://localhost:5555")
