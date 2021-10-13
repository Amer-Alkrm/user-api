
import pytest
from fastapi.exceptions import HTTPException
from pytest_mock import MockerFixture

from model import StakeholderDataRequest, StakeholderDataResponse
from services.authentication import (
    create_access_token, current_admin_email, current_stakeholder, validate_admin, validate_token
)


def test_create_access_token(mock_access_token: str, mock_user_data_access_token: dict) -> None:
    access_token = create_access_token(data=mock_user_data_access_token)
    assert access_token[37:95] == mock_access_token[37:95]


@pytest.mark.asyncio
@pytest.mark.parametrize('correct_password', [(True), (False)])
@pytest.mark.parametrize('access_token_found', [(True), (False)])
@pytest.mark.parametrize('found_data', [(True), (False)])
async def test_validate_token(mock_access_token: str, mock_access_token_empty: str,
                              mocker: MockerFixture, mock_response_stakeholder_data: dict,
                              found_data: bool, access_token_found: bool,
                              correct_password: True) -> None:

    mock_connect = mocker.patch('services.authentication.engine.connect')

    stakeholder_data = StakeholderDataResponse(
        **mock_response_stakeholder_data)
    with pytest.raises(HTTPException):
        if not correct_password:
            stakeholder_data.password = 'hello'
        if found_data:
            mock_connect.return_value.__enter__.return_value.execute.return_value\
                .first.return_value = stakeholder_data
        else:
            mock_connect.return_value.__enter__.return_value.execute.return_value\
                .first.return_value = None

        if access_token_found:
            result = await validate_token(mock_access_token)
        else:
            await validate_token(mock_access_token_empty)

        assert result is True
        raise HTTPException(status_code=200, detail='to get out of pytest raise with no errors.')


@pytest.mark.asyncio
@pytest.mark.parametrize('correct_password', [(True), (False)])
@pytest.mark.parametrize('access_token_found', [(True), (False)])
@pytest.mark.parametrize('found_data', [(True), (False)])
async def test_current_stakeholder(mocker: MockerFixture, mock_access_token: str,
                                   mock_access_token_empty: str,
                                   mock_response_stakeholder_data: dict,
                                   found_data: bool, access_token_found: bool,
                                   correct_password: bool) -> None:

    mock_connect = mocker.patch('services.authentication.engine.connect')

    stakeholder_data = StakeholderDataResponse(
        **mock_response_stakeholder_data)
    with pytest.raises(HTTPException):
        if not correct_password:
            stakeholder_data.password = 'hello'
        if found_data:
            mock_connect.return_value.__enter__.return_value.execute.return_value\
                .first.return_value = stakeholder_data
        else:
            mock_connect.return_value.__enter__.return_value.execute.return_value\
                .first.return_value = None

        if access_token_found:
            result = await current_stakeholder(mock_access_token)
        else:
            await current_stakeholder(mock_access_token_empty)

        assert result == stakeholder_data
        raise HTTPException(status_code=200, detail='to get out of pytest raise with no errors.')


@pytest.mark.asyncio
@pytest.mark.parametrize('is_admin', [(True), (False)])
async def test_validate_admin(mock_request_stakeholder_data: dict, is_admin: bool) -> None:
    stakeholder_data = StakeholderDataRequest(
        **mock_request_stakeholder_data)
    if not is_admin:
        stakeholder_data.is_admin = False
    result = await validate_admin(stakeholder_data)
    assert result is is_admin


@pytest.mark.asyncio
async def test_current_admin_email(mock_request_stakeholder_data: dict) -> None:
    stakeholder_data = StakeholderDataRequest(
        **mock_request_stakeholder_data)
    result = await current_admin_email(stakeholder_data)
    assert result == mock_request_stakeholder_data['email']
