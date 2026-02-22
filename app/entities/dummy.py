from pydantic import BaseModel
from app.entities.base import EntityBase


class DummyEntity(EntityBase):
    dummy_value: str
