import os
from fastapi import FastAPI
import redis

app = FastAPI()

# Initialize Redis connection
# Make sure to use the correct host. If you're running Redis in Docker, you can use 'redis' as the host.
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

def read_root():
    return {"message": "Welcome to FastAPI with Docker and Redis"}

def read_item():
    # Example of storing data in Redis
    r.set(f"item_1", "value 1")
    cached_value = r.get("item_1")
    
    print(cached_value)
    
    # If cached_value is None, it means the key doesn't exist
    if cached_value is not None:
        cached_value = cached_value.decode("utf-8")  # Decode bytes to string
    else:
        cached_value = "No data found"


read_item()
