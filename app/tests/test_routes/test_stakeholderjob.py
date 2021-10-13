
import runpy

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.exc import IntegrityError


def my_side_effect():
    raise IntegrityError(None, None, None)


@pytest.mark.parametrize('no_error', [(True), (False)])
def test_stakeholderjob(mocker: MockerFixture, no_error: bool) -> None:

    if no_error:
        mock_connect = mocker.patch(
            'sqlalchemy.orm.session.Session.execute', side_effect=[True, False])
    else:
        mock_connect = mocker.patch('sqlalchemy.orm.session.Session.execute',
                                    side_effect=IntegrityError(None, None, None))

        mock_rollback = mocker.patch('sqlalchemy.orm.session.Session.rollback')
        mock_rollback.return_value = True

    runpy.run_path('app/jobs/stakeholderjob.py', run_name='__main__')
    assert mock_connect.called
