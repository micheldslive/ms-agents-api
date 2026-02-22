from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.connectors.mongo import MongoConnector
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # startup events
    MongoConnector().init()

    yield
    # shutdown events
    MongoConnector().close()
