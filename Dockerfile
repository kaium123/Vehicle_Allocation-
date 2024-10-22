# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install netcat (specifically netcat-openbsd) and any other dependencies you need
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and give it executable permissions
COPY run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/usr/local/bin/run.sh"]

# Command to run the FastAPI app (not needed as it's handled in run.sh)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
