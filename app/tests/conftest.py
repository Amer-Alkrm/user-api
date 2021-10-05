from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture()
def client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture()
def mock_response_user_data() -> dict:
    return {
        'id': str(uuid4()),
        'user_name': 'cc',
        'first_name': 'cc',
        'last_name': 'cc',
        'email': 'ameralkrm@gmail.com',
        'age': 25,
        'address_id': str(uuid4()),
        'degree': 2,
        'created_by_email': 'amer@gmail.com',
        'gender': 2,
        'created_at': str(datetime.utcnow()).replace(' ', 'T'),
        'updated_at': str(datetime.utcnow()).replace(' ', 'T'),
    }


@pytest.fixture()
def mock_user_id() -> str:
    return str(uuid4())


@pytest.fixture()
def mock_response_address_data() -> dict:
    return {
        'id': str(uuid4()),
        'address': 'efefef',
        'street': 'efef',
        'state': 2,
        'zip_code': 6,
        'apartment_number': 5,
        'created_at': str(datetime.utcnow()).replace(' ', 'T'),
        'updated_at': str(datetime.utcnow()).replace(' ', 'T'),
    }


@ pytest.fixture()
def mock_address_id() -> str:
    return str(uuid4())
