from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from enums import Degree, Gender, State, all_enum_to_str


class UserDataRequest(BaseModel):
    address_id: UUID
    user_name: str
    first_name: str
    last_name: str
    age: int = Field(ge=10, le=100)
    degree: int
    gender: int
    email: EmailStr

    @validator('degree')
    def check_degree(cls, value: int) -> int:
        if value not in [e.value for e in Degree]:
            raise ValueError(f'Degree must one of {all_enum_to_str(Degree)}')
        return value

    @validator('gender')
    def check_gender(cls, value: int) -> int:
        if value not in [e.value for e in Gender]:
            raise ValueError(f'Gender must one of {all_enum_to_str(Gender)}')
        return value


class AddressDataRequest(BaseModel):
    address: str
    street: str
    state: int
    zip_code: Optional[int] = Field(lt=100000)
    apartment_number: int

    @validator('state')
    def check_state(cls, value: int) -> int:
        if value not in [e.value for e in State]:
            raise ValueError(f'State must one of {all_enum_to_str(State)}')
        return value


class AddressDataResponse(BaseModel):
    id: UUID
    address: str
    created_at: datetime
    updated_at: datetime
    street: str
    state: int
    zip_code: int
    apartment_number: int


class UserDataResponse(BaseModel):
    id: UUID
    email: str
    user_name: str
    first_name: str
    last_name: str
    age: int
    address_id: UUID
    degree: int
    gender: int
    created_at: datetime
    updated_at: datetime
