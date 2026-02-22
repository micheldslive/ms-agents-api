from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.lifespan import lifespan
from app.api.main_router import main_router
from app.core.settings import settings
from app.exceptions.http import SystemHttpException

app = FastAPI(
    title="Memory API",
    description="API com as entidades para trabalhar com memoria dos agentes da plataforma IA",
    root_path=settings.OPENAPI_PREFIX,
    lifespan=lifespan,
)
app.include_router(main_router)

# add auth middleware if not in development mode
# if not settings.IS_DEVELOPMENT:
#     from app.api.middlewares.auth import AuthMiddleware

#     app.add_middleware(AuthMiddleware)

#     # add cors for allowed origins

if settings.BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# add custom exception handlers
class ErrorSchema(BaseModel):
    error_code: str
    detail: str


async def http_exception_handler(request: Request, exc: Exception):
    system_exc = (
        exc
        if isinstance(exc, SystemHttpException)
        else SystemHttpException(status_code=500)
    )
    content = ErrorSchema(
        error_code=system_exc.error_code or "", detail=system_exc.detail or ""
    ).model_dump(mode="json")
    return JSONResponse(content, status_code=system_exc.status_code)


app.add_exception_handler(SystemHttpException, http_exception_handler)
