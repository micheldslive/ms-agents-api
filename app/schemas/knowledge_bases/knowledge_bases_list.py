from typing import List

from pydantic import BaseModel

from app.entities.knowledge_bases import KnowledgeBasesEntity


class KnowledgeBasesListSchema(BaseModel):
    items: List[KnowledgeBasesEntity]
    total_count: int
