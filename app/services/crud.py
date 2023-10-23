from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)
from app.schemas.donation import DonationCreate
from app.services.investment import investment
from app.services.validators import (check_full_amount_befor_edit_project,
                                     check_invested_amount,
                                     check_name_duplicate,
                                     check_the_project_is_closed)


async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await investment(new_charity_project, donation_crud, session)
    return new_charity_project


async def update_charity_project(
    charity_project_for_update: CharityProject,
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_the_project_is_closed(project_id, session)
    if obj_in.full_amount:
        await check_full_amount_befor_edit_project(project_id, obj_in, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project_for_update, obj_in, session
    )
    return charity_project


async def delete_charity_project(
    charity_project_for_delete: CharityProject,
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_invested_amount(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project_for_delete,
        session,
    )
    return charity_project


async def creating_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    await investment(new_donation, charity_project_crud, session)
    return new_donation
