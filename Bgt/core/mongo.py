from config import MONGO_DB
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_


_mongo_async_ = _mongo_client_(MONGO_DB)
_mongo_sync_ = MongoClient(MONGO_DB)
mongodb = _mongo_async_.BgtOwner
pymongodb = _mongo_sync_.BgtOwner
