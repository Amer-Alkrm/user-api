
from datetime import datetime, timedelta
from os import getenv

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql import select

from db import engine, stakeholders
from model import StakeholderDataResponse
from services.authentication import Token, create_access_token, current_stakeholder, pwd_context

router = APIRouter()


@ router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """
    Takes username and password to authorize the stakeholder and returns the stakeholder's access token and the access token expiration date.
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
async def get_current_stakeholder(current_stakeholder_data: StakeholderDataResponse = Depends(current_stakeholder)) -> JSONResponse:
    """
    Returns all the information for the current authorized stakeholder
    """

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=encoder(current_stakeholder_data))
