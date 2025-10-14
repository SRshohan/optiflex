# # optiflex/backend/Dockerfile
# FROM python:3.11-slim

# WORKDIR /app

# # Copy application files
# COPY . .

# # Copy package.json to the root of the container filesystem
# # COPY ./package.json /package.json

# # Install dependencies
# # Make sure you have a requirements.txt file in this directory
# RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# # ENV INSTANCE_CONNECTION_NAME=optiflex-test:us-central1:optiflex-sql-instance
# # ENV DB_NAME=optiflex-db
# # ENV DB_USER=postgres
# # ENV DB_PASSWORD=postgres

# # --- FIX ---
# # Make the start.sh script executable
# # RUN chmod +x ./start.sh

# # The port your FastAPI app runs on (must match the port in start.sh)
# EXPOSE 8080

# # --- FIX ---
# # Use the start.sh script to start the application
# CMD ["uvicorn", "open_webui.main:app", "--port", "8080", "--host", "0.0.0.0", "--forwarded-allow-ips", "*"]

# optiflex/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY . .

# Install dependencies including Cloud SQL connector
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt && \
    pip install cloud-sql-python-connector[pg8000]==1.11.0 pg8000==1.31.2

# Expose port
EXPOSE 8080

# Run uvicorn directly - simple and clear
CMD ["python", "-m", "uvicorn", "open_webui.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--forwarded-allow-ips", "*"]
