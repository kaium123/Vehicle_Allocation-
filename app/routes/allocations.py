import os
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import datetime
from aiocache import Cache
from aiocache.decorators import cached
from app.models import Allocation
from app.database import db
from bson import ObjectId

from aiocache import Cache
router = APIRouter()

from fastapi import FastAPI
import redis

from aiocache import Cache

# Get cache URL from environment variable
CACHE_URL = os.getenv("CACHE_URL", "redis://localhost:6379")
cache = Cache.from_url(CACHE_URL)




@router.post("/", response_model=Allocation, summary="Create an allocation", tags=["Allocations"])
async def create_allocation(allocation: Allocation):
    """
    Create a new vehicle allocation.
    
    - **vehicle_id**: ID of the vehicle to be allocated
    - **employee_id**: ID of the employee
    - **allocation_date**: Date for the allocation
    """
    existing_allocation = await db.allocations.find_one({
        "vehicle_id": allocation.vehicle_id,
        "allocation_date": allocation.allocation_date
    })
    
    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for that day")

    result = await db.allocations.insert_one(allocation.dict())
    allocation.id = str(result.inserted_id)
    
    await cache.add(allocation.id,allocation)
    
    return allocation

@router.put("/{allocation_id}", response_model=Allocation, summary="Update an allocation", tags=["Allocations"])
async def update_allocation(allocation_id: str, update_data: Allocation):
    """
    Update an existing vehicle allocation.
    
    - **allocation_id**: ID of the allocation to update
    """
    
    allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})
    
    existing_allocation = await db.allocations.find_one({
        "vehicle_id": update_data.vehicle_id,
        "allocation_date": update_data.allocation_date
    })
    
    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for that day")
    

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation["allocation_date"] < str(datetime.date.today()):
        raise HTTPException(status_code=400, detail="Cannot update past allocations")

    update_result = await db.allocations.update_one(
        {"_id": ObjectId(allocation_id)},
        {"$set": update_data.dict(exclude_unset=True)}
    )

    print("update_result.modified_count -- ",update_result.modified_count)
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update allocation")

    # Clear cache for allocations to refresh data
    await cache.delete(allocation_id)
    await cache.add(allocation_id,allocation)

    print(allocation["vehicle_id"], "  ",allocation["allocation_date"])
    await free_vehicle(allocation["vehicle_id"],allocation["allocation_date"])
    
    return {**allocation, **update_data.dict()}

@router.delete("/{allocation_id}", summary="Delete an allocation", tags=["Allocations"])
async def delete_allocation(allocation_id: str):
    """
    Delete an allocation by its ID.
    
    - **allocation_id**: ID of the allocation to delete
    """
    allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation["allocation_date"] < str(datetime.date.today()):
        raise HTTPException(status_code=400, detail="Cannot delete past allocations")

    await db.allocations.delete_one({"_id": ObjectId(allocation_id)})

    # Clear cache for allocations to refresh data
    await cache.delete("allocations")
    
    return {"detail": "Allocation deleted"}

@router.get("/", response_model=List[Allocation], summary="Get allocations", tags=["Allocations"])
@cached(ttl=60, key="allocations")  # Cache the result for 60 seconds
async def get_allocations(
    employee_id: Optional[str] = Query(None, description="ID of the employee"),
    vehicle_id: Optional[str] = Query(None, description="ID of the vehicle"),
    start_date: Optional[datetime.date] = Query(None, description="Start date for filtering allocations"),
    end_date: Optional[datetime.date] = Query(None, description="End date for filtering allocations")
):
    """
    Retrieve a list of vehicle allocations, optionally filtered by employee ID, vehicle ID, or allocation date range.
    
    - **employee_id**: Filter by employee ID
    - **vehicle_id**: Filter by vehicle ID
    - **start_date**: Start of allocation date range
    - **end_date**: End of allocation date range
    """
    query = {}

    if employee_id:
        query["employee_id"] = ObjectId(employee_id)
    if vehicle_id:
        query["vehicle_id"] = ObjectId(vehicle_id)
    if start_date and end_date:
        query["allocation_date"] = {"$gte": start_date, "$lte": end_date}

    allocations = []
    async for allocation in db.allocations.find(query):
        allocations.append(Allocation(**allocation))

    return allocations

async def free_vehicle(vehicle_id: str, allocation_date: str):
    """
    Delete an allocation by vehicle ID and allocation date.
    
    - **vehicle_id**: ID of the vehicle being freed
    - **allocation_date**: Date of the allocation to delete (formatted as 'YYYY-MM-DD')
    """
    
    print(vehicle_id, "  ",allocation_date)
    # Convert allocation_date from string to a date object
    allocation_date_obj = datetime.datetime.strptime(allocation_date, "%Y-%m-%d").date()

    # Find the allocation using vehicle_id and allocation_date
    allocation = await db.allocations.find_one({
        "vehicle_id": ObjectId(vehicle_id),
        "allocation_date": allocation_date_obj
    })

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation["allocation_date"] < datetime.date.today():
        raise HTTPException(status_code=400, detail="Cannot delete past allocations")

    # Delete the allocation
    await db.allocations.delete_one({
        "vehicle_id": ObjectId(vehicle_id),
        "allocation_date": allocation_date_obj
    })
    
    return {"detail": "Allocation deleted"}
