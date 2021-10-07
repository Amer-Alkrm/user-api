
from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from db import engine, stakeholders
from model import StakeholderDataResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    This method is used to create JWT access token then return it
    """

    data_to_encode = data.copy()
    expire = (datetime.utcnow() + expires_delta
              ) if expires_delta else (datetime.utcnow() + timedelta(minutes=15))
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt


async def validate_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> bool:
    """
    This method is used to validate that the given token is correct(not modified) and the stakeholder is/still authorized
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=getenv("ALGORITHM"))
        username: str = payload.get("user")
        password: str = payload.get("pass")
        token_data = TokenData(username=username, password=password)
    except JWTError:
        raise credentials_exception
    with engine.connect() as conn:
        user_data = conn.execute(stakeholders.select().where(
            stakeholders.c.email == token_data.username)).first()
    if not user_data:
        raise credentials_exception
    if(not pwd_context.verify(user_data.password, token_data.password)):
        raise credentials_exception
    return True


async def current_stakeholder(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> StakeholderDataResponse:
    """
    This method is used to return the current authorized stakeholder information using the token as a input.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=getenv("ALGORITHM"))
        username: str = payload.get("user")
        password: str = payload.get("pass")
        token_data = TokenData(username=username, password=password)
    except JWTError:
        raise credentials_exception
    with engine.connect() as conn:
        stakeholder_data = conn.execute(stakeholders.select().where(
            stakeholders.c.email == token_data.username)).first()
    if not stakeholder_data:
        raise credentials_exception
    if(not pwd_context.verify(stakeholder_data.password, token_data.password)):
        raise credentials_exception
    return StakeholderDataResponse(**dict(stakeholder_data))


async def validate_admin(current_stackholder: StakeholderDataResponse = Depends(current_stakeholder)) -> bool:
    """
    This method is used check if the current authorized stakeholder is an admin or not.
    """

    if not current_stackholder.is_admin:
        raise HTTPException(
            status_code=400, detail="This stakeholder is not an Admin. only admins can create users.")
    return True


async def current_admin_email(current_stakeholder: StakeholderDataResponse = Depends(current_stakeholder)) -> str:
    """
    This method is used return the current authorized stakeholder is email.
    """

    if not current_stakeholder.is_admin:
        raise HTTPException(
            status_code=400, detail="This stakeholder is not an Admin. only admins can create users.")
    return current_stakeholder.email
