from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.dependencies.use_cases.agents import (
    delete_agents_use_case,
    get_create_agent_use_case,
    get_list_agents_use_case,
)
from app.core.logging import get_logger

from app.exceptions.http import SystemHttpException
from app.exceptions.agents import AgentNotExists

from app.schemas.agents.agent_create import AgentResponseSchema, AgentSchema
from app.schemas.agents.agents_list import AgentsListSchema

from app.use_cases.agents.create_agent import CreateAgentUseCase
from app.use_cases.agents.delete_agents import DeleteAgentsUseCase
from app.use_cases.agents.list_agents import ListAgentsUseCase
from app.utils import build_filters


logger = get_logger("agents_endpoints")


def create_agent(
    agent_data: AgentSchema,
    use_case: Annotated[CreateAgentUseCase, Depends(get_create_agent_use_case)],
) -> AgentResponseSchema:
    try:
        return use_case.execute(agent_data=agent_data)
    except AgentNotExists as e:
        raise SystemHttpException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="DUPLICATED_AGENT",
            detail=str(e),
        )


def list_agents(
    use_case: Annotated[ListAgentsUseCase, Depends(get_list_agents_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
    start_date: Annotated[Optional[datetime], Query(title="Initial Date")] = None,
    end_date: Annotated[Optional[datetime], Query(title="Final Date")] = None,
    skip: Annotated[int, Query(title="Number of agents to skip", ge=0)] = 0,
    limit: Annotated[int, Query(title="Number of agents to limit", ge=1, le=100)] = 100,
    last_iterations: Annotated[
        Optional[int], Query(ge=1, le=50, title="Number of last iterations")
    ] = None,
    order_by: Annotated[Optional[str], Query(title="Order by")] = None,
    order_dir: Annotated[Optional[int], Query(title="Order dir")] = 1,
) -> AgentsListSchema:

    filters = build_filters(
        _id=_id,
        start_date=start_date,
        end_date=end_date,
    )

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


def delete_agents(
    use_case: Annotated[DeleteAgentsUseCase, Depends(delete_agents_use_case)],
    _id: Annotated[Optional[List[str]], Query(title="Optional Object Id List")] = None,
):

    filters = build_filters(
        _id=_id,
    )

    try:
        result = use_case.execute(filters=filters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except AgentNotExists:
        raise SystemHttpException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="AGENTS_NOT_FOUND",
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
