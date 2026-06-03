# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for OCR, Node, and frontend tooling
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

WORKDIR /app

# Create data directory for ChromaDB
RUN mkdir -p data/chroma

# Set environment variables
ENV PYTHONPATH=.
ENV MEMORYOS_BACKEND_PORT=8001
ENV MEMORYOS_FRONTEND_PORT=5173

# Expose ports for FastAPI (8001) and Vite frontend (5173)
EXPOSE 8001
EXPOSE 5173

# Run the start script
CMD ["python", "start.py"]
