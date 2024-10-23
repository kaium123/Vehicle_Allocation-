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
6. Run the project in locally
   uvicorn app.main:app --reload

Running the Project in docker
   docker compose up

Migrations
   To run database migrations:
   docker compose up mongodb -d
   python3 migrate.py

Caching
   The get_allocations endpoint is cached for 60 seconds using aiocache to reduce database load.

Deployment
   For production deployment, use Docker Compose:
   docker compose up
   Or deploy the API to cloud services (AWS, GCP, Azure) using container orchestration platforms like Kubernetes.

Maintenance
- Monitoring: Use tools like Prometheus and Grafana.
- Scaling: Horizontal scaling via Kubernetes.
- Logging: Centralized logging with the Loki Stack or Fluentd.
