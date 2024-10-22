# migration.py
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import Employee, Vehicle, Allocation

class Migration:
    def __init__(self, version: str):
        self.version = version

    async def upgrade(self):
        raise NotImplementedError

    async def downgrade(self):
        raise NotImplementedError

class InitialMigration(Migration):
    def __init__(self):
        super().__init__(version="1.0")

    async def upgrade(self):
        # Optionally, insert initial data if needed
        if not await Employee.find_one():
            await Employee(name="John Doe", email="john@example.com", department="Engineering").insert()
        if not await Vehicle.find_one():
            await Vehicle(license_plate="ABC123", model="Toyota", driver="Jane Smith").insert()

    async def downgrade(self):
        # Optional: Define downgrade logic if necessary
        pass

async def run_migrations():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.vehicle_allocation

    # Initialize Beanie
    await init_beanie(database, document_models=[Employee, Vehicle, Allocation])

    # Run migrations
    migrations = [InitialMigration()]

    for migration in migrations:
        print(f"Applying migration {migration.version}...")
        await migration.upgrade()
        print(f"Migration {migration.version} applied.")
