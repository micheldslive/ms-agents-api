from typing import List

from pydantic import BaseModel

from app.entities.tools import ToolsEntity


class ToolsListSchema(BaseModel):
    items: List[ToolsEntity]
    total_count: int
