

import datetime
from datetime import datetime, timedelta
from os import getenv

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql import select

from db import engine, stakeholders
from model import StakeholderDataResponse, StakeholderDataRequest
from services.authentication import Token, create_access_token, current_user, pwd_context

router = APIRouter()


@ router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Takes username and password to authorize the user and returns the user's access token and the access token expiration date.
    """

    with engine.connect() as conn:
        user_data = conn.execute(select(stakeholders).where(stakeholders.c.email == form_data.username)
                                 .where(stakeholders.c.password == form_data.password)).first()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"user": user_data.email, 'pass': pwd_context.hash(user_data.password)}, expires_delta=timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=encoder(
                            {"access_token": access_token, "token_type": "bearer", 'EXPIRE_MINUTES': int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
                             'EXPIRE_DATE_IN_UTC': datetime.now() + timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))}))


@ router.get("/token")
async def get_current_user(current_user_data: StakeholderDataResponse = Depends(current_user)) -> JSONResponse:
    """
    Returns all the information for the current authorized user
    """

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=encoder(current_user_data))


# STAKEHOLDERS

@router.get('/admin/stakeholders')
async def get_all_stakeholders():
    """
    Returns all available stakeholders in the database.
    """

    with engine.connect() as conn:
        stakeholders_data = conn.execute(stakeholders.select()).fetchall()
        if not stakeholders_data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=[])

        return stakeholders_data


@router.post('/admin/stakeholders')
async def create_stakeholder(inserted_stakeholder_data: StakeholderDataRequest):
    """
    Creates a new stakeholder with the filled data.
    """

    with engine.begin() as conn:
        result = conn.execute(stakeholders.insert().returning(stakeholders).values(
            **inserted_stakeholder_data.dict(),
        )).first()
        return result
