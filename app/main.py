import os
from fastapi import FastAPI
from app.routes.allocations import router as allocation_router  # Importing allocation-related routes
from app.database import initialize_database  # Importing the function to initialize the database
import asyncio

# Create an instance of the FastAPI application
app = FastAPI(
    title="Vehicle Allocation API",
    description="API for managing vehicle allocations to employees.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs when the application starts up.
    
    This function is executed before the application starts serving requests.
    It is used here to initialize the database connection and perform
    any other necessary startup tasks.
    """
    await initialize_database()  # Initialize the database connection when the app starts


# Include the allocation router to manage the /allocations routes
app.include_router(allocation_router, prefix="/allocations", tags=["Allocations"])

@app.get("/")
async def root():
    """
    Root endpoint to verify that the API is working.
    
    This simple endpoint returns a welcome message and can be used to check
    the status of the API.
    
    Returns:
    - A message indicating that the Vehicle Allocation API is running.
    """
    return {"message": "Vehicle Allocation API"}


