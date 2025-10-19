#!/bin/bash
set -e

# Set environment variables for Cloud SQL
export DATABASE_URL="postgresql+psycopg2://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=${DB_SOCKET}"

# Set the DATABASE_URL for OpenWebUI's internal db module (needs postgres:// scheme)
export OPENWEBUI_DATABASE_URL="postgres://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=${DB_SOCKET}"

# Override the DATABASE_URL in the internal db module
export DATABASE_URL="$OPENWEBUI_DATABASE_URL"

# Set CORS to allow localhost for development
export CORS_ALLOW_ORIGIN="*"

export OPENAI_API_BASE_URL='https://proxy-server.optiflex.ai'
export OPENAI_API_KEY='sk-aa6AcxKfnOc9zjDdKxrgiw'

echo "Starting OpenWebUI backend..."
cd /app
exec uvicorn open_webui.main:app --host 0.0.0.0 --port 8080