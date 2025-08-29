# open-webui/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY ./backend/. .

# Copy package.json to the root of the container filesystem
COPY ./package.json /package.json

# Install dependencies
# Make sure you have a requirements.txt file in this directory
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# --- FIX ---
# Make the dev.sh script executable
RUN chmod +x ./dev.sh

# The port your FastAPI app runs on (must match the port in dev.sh)
EXPOSE 8080

# --- FIX ---
# Use the dev.sh script to start the application
CMD ["./dev.sh"]