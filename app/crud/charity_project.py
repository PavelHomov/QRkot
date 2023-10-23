from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получаем id существующего проекта из базы данных."""
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == charity_project_name)
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_charity_project_by_id(
        self,
        charity_project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получаем проект по id."""
        db_charity_project = await session.execute(
            select(CharityProject).where(CharityProject.id == charity_project_id)
        )
        db_charity_project = db_charity_project.scalars().first()
        return db_charity_project

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, str]]:
        """Сортирует список со всеми закрытыми проектами."""
        projects_closed = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        projects_closed = projects_closed.scalars().all()
        projects = []
        for project in projects_closed:
            projects.append({
                'name': project.name,
                'collection_time': project.close_date - project.create_date,
                'description': project.description
            })
        projects = sorted(projects, key=lambda date: date['collection_time'])
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
