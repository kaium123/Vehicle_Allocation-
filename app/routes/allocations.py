from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List, Optional
import datetime

from app.models import Allocation
from app.database import db

router = APIRouter()

@router.post("/", response_model=Allocation)
async def create_allocation(allocation: Allocation):
    existing_allocation = await db.allocations.find_one({
        "vehicle_id": allocation.vehicle_id,
        "allocation_date": allocation.allocation_date
    })
    print("data -- ",existing_allocation)

    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for that day")

    result = await db.allocations.insert_one(allocation.dict())
    allocation.id = result.inserted_id
    return allocation

@router.put("/{allocation_id}", response_model=Allocation)
async def update_allocation(allocation_id: str, update_data: Allocation):
    allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation["allocation_date"] < str(datetime.date.today()):
        raise HTTPException(status_code=400, detail="Cannot update past allocations")

    update_result = await db.allocations.update_one(
        {"_id": ObjectId(allocation_id)},
        {"$set": update_data.dict(exclude_unset=True)}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update allocation")

    return {**allocation, **update_data.dict()}

@router.delete("/{allocation_id}")
async def delete_allocation(allocation_id: str):
    allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation["allocation_date"] < str(datetime.date.today()):
        raise HTTPException(status_code=400, detail="Cannot delete past allocations")

    await db.allocations.delete_one({"_id": ObjectId(allocation_id)})
    return {"detail": "Allocation deleted"}

@router.get("/", response_model=List[Allocation])
async def get_allocations(employee_id: Optional[str] = None, vehicle_id: Optional[str] = None,
                           start_date: Optional[str] = None, end_date: Optional[str] = None):
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
