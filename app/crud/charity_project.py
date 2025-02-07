from typing import Type, Optional, List

from sqlalchemy import select, asc, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.models.base import BaseModel


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_oldest_open_item(
            self,
            session: AsyncSession,
            model: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """
        Универсальная функция для получения самой старой открытой записи
        из указанной модели.
        """
        oldest_open_item = await session.execute(
            select(model).filter(
                model.fully_invested.is_(False)
            ).order_by(asc(model.create_date)).limit(1)
        )
        return oldest_open_item.scalars().first()


async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,) -> List[CharityProject]:
    """Запрос по завершённым проектам."""

    projects = await session.execute(
        select([
            CharityProject.name,
            CharityProject.description,
            CharityProject.create_date,
            CharityProject.close_date]).where(
            CharityProject.fully_invested.is_(True)
        ).order_by(
            extract('year', CharityProject.close_date) -
            extract('year', CharityProject.create_date),
            extract('month', CharityProject.close_date) -
            extract('month', CharityProject.create_date),
            extract('day', CharityProject.close_date) -
            extract('day', CharityProject.create_date),
            extract('hour', CharityProject.close_date) -
            extract('hour', CharityProject.create_date),
        )
    )
    return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
