from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from routes.address import router as address_router
from routes.stakeholder import router as stakeholder_router
from routes.token import router as auth_router
from routes.user import router as user_router

app = FastAPI()


app.include_router(
    auth_router,
    tags=['Token'],
)

app.include_router(
    stakeholder_router,
    tags=['Stakeholders'],
)

app.include_router(
    user_router,
    tags=['Users'],
)

app.include_router(
    address_router,
    tags=['Addresses'],
)


@app.exception_handler(IntegrityError)
async def default_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    error_info = str(exc.args[0])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"error": 'Integrity Error', "details": error_info[error_info.index('DETAIL'):]}))
