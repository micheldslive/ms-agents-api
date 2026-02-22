from functools import lru_cache
from typing import Annotated

import pytz
from bson.codec_options import CodecOptions
from fastapi import Depends
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.api.dependencies.connectors import get_mongo_client


# databases
@lru_cache(maxsize=16)
def get_registry_database(
    mongo_client: Annotated[MongoClient, Depends(get_mongo_client)],
) -> Database:
    database = mongo_client.get_default_database()
    return database


@lru_cache(maxsize=16)
def get_agents_collection(
    db: Annotated[Database, Depends(get_registry_database)],
) -> Collection:
    collection = db["agents"]
    collection = collection.with_options(
        CodecOptions(tz_aware=True, tzinfo=pytz.timezone("America/Sao_Paulo"))
    )
    return collection


@lru_cache(maxsize=16)
def get_tools_collection(
    db: Annotated[Database, Depends(get_registry_database)],
) -> Collection:
    collection = db["tools"]
    collection = collection.with_options(
        CodecOptions(tz_aware=True, tzinfo=pytz.timezone("America/Sao_Paulo"))
    )
    return collection


@lru_cache(maxsize=16)
def get_knowledge_bases_collection(
    db: Annotated[Database, Depends(get_registry_database)],
) -> Collection:
    collection = db["knowledge_bases"]
    collection = collection.with_options(
        CodecOptions(tz_aware=True, tzinfo=pytz.timezone("America/Sao_Paulo"))
    )
    return collection
