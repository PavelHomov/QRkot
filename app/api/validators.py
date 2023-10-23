from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка наличия проекта в базе данных."""

    charity_project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден!"
        )
    return charity_project
