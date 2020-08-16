import pytest
from starlette.testclient import TestClient

from src.extensions import metadata
from src.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        metadata.create_all()
        yield client
        metadata.drop_all()
