
from os import getenv

from sqlalchemy.exc import IntegrityError

from db import Session, stakeholders
from services.log import logger

default_stakeholder = {'email': getenv('DEF_EMAIL'),
                       'password': getenv('DEF_PASS'),
                       'is_admin': bool(getenv('DEF_ADMIN'))}


def delete_and_add_default_stakeholders() -> None:
    """
    This job deletes all available stakeholders from the database.
    """
    logger.info('Stakeholderjob has started..')
    logger.warning('All stakeholders data will be deleted from the database!!')

    with Session.begin() as conn:
        try:
            conn.execute(stakeholders.delete())
            logger.info('Successfully deleted all stakeholders.')
            logger.info('creating default stakeholder..')
            conn.execute(stakeholders.insert().values(
                default_stakeholder,
            ))
            logger.info('Successfully created.')
        except (IntegrityError):
            conn.rollback()
            logger.error("An error has occured while deleting and adding default stakeholder.")
            logger.info("Rolled back.")


if __name__ == "__main__":
    delete_and_add_default_stakeholders()
