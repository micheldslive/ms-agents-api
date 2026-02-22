from typing import Optional

from app.core.logging import get_logger
from app.repositories.agents.mongo import AgentsMongoRepository
from app.schemas.agents.agents_list import AgentsListSchema

logger = get_logger("list_agents")


class ListAgentsUseCase:
    def __init__(self, agents_repository: AgentsMongoRepository):
        self.agents_repository = agents_repository

    def execute(
        self,
        limit: int,
        skip: int,
        filters: Optional[dict],
        last_iterations: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[int] = 1,
    ) -> AgentsListSchema:
        logger.info(
            f"Listing agents with skip:{skip}, limit: {limit}, filters:{filters}"
        )

        agents = self.agents_repository.list(
            limit=limit,
            skip=skip,
            last_iterations=last_iterations,
            order_by=order_by,
            order_dir=order_dir,
            filters=filters,
        )

        logger.info(f"Found {len(agents)} agents")

        try:
            total_count = (
                len(agents)
                if last_iterations
                else self.agents_repository.count(filters=filters)
            )
        except Exception as e:
            logger.exception("Error while counting agents")
            raise

        return AgentsListSchema(items=agents, total_count=total_count)
