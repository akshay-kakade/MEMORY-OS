# Use Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code only
COPY . .

# Expose Render port (Render injects its own PORT)
ENV PORT=8000
EXPOSE 8000

# Run FastAPI backend
CMD ["python", "start.py"]
