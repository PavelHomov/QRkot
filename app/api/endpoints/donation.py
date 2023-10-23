from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAll
from app.services.crud import creating_donation

router = APIRouter()


@router.post("/", response_model=DonationDB, response_model_exclude_none=True)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Cоздание пожертвования."""
    result = await creating_donation(donation, session, user)
    return result


@router.get(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=List[DonationGetAll],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get("/my", response_model=List[DonationDB])
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получаем список всех пожертвований пользователя."""
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
