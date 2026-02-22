from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class KnowledgeBaseTypeEnum(str, Enum):
    document = "document"
    website = "website"
    database = "database"
    custom = "custom"


class KnowledgeBaseFileStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class KnowledgeBaseFileSchema(BaseModel):
    name: str = Field(..., description="Original file name")
    url: str = Field(..., description="URL or storage path to access the file")
    mime_type: str = Field(
        ..., description="File MIME type (e.g. application/pdf, text/plain)"
    )
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    status: KnowledgeBaseFileStatusEnum = Field(
        KnowledgeBaseFileStatusEnum.pending,
        description="Processing status of the file",
    )
    checksum: Optional[str] = Field(
        None, description="MD5 or SHA256 checksum for integrity validation"
    )


class KnowledgeBaseSchema(BaseModel):
    name: str = Field(..., description="Knowledge base name")
    description: str = Field(
        ..., description="What content this knowledge base contains"
    )
    type: KnowledgeBaseTypeEnum = Field(
        ..., description="Source type: document, website, database, custom"
    )
    enable: bool = Field(True, description="Whether the knowledge base is active")
    files: Optional[List[KnowledgeBaseFileSchema]] = Field(
        default_factory=list,
        description="Files associated with this knowledge base",
    )
    embedding_model: Optional[str] = Field(
        "text-embedding-ada-002",
        description="Embedding model used to vectorize content",
    )
    chunk_size: Optional[int] = Field(
        512, ge=64, le=8192, description="Token size of each document chunk"
    )
    chunk_overlap: Optional[int] = Field(
        64, ge=0, le=1024, description="Overlap between consecutive chunks"
    )
    tags: Optional[List[str]] = Field(
        default_factory=list,
        description="Tags for grouping and filtering knowledge bases",
    )


class KnowledgeBaseResponseSchema(KnowledgeBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime
