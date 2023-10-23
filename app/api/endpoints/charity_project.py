from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.crud import (create_charity_project, delete_charity_project,
                               update_charity_project)

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    result = await create_charity_project(charity_project, session)
    return result


@router.get(
    "/", response_model=List[CharityProjectDB], response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    result = await update_charity_project(
        charity_project,
        project_id,
        obj_in,
        session
    )
    return result


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    result = await delete_charity_project(
        charity_project,
        project_id,
        session,
    )
    return result
