import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.config.settings import get_settings


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def test_settings():
    return get_settings()
