from operator import and_
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from db import addresses, engine, users
from docs import UserRequestDoc, UserResponseDoc
from enums import Degree, Gender, all_enum_to_str
from model import UserDataRequest, UserDataResponse
from services.authentication import current_admin_email, validate_admin, validate_token

router = APIRouter()


@router.get('/users', response_model=UserResponseDoc)
async def get_all_users(_: bool = Depends(validate_token)) -> JSONResponse:
    """
    Returns all available users in the database.
    """
    with engine.connect() as conn:
        users_data = conn.execute(users.select())
        if not users_data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=[])

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(UserDataResponse(**dict(data))
                                            for data in users_data))


@router.get('/users/gender', response_model=UserRequestDoc)
async def get_user_by_gender(gender: Gender, _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Returns all users information with the following gender.
    """
    with engine.connect() as conn:
        user_data = conn.execute(
            users.select().where(users.c.gender == gender))
        if not user_data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=[])

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(
                                UserDataResponse(**dict(data)) for data in user_data))


@router.get('/users/{user_id}', response_model=UserRequestDoc)
async def get_user(user_id: UUID, _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Returns all the information of the following user_id.
    """
    with engine.connect() as conn:
        user_data = conn.execute(  # join alias or label.
            users.join(addresses, and_(users.c.id == user_id, addresses.c.id == users.c.address_id))
            .alias().select()).fetchall()
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User Not Found id: {user_id}')

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(data
                                            for data in user_data))


@router.post('/users', response_model=UserRequestDoc)
async def create_user(inserted_user_data: UserDataRequest, is_admin: bool = Depends(validate_admin),
                      admin_email: str = Depends(current_admin_email)) -> JSONResponse:
    f"""
    `address_id`: UUID Foreign key , this value must exist in the ID in the Address table \n
    `user_name`: string , the username of the user which will be displayed on the forum.\n
    `first_name`: string.\n
    `last_name`: string.\n
    `age`: integer, It must be between 10 and 100 .\n
    `degree`: integer, must be {all_enum_to_str(Degree)}.\n
    `gender`: integer, must be {all_enum_to_str(Gender)}.\n
    `email`: Email, it must be a valid mail format. Example: example@gmail.com\n
    """
    with engine.begin() as conn:
        if not is_admin:
            raise HTTPException(
                status_code=403, detail=('This stakeholder is not an Admin.'
                                         + ' only admins can create users.'))
        result = conn.execute(users.insert().returning(users).values(
            **inserted_user_data.dict(),
            created_by_email=admin_email
        )).first()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(UserDataResponse(
                                **dict(result))))


@ router.delete('/users/{user_id}')
async def delete_user(user_id: UUID, _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Deletes all the information for this user ID from the database.
    """
    with engine.connect() as conn:
        result = conn.execute(users.delete().where(
            users.c.id == user_id)).rowcount
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User id: {user_id} does not exist.')

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content={'data': f'{user_id} User Deleted Successfully'})


@ router.patch('/users/{user_id}', response_model=UserRequestDoc)
async def update_users(user_id: UUID, user_data: UserDataRequest,
                       _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Update user information that matches the inserted user ID.
    """
    with engine.begin() as conn:
        result = conn.execute(users.update().returning(users).where(
            users.c.id == user_id).values(
            **user_data.dict()
        ))
        if not result.rowcount:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User id: {user_id} does not exist.')

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(UserDataResponse(
                                **dict(data)) for data in result))
