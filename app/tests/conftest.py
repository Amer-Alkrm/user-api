from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from main import app
from pydantic import BaseModel

from routes.token import OAuth2PasswordRequestForm
from services.authentication import (
    TokenData, current_admin_email, current_stakeholder, validate_admin, validate_token
)


def mocking_auth_token_validation() -> bool:
    return True


def mocking_auth_admin_email() -> str:
    return 'amer@gmail.com'


def mocking_auth_is_admin() -> bool:
    return True


def mocking_req_form() -> TokenData:
    return TokenData(**{'username': 'amer', 'password': 'string'})


def mocking_current_stackholder() -> dict:
    return {
        'email': 'amer@gmail.com',
        'password': 'string',
        'created_by_email': 'amer@gmail.com',
        'is_admin': True,
    }


@pytest.fixture()
def client() -> TestClient:
    app.dependency_overrides[validate_token] = mocking_auth_token_validation
    app.dependency_overrides[current_admin_email] = mocking_auth_admin_email
    app.dependency_overrides[validate_admin] = mocking_auth_is_admin
    app.dependency_overrides[OAuth2PasswordRequestForm] = mocking_req_form
    app.dependency_overrides[current_stakeholder] = mocking_current_stackholder
    client = TestClient(app)
    yield client


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


@pytest.fixture()
def mock_response_stakeholder_data() -> dict:
    return {
        'id': str(uuid4()),
        'email': 'amer@gmail.com',
        'password': 'string',
        'created_by_email': 'amer@gmail.com',
        'is_admin': True,
        'created_at': str(datetime.utcnow()).replace(' ', 'T'),
        'updated_at': str(datetime.utcnow()).replace(' ', 'T'),
    }


@pytest.fixture()
def mock_request_stakeholder_data() -> dict:
    return {
        'email': 'amer@gmail.com',
        'password': 'string',
        'created_by_email': 'amer@gmail.com',
        'is_admin': True,
    }


@ pytest.fixture()
def mock_stakeholder_id() -> str:
    return str(uuid4())


@pytest.fixture()
async def mock_access_token() -> str:
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidXNlckBleGFtcGxlLmNvbSIsInBhc3MiOiIkMmIkMTIkVm9QTUJHU1FvRFludGtPRXAzWWFldUNqajBDTWN5NHhQZ2pPaVRXUG5RWE5ZTUtpNzEuVXkiLCJleHAiOjIyMjQzMzU1MTMwM30.ALMxc1YKFc7G8YHZjDvM_UWoYTTMJi7i_89V6cQrscE'


@pytest.fixture()
async def mock_access_token_empty() -> str:
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzIjoiJDJiJDEyJFZvUE1CR1NRb0RZbnRrT0VwM1lhZXVDamowQ01jeTR4UGdqT2lUV1BuUVhOWU1LaTcxLlV5IiwiZXhwIjoyMjI0MzM1NTEzMDN9.ti-MTIwbG8YJxmq0H8e1jZwCbr2L40sinP7fNtoYzWk'


class User_data(BaseModel):
    email: str
    password: str


@pytest.fixture()
def mock_user_data() -> User_data:
    return User_data(**{'email': 'amer@gmail.com', 'password': 'string'})
