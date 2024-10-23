Vehicle Allocation API
This project provides a FastAPI-based API for managing vehicle allocations, with MongoDB as the database using Beanie for ODM.

Installation
Prerequisites
Python 3.8+
MongoDB (Local or Docker)
Docker (optional, for containerized deployment)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/vehicle-allocation-api.git
cd vehicle-allocation-api
Create and activate a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Ensure MongoDB is running:

bash
Copy code
docker run --name mongodb -p 27017:27017 -d mongo
Running the Project
Locally
Run the app:

bash
Copy code
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.

Using Docker
Build the Docker image:

bash
Copy code
docker build -t vehicle-allocation-api .
Run the container:

bash
Copy code
docker run -d -p 8000:8000 vehicle-allocation-api
Migrations
To run database migrations:

bash
Copy code
python -m app.migrations.migration run_migrations
Testing
To run tests:

bash
Copy code
pytest
Caching
The get_allocations endpoint is cached for 60 seconds using aiocache to reduce database load.

Deployment
For production deployment, use Docker Compose:

bash
Copy code
docker-compose up --build
Or deploy the API to cloud services (AWS, GCP, Azure) using container orchestration platforms like Kubernetes.

Maintenance
Monitoring: Use tools like Prometheus and Grafana.
Scaling: Horizontal scaling via Kubernetes.
Logging: Centralized logging with the ELK Stack or Fluentd.