from fastapi import APIRouter, HTTPException, Response, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserLoginSchema
from config import security, config
from database import get_db
from repository import UserRepository
from models import UserModel

router = APIRouter(
    tags=["login"]
)


@router.post("/login")
async def login(
    credentials: UserLoginSchema,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)

    user: UserModel = await repo.authenticate(
        credentials.username,
        credentials.password
    )
    if user:
        access_token = security.create_access_token(uid="1")
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=access_token,
            secure=True,
            max_age=3600
        )
        return {"access_token": access_token}
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


@router.get(
    "/protected",
    dependencies=[Depends(security.access_token_required)]
)
async def potected():
    return {"message": "OK"}
