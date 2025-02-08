from sqlalchemy import Column, String, Text

from app.constants import NAME_MAX_LENGTH
from app.models.base import BaseModel


class CharityProject(BaseModel):
    """
    Для благотворительных проектов:
    - name: Название проекта (уникальное).
    - description: Описание проекта.
    """
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"CharityProject (ID: {self.id}, Name: {self.name})"
