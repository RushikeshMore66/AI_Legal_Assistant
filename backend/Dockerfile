FROM python:3.11-slim

WORKDIR /app

# Install build dependencies that might be required
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
