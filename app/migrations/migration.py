import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import ConnectionFailure

from app.models import Employee, Vehicle, Allocation

async def init_db():
    # Set MongoDB host and port
    mongo_host = "localhost"
    mongo_port = "27017"
    
    print(f"Connecting to MongoDB at {mongo_host}:{mongo_port}...")

    # Construct the MongoDB connection string
    mongo_uri = "mongodb://localhost:27017"

    try:
        # Initialize the MongoDB client
        client = AsyncIOMotorClient(mongo_uri)
        
        # Attempt to get the database to verify the connection
        database = client.vehicle_allocation
        
        # Check if the connection is successful
        await database.command("ping")
        print("Successfully connected to the database.")

        # Initialize Beanie with the database and models
        await init_beanie(database, document_models=[Employee, Vehicle, Allocation])
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

async def migrate():
    # Define your migration logic here if needed
    pass
