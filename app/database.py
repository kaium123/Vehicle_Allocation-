import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.migrations.migration import init_db

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.vehicle_allocation

async def initialize_database():
    # mongo_host = os.getenv("MONGO_HOST", "mongodb")
    # mongo_port = os.getenv("MONGO_PORT", "27017")
    # print(mongo_host)
    # print(mongo_port)
    await init_db()