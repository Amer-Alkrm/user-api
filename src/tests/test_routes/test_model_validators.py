from src.model import UserDataRequest, AddressDataRequest
import pytest


def test_validators():

    with pytest.raises(ValueError):
        UserDataRequest.check_degree(6)

    with pytest.raises(ValueError):
        UserDataRequest.check_gender(3)

    with pytest.raises(ValueError):
        AddressDataRequest.check_state(16)
