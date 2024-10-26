from beanie import Document, init_beanie
from pydantic import BaseModel

class Employee(Document):
    name: str
    email: str
    department: str

class Vehicle(Document):
    license_plate: str
    model: str
    driver: str

class Allocation(Document):
    employee_id: str
    vehicle_id: str
    allocation_date: str  # Can use datetime.date or str
    status: str  # e.g., "allocated", "available"
    
class UpdateAllocation(Document):
    vehicle_id: str
    allocation_date: str  # Can use datetime.date or str
    status: str  # e.g., "allocated", "available"
