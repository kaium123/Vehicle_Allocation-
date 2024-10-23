from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from bson import ObjectId

# Pydantic model for vehicle allocations
class Allocation(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID field, mapped from MongoDB's ObjectId
    employee_id: Optional[str]  # ID of the employee being allocated a vehicle
    vehicle_id: str  # ID of the allocated vehicle
    allocation_date: date  # Date of allocation

    class Config:
        # Allows the model to use field names different from MongoDB's key names
        allow_population_by_field_name = True
        # This encoder ensures that ObjectId is converted to string for JSON serialization
        json_encoders = {
            ObjectId: str
        }
