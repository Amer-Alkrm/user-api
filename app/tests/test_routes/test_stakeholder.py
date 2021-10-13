import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from starlette.status import HTTP_200_OK


@pytest.mark.parametrize('found', [(True), (False)])
def test_get_all_stakeholders(mocker: MockerFixture, client: TestClient,
                              mock_response_stakeholder_data: dict, found: bool) -> None:
    mock_connect = mocker.patch('routes.stakeholder.engine.connect')
    response_data = [mock_response_stakeholder_data]
    if found:
        mock_connect.return_value.__enter__.return_value.execute.return_value = [
            mock_response_stakeholder_data]
    else:
        mock_connect.return_value.__enter__.return_value.execute.return_value = []
        response_data = []
    with client.get('/admin/stakeholders') as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == response_data


def test_create_address(mocker: MockerFixture, client: TestClient,
                        mock_response_stakeholder_data: dict) -> None:
    mock_connect = mocker.patch('routes.stakeholder.engine.begin')
    mock_connect.return_value.__enter__.return_value.execute.return_value\
        .first.return_value = mock_response_stakeholder_data

    with client.post('/admin/stakeholders', json=mock_response_stakeholder_data) as response:
        assert mock_connect.called
        assert response.status_code == HTTP_200_OK
        assert response.json() == mock_response_stakeholder_data
