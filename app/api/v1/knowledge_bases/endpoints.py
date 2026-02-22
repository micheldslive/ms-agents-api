from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.dependencies.use_cases.knowledge_bases import (
    delete_knowledge_bases_use_case,
    get_create_knowledge_base_use_case,
    get_list_knowledge_bases_use_case,
)
from app.core.logging import get_logger

from app.exceptions.http import SystemHttpException
from app.exceptions.knowledge_bases import KnowledgeBaseNotExists

from app.schemas.knowledge_bases.knowledge_base_create import (
    KnowledgeBaseResponseSchema,
    KnowledgeBaseSchema,
    KnowledgeBaseTypeEnum,
)
from app.schemas.knowledge_bases.knowledge_bases_list import KnowledgeBasesListSchema

from app.use_cases.knowledge_bases.create_knowledge_base import CreateKnowledgeBaseUseCase
from app.use_cases.knowledge_bases.delete_knowledge_bases import DeleteKnowledgeBasesUseCase
from app.use_cases.knowledge_bases.list_knowledge_bases import ListKnowledgeBasesUseCase
from app.utils import build_filters


logger = get_logger("knowledge_bases_endpoints")


def create_knowledge_base(
    kb_data: KnowledgeBaseSchema,
    use_case: Annotated[CreateKnowledgeBaseUseCase, Depends(get_create_knowledge_base_use_case)],
) -> KnowledgeBaseResponseSchema:
    try:
        return use_case.execute(kb_data=kb_data)
    except KnowledgeBaseNotExists as e:
        raise SystemHttpException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="DUPLICATED_KNOWLEDGE_BASE",
            detail=str(e),
        )


def list_knowledge_bases(
    use_case: Annotated[ListKnowledgeBasesUseCase, Depends(get_list_knowledge_bases_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
    start_date: Annotated[Optional[datetime], Query(title="Initial Date")] = None,
    end_date: Annotated[Optional[datetime], Query(title="Final Date")] = None,
    type: Annotated[Optional[KnowledgeBaseTypeEnum], Query(title="Filter by knowledge base type")] = None,
    tags: Annotated[Optional[List[str]], Query(title="Filter by tags")] = None,
    enable: Annotated[Optional[bool], Query(title="Filter by enabled status")] = None,
    skip: Annotated[int, Query(title="Number of knowledge bases to skip", ge=0)] = 0,
    limit: Annotated[int, Query(title="Number of knowledge bases to limit", ge=1, le=100)] = 100,
    last_iterations: Annotated[
        Optional[int], Query(ge=1, le=50, title="Number of last iterations")
    ] = None,
    order_by: Annotated[Optional[str], Query(title="Order by")] = None,
    order_dir: Annotated[Optional[int], Query(title="Order dir")] = 1,
) -> KnowledgeBasesListSchema:

    filters = build_filters(
        _id=_id,
        start_date=start_date,
        end_date=end_date,
    )
    if type is not None:
        filters["type"] = type.value
    if tags:
        filters["tags"] = {"$all": tags}
    if enable is not None:
        filters["enable"] = enable

    try:
        return use_case.execute(
            limit=limit,
            skip=skip,
            last_iterations=last_iterations,
            order_by=order_by,
            order_dir=order_dir,
            filters=filters,
        )
    except ValidationError:
        raise SystemHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
        )
    except Exception:
        raise SystemHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
        )


def delete_knowledge_bases(
    use_case: Annotated[DeleteKnowledgeBasesUseCase, Depends(delete_knowledge_bases_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
):

    filters = build_filters(
        _id=_id,
    )

    try:
        result = use_case.execute(filters=filters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except KnowledgeBaseNotExists:
        raise SystemHttpException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="KNOWLEDGE_BASES_NOT_FOUND",
        )
    except ValidationError:
        raise SystemHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
        )
    except Exception:
        raise SystemHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
        )
