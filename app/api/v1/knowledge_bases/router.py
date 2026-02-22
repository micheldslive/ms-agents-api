from typing import Any
from fastapi import APIRouter

from app.schemas.knowledge_bases.knowledge_base_create import KnowledgeBaseResponseSchema
from app.schemas.knowledge_bases.knowledge_bases_list import KnowledgeBasesListSchema

from .endpoints import (
    create_knowledge_base,
    delete_knowledge_bases,
    list_knowledge_bases,
)

router = APIRouter(prefix="/knowledge-bases", tags=["Knowledge Bases"])

router.add_api_route(
    "/",
    create_knowledge_base,
    methods=["POST"],
    name="Create Knowledge Base",
    description="Creates a new knowledge base.",
    response_model=KnowledgeBaseResponseSchema,
)

router.add_api_route(
    "/",
    list_knowledge_bases,
    methods=["GET"],
    name="List Knowledge Bases",
    description="Returns the knowledge bases if parameters is provided.",
    response_model=KnowledgeBasesListSchema,
)

router.add_api_route(
    "/",
    delete_knowledge_bases,
    methods=["DELETE"],
    name="Delete Knowledge Bases",
    description="Delete knowledge base(s) of a specific _id.",
    response_model=Any,
)
