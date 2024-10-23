import os
from aiocache import Cache
import asyncio

# Get cache URL from environment variable
CACHE_URL = os.getenv("CACHE_URL", "redis://localhost:6379")
cache = Cache.from_url(CACHE_URL)

async def read_item():
    try:
        # Example of storing data in Redis
        await cache.set("item_1", "value 1")  # Await the async method
        cached_value = await cache.get("item_1")  # Await the async method
        
        # If cached_value is None, it means the key doesn't exist
        if cached_value is not None:
            return {"cached_value": cached_value}
        else:
            return {"cached_value": "No data found"}
    finally:
        # Close the cache connection if necessary
        await cache.close()  # Ensure the cache connection is closed

# Main entry point
if __name__ == "__main__":
    # Use asyncio to run the async function and print the result
    result = asyncio.run(read_item())
    print(result)
