from typing import List

from pydantic import BaseModel

from app.entities.agents import AgentsEntity


class AgentsListBaseSchema(AgentsEntity): ...


class AgentsListSchema(BaseModel):
    items: List[AgentsEntity]
    total_count: int
