from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import Employee, Vehicle, Allocation

class Migration:
    """
    Base class for migrations.

    This class provides an interface for database migrations, allowing for
    both upgrades and downgrades to be implemented in derived classes.
    """
    def __init__(self, version: str):
        self.version = version

    async def upgrade(self):
        """
        Apply the migration upgrade.

        This method should be overridden in derived classes to define
        the actions for upgrading the database schema or data.
        """
        raise NotImplementedError

    async def downgrade(self):
        """
        Revert the migration downgrade.

        This method should be overridden in derived classes to define
        the actions for downgrading the database schema or data.
        """
        raise NotImplementedError

class InitialMigration(Migration):
    """
    Initial migration class for setting up the database with default data.

    This migration inserts initial data into the Employee and Vehicle collections
    if they are empty.
    """
    def __init__(self):
        super().__init__(version="1.0")

    async def upgrade(self):
        """
        Upgrade the database to the initial state by inserting default data.

        This method checks if there are any existing Employee or Vehicle documents
        in the database, and if not, inserts default entries.
        """
        # Check if the Employee collection is empty and insert default data if needed
        if not await Employee.find_one():
            await Employee(name="John Doe", email="john@example.com", department="Engineering").insert()
        
        # Check if the Vehicle collection is empty and insert default data if needed
        if not await Vehicle.find_one():
            await Vehicle(license_plate="ABC123", model="Toyota", driver="Jane Smith").insert()

    async def downgrade(self):
        """
        Downgrade the database by removing the initial data.

        This method can be implemented to remove the default data inserted
        during the upgrade, if necessary.
        """
        pass  # Optional: Define downgrade logic if necessary

async def run_migrations():
    """
    Run all migrations to upgrade the database schema and data.

    This function initializes the MongoDB connection, sets up Beanie, 
    and applies all defined migrations.
    """
    # Connect to MongoDB using the specified URI
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.vehicle_allocation

    # Initialize Beanie with the document models
    await init_beanie(database, document_models=[Employee, Vehicle, Allocation])

    # List of migrations to be applied
    migrations = [InitialMigration()]

    for migration in migrations:
        print(f"Applying migration {migration.version}...")
        await migration.upgrade()  # Apply the upgrade method of the migration
        print(f"Migration {migration.version} applied.")
