import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette import status
from starlette.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)


@pytest.mark.parametrize('found', [(True), (False)])
def test_get_all_users(mocker: MockerFixture, client: TestClient,
                       mock_response_user_data: dict, found: bool) -> None:
    mock_connect = mocker.patch('routes.user.engine.connect')
    response_data = [mock_response_user_data]
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value = [
            mock_response_user_data]
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value = []
        response_data = []
    with client.get('/users') as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == response_data


@pytest.mark.parametrize('found', [(True), (False)])
def test_get_user_by_gender(mocker: MockerFixture, client: TestClient,
                            mock_response_user_data: dict, found: bool) -> None:
    mock_connect = mocker.patch('routes.user.engine.connect')
    response_data = [mock_response_user_data]
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value = [
            mock_response_user_data]
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value = []
        response_data = []

    with client.get('/users/gender', params={'gender': 2}) as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == response_data


@pytest.mark.parametrize('found, status_code', [(True, HTTP_200_OK), (False, HTTP_404_NOT_FOUND)])
def test_get_user(mocker: MockerFixture, client: TestClient,
                  mock_response_user_data: dict, mock_user_id: str,
                  found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.user.engine.connect')
    response_data = [mock_response_user_data]
    if found:
        (mock_connect.return_value.__enter__.return_value.execute.return_value
         ).fetchall.return_value = [
            mock_response_user_data]
    else:
        (mock_connect.return_value.__enter__.return_value.execute.return_value
         ).fetchall.return_value = []
        response_data = {'detail': f'User Not Found id: {mock_user_id}'}

    with client.get(f'/users/{mock_user_id}') as response:
        assert mock_connect.called
        assert response.status_code == status_code
        assert response.json() == response_data


def test_create_user(mocker: MockerFixture, client: TestClient,
                     mock_response_user_data: dict) -> None:
    mock_connect = mocker.patch('routes.user.engine.begin')
    (mock_connect.return_value.__enter__.return_value.execute.return_value
     ).first.return_value = mock_response_user_data

    with client.post('/users', json=mock_response_user_data) as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == mock_response_user_data


@ pytest.mark.parametrize('flag', [(True), (False)])
def test_create_user_validator(mocker: MockerFixture, client: TestClient,
                               mock_response_user_data: dict, flag: bool) -> None:
    if(flag):
        mock_response_user_data['gender'] = 5
    else:
        mock_response_user_data['degree'] = 5
    mock_connect = mocker.patch('routes.user.engine.begin')
    (mock_connect.return_value.__enter__.return_value.execute.return_value
     ).first.return_value = mock_response_user_data

    with client.post('/users', json=mock_response_user_data) as response:
        assert mock_connect.called is False
        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


@ pytest.mark.parametrize('found, status_code', [(True, HTTP_204_NO_CONTENT),
                                                 (False, HTTP_404_NOT_FOUND)])
def test_delete_user(mocker: MockerFixture, client: TestClient,
                     mock_response_user_data: dict, mock_user_id: str,
                     found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.user.engine.connect')
    mock_connect.return_value.__enter__.return_value.execute.return_value.rowcount = found
    response_data = {'data': f'{mock_user_id} User Deleted Successfully'} if found else {
        'detail': f'User id: {mock_user_id} does not exist.'}
    with client.delete(f'/users/{mock_user_id}', json=mock_response_user_data) as response:
        assert mock_connect.called
        assert response.status_code == status_code
        assert response.json() == response_data


@ pytest.mark.parametrize('found, status_code', [(True, HTTP_200_OK), (False, HTTP_404_NOT_FOUND)])
def test_update_user(mocker: MockerFixture, client: TestClient,
                     mock_response_user_data: dict, mock_user_id: str,
                     found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.user.engine.begin')
    response_data = mock_response_user_data
    if found:
        (mock_connect.return_value.__enter__.return_value
         ).execute.return_value = mock_response_user_data
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value.rowcount = 0
        response_data = {'detail': f'User id: {mock_user_id} does not exist.'}
    with pytest.raises(AttributeError):
        with client.patch(f'/users/{mock_user_id}', json=mock_response_user_data) as response:
            assert mock_connect.called
            assert response.status_code == status_code
            assert response.json() == response_data
            raise AttributeError('Passing Error')
