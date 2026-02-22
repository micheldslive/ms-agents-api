from typing import List, Optional

from app.entities.base import EntityBase
from app.schemas.knowledge_bases.knowledge_base_create import (
    KnowledgeBaseFileSchema,
    KnowledgeBaseTypeEnum,
)


class KnowledgeBasesEntity(EntityBase):
    name: str
    description: str
    type: KnowledgeBaseTypeEnum
    enable: bool
    files: Optional[List[KnowledgeBaseFileSchema]] = None
    embedding_model: Optional[str] = None
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    tags: Optional[List[str]] = None
