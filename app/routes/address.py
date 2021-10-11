from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from db import addresses, engine
from docs import AddressRequestDoc, AddressResponseDoc
from enums import State, all_enum_to_str
from model import AddressDataRequest, AddressDataResponse
from services.authentication import validate_token

router = APIRouter()


@router.get('/addresses', response_model=AddressResponseDoc)
async def get_all_addresses(_: bool = Depends(validate_token)) -> JSONResponse:
    """
    Returns all available addresses in the database.
    """
    with engine.connect() as conn:
        address_data = conn.execute(addresses.select())
        if not address_data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=[])
        return JSONResponse(status_code=status.HTTP_200_OK, content=encoder(
            AddressDataResponse(**dict(data)) for data in address_data))


@ router.get('/addresses/{address_id}', response_model=AddressRequestDoc)
async def get_address(address_id: UUID, _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Returns all the information of the following address ID.
    """
    with engine.connect() as conn:
        address_data = conn.execute(
            addresses.select().where(addresses.c.id == address_id)).first()
        if not address_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Address Not Found id: {address_id}')
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder((AddressDataResponse(**dict(address_data)))))


@router.post('/addresses', response_model=AddressRequestDoc)
async def create_address(address_data: AddressDataRequest,
                         _: bool = Depends(validate_token)) -> JSONResponse:
    f"""
    `address`: string, The name of the Address.\n
    `street`: string, The name of the street.\n
    `state`: integer, States: {all_enum_to_str(State)}.\n
    `zip_code`: integer, The zipcode must not exceed 5 characters. (Optional Field)\n
    `apartment_number`: integer\n
    """
    with engine.begin() as conn:
        address_data.dict(exclude_none=True)
        result = conn.execute(addresses.insert().returning(addresses).values(
            **address_data.dict(),
        )).first()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(AddressDataResponse(
                                **dict(result))))


@ router.delete('/addresses/{address_id}')
async def delete_address(address_id: UUID, _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Deletes all the information for this address ID from the database.
    """
    with engine.connect() as conn:
        result = conn.execute(addresses.delete().where(
            addresses.c.id == address_id)).rowcount

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Address id: {address_id} does not exist.')

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content={'data': f'{address_id} Address Deleted Successfully'})


@ router.patch('/addresses/{address_id}', response_model=AddressRequestDoc)
async def update_address(address_id: UUID, address_data: AddressDataRequest,
                         _: bool = Depends(validate_token)) -> JSONResponse:
    """
    Update address information that matches the inserted address ID.
    """
    with engine.begin() as conn:
        result = conn.execute(
            addresses.update().returning(addresses).where(
                addresses.c.id == address_id).values(
                **address_data.dict())).first()

        if not result.rowcount:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Address id: {address_id} does not exist.')

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(AddressDataResponse(
                                **dict(result))))
