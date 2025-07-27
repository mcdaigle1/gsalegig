# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

RUN python3 -m pip install --upgrade pip setuptools wheel requests

# Step 5: Install dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application code to the container
COPY . .

# Step 7: Expose the port on which the API will run
EXPOSE 8080

# Step 8: Define the entry point for Gunicorn
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "app:app", "--workers", "4"]