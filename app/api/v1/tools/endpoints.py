from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.dependencies.use_cases.tools import (
    delete_tools_use_case,
    get_create_tool_use_case,
    get_list_tools_use_case,
)
from app.core.logging import get_logger

from app.exceptions.http import SystemHttpException
from app.exceptions.tools import ToolNotExists

from app.schemas.tools.tool_create import ToolResponseSchema, ToolSchema, ToolTypeEnum
from app.schemas.tools.tools_list import ToolsListSchema

from app.use_cases.tools.create_tool import CreateToolUseCase
from app.use_cases.tools.delete_tools import DeleteToolsUseCase
from app.use_cases.tools.list_tools import ListToolsUseCase
from app.utils import build_filters


logger = get_logger("tools_endpoints")


def create_tool(
    tool_data: ToolSchema,
    use_case: Annotated[CreateToolUseCase, Depends(get_create_tool_use_case)],
) -> ToolResponseSchema:
    try:
        return use_case.execute(tool_data=tool_data)
    except ToolNotExists as e:
        raise SystemHttpException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="DUPLICATED_TOOL",
            detail=str(e),
        )


def list_tools(
    use_case: Annotated[ListToolsUseCase, Depends(get_list_tools_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
    start_date: Annotated[Optional[datetime], Query(title="Initial Date")] = None,
    end_date: Annotated[Optional[datetime], Query(title="Final Date")] = None,
    type: Annotated[Optional[ToolTypeEnum], Query(title="Filter by tool type")] = None,
    tags: Annotated[Optional[List[str]], Query(title="Filter by tags")] = None,
    enable: Annotated[Optional[bool], Query(title="Filter by enabled status")] = None,
    skip: Annotated[int, Query(title="Number of tools to skip", ge=0)] = 0,
    limit: Annotated[int, Query(title="Number of tools to limit", ge=1, le=100)] = 100,
    last_iterations: Annotated[
        Optional[int], Query(ge=1, le=50, title="Number of last iterations")
    ] = None,
    order_by: Annotated[Optional[str], Query(title="Order by")] = None,
    order_dir: Annotated[Optional[int], Query(title="Order dir")] = 1,
) -> ToolsListSchema:

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


def delete_tools(
    use_case: Annotated[DeleteToolsUseCase, Depends(delete_tools_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
):

    filters = build_filters(
        _id=_id,
    )

    try:
        result = use_case.execute(filters=filters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except ToolNotExists:
        raise SystemHttpException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="TOOLS_NOT_FOUND",
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
