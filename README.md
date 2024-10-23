Vehicle Allocation API
This project provides a FastAPI-based API for managing vehicle allocations, with MongoDB as the database using Beanie for ODM.

Installation
Prerequisites
- Python 3.8+
- MongoDB (Local or Docker)
- Docker (optional, for containerized deployment)

Steps
1. Clone the repository:
   git clone https://github.com/kaium123/Vehicle_Allocation-.git
   cd Vehicle_Allocation
2. Create and activate a virtual environment:
   python3 -m venv myvenv
   source myvenv/bin/activate
3. Install dependencies:
   pip3 install -r requirements.txt
4. Ensure MongoDB is running:
   docker run --name mongodb -p 27017:27017 -d mongo
5. Ensure MongoDB is running:
   docker run --name redis -p 6379:6379 -d redis

Running the Project
Locally
- Run the app:
   uvicorn app.main:app --reload
   The API will be available at http://localhost:8000.

Using Docker
1. Build the Docker image:
   docker build -t vehicle-allocation-api .
2. Run the container:
   docker run -d -p 8000:8000 vehicle-allocation-api

Migrations
To run database migrations:
python -m app.migrations.migration run_migrations

Caching
The get_allocations endpoint is cached for 60 seconds using aiocache to reduce database load.

Deployment
For production deployment, use Docker Compose:
docker-compose up --build
Or deploy the API to cloud services (AWS, GCP, Azure) using container orchestration platforms like Kubernetes.

Maintenance
- Monitoring: Use tools like Prometheus and Grafana.
- Scaling: Horizontal scaling via Kubernetes.
- Logging: Centralized logging with the ELK Stack or Fluentd.
