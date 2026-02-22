from fastapi import APIRouter

from app.api.v1.agents.router import router as agents_router
from app.api.v1.tools.router import router as tools_router
from app.api.v1.knowledge_bases.router import router as knowledge_bases_router

v1_routers = [
    agents_router,
    tools_router,
    knowledge_bases_router,
]
v1_router = APIRouter(prefix="/v1")

for router in v1_routers:
    v1_router.include_router(router)
