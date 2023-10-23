from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class DonationCreate(BaseModel):
    """Схема для создания прожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    """Схема для ответа."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGetAll(DonationDB):
    """Схема для получения сприска всех пожертвований."""
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: datetime = Field(None)
