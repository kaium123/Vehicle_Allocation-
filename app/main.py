import os
from fastapi import FastAPI
from app.routes.allocations import router as allocation_router
from app.database import initialize_database
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # mongo_host = os.getenv("MONGO_HOST", "mongodb")
    # mongo_port = os.getenv("MONGO_PORT", "27017")
    # print(mongo_host)
    # print(mongo_port)
    await initialize_database()

app.include_router(allocation_router, prefix="/allocations", tags=["Allocations"])

@app.get("/")
async def root():
    return {"message": "Vehicle Allocation API"}