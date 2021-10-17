from datetime import datetime, timedelta
from os import getenv
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient
from main import app
from pydantic import BaseModel

from routes.token import OAuth2PasswordRequestForm
from services.authentication import (
    current_admin_email, current_stakeholder, validate_admin, validate_token
)
from services.redis import redis_client


class Form(BaseModel):
    username: str
    password: str


def mocking_auth_token_validation() -> bool:
    return True


def mocking_auth_admin_email() -> str:
    return 'amer@gmail.com'


def mocking_auth_is_admin_true() -> bool:
    return True


def mocking_auth_is_admin_false() -> bool:
    return False


def mocking_req_form() -> dict:
    return Form(**dict({'username': 'amer', 'password': 'string'}))


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
    app.dependency_overrides[validate_admin] = mocking_auth_is_admin_true
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


@ pytest.fixture()
def clear_redis_cache() -> None:
    redis_client.flushall()


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
async def mock_access_token(mock_user_data_access_token: dict) -> str:
    return jwt.encode(mock_user_data_access_token, key=getenv('SECRET_KEY'),
                      algorithm=getenv('ALGORITHM'))


@pytest.fixture()
async def mock_access_token_empty() -> str:
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzIjoiJDJiJDEyJFZvUE1CR1NR' +\
        'b0RZbnRrT0VwM1lhZXVDamowQ01jeTR4UGdqT2lUV1BuUVhOWU1LaTcxLlV5IiwiZXhw' +\
        'IjoyMjI0MzM1NTEzMDN9.ti-MTIwbG8YJxmq0H8e1jZwCbr2L40sinP7fNtoYzWk'


@pytest.fixture()
def mock_user_data() -> dict:
    return {'email': 'amer@gmail.com', 'password': 'string'}


@pytest.fixture()
def mock_user_data_access_token() -> dict:
    return {'user': 'user@example.com',
            'pass': '$2b$12$VoPMBGSQoDYntkOEp3YaeuCjj0CMcy4xPgjOiTWPnQXNYMKi71.Uy'}


@pytest.fixture()
def token_response_data(mock_access_token):
    return {"access_token": mock_access_token,
            "token_type": "bearer",
            'EXPIRE_MINUTES': int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
            'EXPIRE_DATE_IN_UTC': datetime.now() + timedelta(
                minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))}
