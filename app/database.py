import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.migrations.migration import init_db

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.vehicle_allocation

async def initialize_database():

    await init_db()