#migrate.py
from app.migrations.migrations import run_migrations
from app.database import initialize_database
import asyncio

async def main():
    await initialize_database()
    await run_migrations()

if __name__ == "__main__":
    asyncio.run(main())
