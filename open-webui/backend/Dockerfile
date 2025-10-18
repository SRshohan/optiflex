# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies for psycopg2 and other requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Use startup script that handles migrations and starts the app
CMD ["./start.sh"]