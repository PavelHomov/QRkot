from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LENGHT
from app.models.base import CharityProjectDonationBaseModel


class CharityProject(CharityProjectDonationBaseModel):
    """Модель проекта."""
    name = Column(String(NAME_MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
