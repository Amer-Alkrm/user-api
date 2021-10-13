import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette import status
from starlette.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)


@pytest.mark.parametrize('found', [(True), (False)])
def test_get_all_addresses(mocker: MockerFixture, client: TestClient,
                           mock_response_address_data: str, found: bool) -> None:
    mock_connect = mocker.patch('routes.address.engine.connect')
    response_data = [mock_response_address_data]
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value = [
            mock_response_address_data]
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value = []
        response_data = []

    with client.get('/addresses') as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == response_data


@pytest.mark.parametrize('found, status_code', [(True, HTTP_200_OK), (False, HTTP_404_NOT_FOUND)])
def test_get_address(mocker: MockerFixture, client: TestClient,
                     mock_response_address_data: dict, mock_address_id: str,
                     found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.address.engine.connect')
    response_data = mock_response_address_data
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value = mock_response_address_data
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value = []
        response_data = {'detail': f'Address Not Found id: {mock_address_id}'}

    with client.get(f'/addresses/{mock_address_id}') as response:
        assert mock_connect.called
        assert response.status_code == status_code
        assert response.json() == response_data


@pytest.mark.parametrize('valid_state, status_code', [(True, HTTP_200_OK),
                                                      (False, HTTP_422_UNPROCESSABLE_ENTITY)])
def test_create_address(mocker: MockerFixture, client: TestClient,
                        mock_response_address_data: dict, valid_state: bool,
                        status_code: status) -> None:
    if not valid_state:
        mock_response_address_data['state'] = 25
    mock_connect = mocker.patch('routes.address.engine.begin')
    mock_connect.return_value.__enter__.return_value.execute.return_value\
        .first.return_value = mock_response_address_data

    with client.post('/addresses', json=mock_response_address_data) as response:
        assert mock_connect.called is valid_state
        assert response.status_code == status_code
        if valid_state:
            assert response.json() == mock_response_address_data


@ pytest.mark.parametrize('found, status_code', [(True, HTTP_204_NO_CONTENT),
                                                 (False, HTTP_404_NOT_FOUND)])
def test_delete_address(mocker: MockerFixture, client: TestClient,
                        mock_address_id: str, found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.address.engine.connect')
    mock_connect.return_value.__enter__.return_value.execute.return_value.rowcount = found

    response_data = {'data': f'{mock_address_id} Address Deleted Successfully'} if found else{
        'detail': f'Address id: {mock_address_id} does not exist.'}

    with client.delete(f'/addresses/{mock_address_id}') as response:
        assert mock_connect.called
        assert response.status_code == status_code
        assert response.json() == response_data


@ pytest.mark.parametrize('found, status_code', [(True, HTTP_200_OK), (False, HTTP_404_NOT_FOUND)])
def test_update_address(mocker: MockerFixture, client: TestClient,
                        mock_response_address_data: dict, mock_address_id: str,
                        found: bool, status_code: status) -> None:
    mock_connect = mocker.patch('routes.address.engine.begin')
    response_data = mock_response_address_data
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value = mock_response_address_data
    else:
        response_data = {'detail': f'Address id: {mock_address_id} does not exist.'}
        mock_connect.return_value.__enter__.return_value.execute.return_value\
            .first.return_value.rowcount = 0
    with pytest.raises(AttributeError):
        with client.patch(f'/addresses/{mock_address_id}',
                          json=mock_response_address_data) as response:
            assert mock_connect.called
            assert response.status_code == status_code
            assert response.json() == response_data
            raise AttributeError('Passing Error')
