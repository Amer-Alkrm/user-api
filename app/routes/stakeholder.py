
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder as encoder
from fastapi.responses import JSONResponse

from db import engine, stakeholders
from model import StakeholderDataRequest, StakeholderDataResponse

router = APIRouter()


@router.get('/admin/stakeholders')
async def get_all_stakeholders() -> JSONResponse:
    """
    Returns all available stakeholders in the database.
    """
    with engine.connect() as conn:
        stakeholders_data = conn.execute(stakeholders.select())
        if not stakeholders_data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=[])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(StakeholderDataResponse(**dict(data))
                                            for data in stakeholders_data))


@router.post('/admin/stakeholders')
async def create_stakeholder(inserted_stakeholder_data: StakeholderDataRequest) -> JSONResponse:
    """
    Creates a new stakeholder with the filled data.
    """
    with engine.begin() as conn:
        result = conn.execute(stakeholders.insert().returning(stakeholders).values(
            **inserted_stakeholder_data.dict(),
        )).first()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=encoder(StakeholderDataResponse(
                                **dict(result))))
