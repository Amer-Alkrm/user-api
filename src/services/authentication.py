
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt


async def validate_token(token: str = Depends(oauth2_scheme)) -> bool:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=getenv("ALGORITHM"))
        username: str = payload.get("user")
        password: str = payload.get("pass")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password)
    except JWTError:
        raise credentials_exception
    with engine.connect() as conn:
        user_data = conn.execute(stakeholders.select().where(
            stakeholders.c.email == token_data.username)).first()
    if(not pwd_context.verify(user_data.password, token_data.password)):
        raise credentials_exception
    if user_data is None:
        raise credentials_exception
    return True


async def current_user(token: str = Depends(oauth2_scheme)) -> StakeholderDataResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=getenv("ALGORITHM"))
        username: str = payload.get("user")
        password: str = payload.get("pass")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password)
    except JWTError:
        raise credentials_exception
    with engine.connect() as conn:
        user_data = conn.execute(stakeholders.select().where(
            stakeholders.c.email == token_data.username)).first()
    if(not pwd_context.verify(user_data.password, token_data.password)):
        raise credentials_exception
    if user_data is None:
        raise credentials_exception
    return StakeholderDataResponse(**dict(user_data))


async def validate_admin(current_user: StakeholderDataResponse = Depends(current_user)) -> bool:
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="This user is not an Admin.")
    return True
