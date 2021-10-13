import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette import status
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('found, status_code', [(True, HTTP_200_OK),
                                                (False, HTTP_401_UNAUTHORIZED)])
def test_login_for_token(mocker: MockerFixture, mock_access_token: str, mock_user_data: dict,
                         client: TestClient, found: bool, status_code: status,
                         token_response_data: dict) -> None:
    mock_connect = mocker.patch('routes.token.engine.connect')
    mock_create_access_token = mocker.patch('routes.token.create_access_token')
    mock_create_access_token.return_value = mock_access_token

    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value = mock_user_data
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value = []
        token_response_data = {'detail': 'Incorrect username or password'}

    with client.post('/token') as response:
        assert mock_connect.called
        assert response.status_code == status_code
        assert response.json()['access_token'] == token_response_data[
            'access_token'] if found else response.json() == token_response_data


def test_get_current_stakeholder(client: TestClient, mock_request_stakeholder_data: dict) -> None:

    with client.get('/token') as response:
        assert response.status_code == HTTP_200_OK
        assert response.json() == mock_request_stakeholder_data
