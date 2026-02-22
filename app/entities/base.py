from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.datetime import get_brazil_current_datetime


class EntityBase(BaseModel):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=get_brazil_current_datetime)
    updated_at: datetime = Field(default_factory=get_brazil_current_datetime)

    @field_validator("id", mode="before")
    @classmethod
    def id_validate(cls, value: str | ObjectId):
        return str(value)
