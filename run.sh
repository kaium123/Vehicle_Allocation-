#!/bin/sh

# Wait for MongoDB to be ready
while ! nc -z mongodb 27017; do
  echo "Waiting for MongoDB..."
  sleep 1
done

echo "MongoDB is ready, starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
