import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.migrations.migration import init_db

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(mongo_uri)
db = client.vehicle_allocation

async def initialize_database():

    await init_db()