from fastapi import APIRouter

from app.api.v1.router import v1_router

routers = [v1_router]

main_router = APIRouter(
    prefix="/api",
)

for router in routers:
    main_router.include_router(router)


# simple endpoint for status check
@main_router.get("/ping", tags=["Status"])
def pong():
    return "pong"
