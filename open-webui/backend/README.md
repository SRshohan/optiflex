# OpenWebUI Backend - Google Cloud Run Deployment

This document provides step-by-step instructions for deploying OpenWebUI backend to Google Cloud Run with Cloud SQL PostgreSQL using Unix socket connections.

## 🎯 Overview

- **Platform**: Google Cloud Run
- **Database**: Cloud SQL PostgreSQL
- **Connection Method**: Unix domain socket (`/cloudsql/...`)
- **Container**: Docker with Uvicorn
- **Memory**: 2Gi (required for OpenWebUI's ML dependencies)

## 📋 Prerequisites

1. Google Cloud Project with billing enabled
2. Cloud SQL PostgreSQL instance
3. Cloud Run and Cloud Build APIs enabled
4. `gcloud` CLI installed and authenticated

## 🔧 Environment Variables

Set these environment variables before running deployment commands:

```bash
export PROJECT_ID=optiflex-test
export INSTANCE_CONNECTION_NAME=optiflex-test:us-central1:optiflex-sql-instance
export DB_NAME=optiflex-db
export DB_USER=optiflex-user
export DB_PASS=REDACTED
```

## 🚀 Deployment Steps

### 1. Enable Required APIs
```bash
gcloud services enable run.googleapis.com sqladmin.googleapis.com cloudbuild.googleapis.com
```
**Purpose**: Enables Cloud Run, Cloud SQL Admin, and Cloud Build services.

### 2. Build Docker Image
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/openwebui-backend
```
**Purpose**: Builds the Docker image from Dockerfile and pushes to Google Container Registry.

### 3. Fix Database User Password
```bash
gcloud sql users set-password optiflex-user --instance=optiflex-sql-instance --password=$DB_PASS
```
**Purpose**: Ensures Cloud SQL user password matches environment variable.

### 4. Deploy to Cloud Run
```bash
gcloud run deploy openwebui-backend \
  --image gcr.io/$PROJECT_ID/openwebui-backend \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances $INSTANCE_CONNECTION_NAME \
  --set-env-vars INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME,DB_NAME=$DB_NAME,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_SOCKET=/cloudsql/$INSTANCE_CONNECTION_NAME \
  --memory=2Gi --cpu=2 --timeout=900
```
**Purpose**: Deploys the main OpenWebUI service with Cloud SQL connection.

### 5. Create Migration Job
```bash
gcloud run jobs create openwebui-migrations \
  --image gcr.io/$PROJECT_ID/openwebui-backend \
  --region us-central1 \
  --set-cloudsql-instances $INSTANCE_CONNECTION_NAME \
  --set-env-vars INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME,DB_NAME=$DB_NAME,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_SOCKET=/cloudsql/$INSTANCE_CONNECTION_NAME \
  --command="bash" --args="-c,cd /app/open_webui && alembic upgrade head" \
  --memory=1Gi --cpu=1
```
**Purpose**: Creates a Cloud Run Job for running database migrations. The job runs `alembic upgrade head` from the correct directory (`/app/open_webui`) where the `alembic.ini` configuration file is located.

### 6. Execute Migrations
```bash
gcloud run jobs execute openwebui-migrations --region us-central1
```
**Purpose**: Runs database migrations to set up the schema.

### 7. Set IAM Permissions
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:953676742197-compute@developer.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```
**Purpose**: Grants Cloud Run service account permission to connect to Cloud SQL.

### 8. Test Deployment
```bash
curl -I https://openwebui-backend-953676742197.us-central1.run.app
```
**Purpose**: Verifies the service is running and accessible.

## 🔍 Key Files

### `start.sh`
```bash
#!/bin/bash
set -e

# Set environment variables for Cloud SQL
export DATABASE_URL="postgresql+psycopg2://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=${DB_SOCKET}"

# Set the DATABASE_URL for OpenWebUI's internal db module (needs postgres:// scheme)
export OPENWEBUI_DATABASE_URL="postgres://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=${DB_SOCKET}"

# Override the DATABASE_URL in the internal db module
export DATABASE_URL="$OPENWEBUI_DATABASE_URL"

echo "Starting OpenWebUI backend..."
cd /app
exec uvicorn open_webui.main:app --host 0.0.0.0 --port 8080
```
**Purpose**: Sets correct DATABASE_URL format for OpenWebUI's Peewee ORM.

### `Dockerfile`
```dockerfile
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

# Use startup script
CMD ["./start.sh"]
```
**Purpose**: Production-ready container configuration for Cloud Run.

## 🚨 Troubleshooting

### Common Issues

1. **Memory Exhaustion**
   - **Error**: `Memory limit exceeded (512 MiB)`
   - **Solution**: Increase memory to `--memory=2Gi`

2. **Database Scheme Mismatch**
   - **Error**: `Unrecognized or unsupported scheme: "postgresql+psycopg2"`
   - **Solution**: Use `postgres://` scheme in `start.sh` for OpenWebUI's Peewee ORM

3. **Username Mismatch**
   - **Error**: `password authentication failed for user "optiflex_user"`
   - **Solution**: Use correct username `optiflex-user` (with hyphen)

4. **Password Authentication Failed**
   - **Error**: `FATAL: password authentication failed`
   - **Solution**: Update Cloud SQL user password with `gcloud sql users set-password`

5. **Missing IAM Permissions**
   - **Error**: Connection refused to Cloud SQL
   - **Solution**: Grant `roles/cloudsql.client` to service account

6. **Migration Job: No config file 'alembic.ini' found**
   - **Error**: `FAILED: No config file 'alembic.ini' found, or file has no '[alembic]' section`
   - **Solution**: Use `--command="bash" --args="-c,cd /app/open_webui && alembic upgrade head"` to run from correct directory

## 📊 Service Information

- **Service URL**: https://openwebui-backend-953676742197.us-central1.run.app
- **Region**: us-central1
- **Memory**: 2Gi
- **CPU**: 2 cores
- **Database**: Cloud SQL PostgreSQL via Unix socket

## 🔄 Migration Commands

To run migrations manually:
```bash
# Execute migration job
gcloud run jobs execute openwebui-migrations --region us-central1

# Check migration status
gcloud run jobs executions describe openwebui-migrations-XXXX --region us-central1
```

## 🤔 Why Do We Need a Migration Job?

### **The Problem:**
OpenWebUI requires database migrations to run before the main application can start. These migrations:
- Create database tables (`users`, `chats`, `messages`, `files`, etc.)
- Set up the database schema and relationships
- Initialize the database structure
- Must complete **before** the main service starts serving requests

### **Why Not Run Migrations in the Main Service?**

| **Issue** | **Explanation** |
|-----------|-----------------|
| **Startup Reliability** | If migrations fail, the entire service fails to start |
| **Performance** | Migrations can be slow, delaying service startup |
| **Resource Conflicts** | Running migrations while serving requests can cause conflicts |
| **Separation of Concerns** | Database setup should be separate from application serving |

### **What the Migration Job Does:**

```bash
--command="bash" --args="-c,cd /app/open_webui && alembic upgrade head"
```

**Translation**: `cd /app/open_webui && alembic upgrade head`

**Steps**:
1. **Changes directory** to `/app/open_webui` (where `alembic.ini` is located)
2. **Runs `alembic upgrade head`** to apply all pending migrations
3. **Creates database tables** for OpenWebUI functionality
4. **Sets up indexes** and relationships
5. **Initializes the database** for production use

### **Job vs Service:**

| **Cloud Run Service** | **Cloud Run Job** |
|----------------------|-------------------|
| **Purpose**: Serves HTTP requests | **Purpose**: Runs one-time tasks |
| **Lifecycle**: Long-running, always available | **Lifecycle**: Runs once, then stops |
| **Access**: Public URL, handles traffic | **Access**: Internal, no public URL |
| **Use Case**: Web application | **Use Case**: Database migrations, data processing |

## 📝 Notes

- OpenWebUI uses Peewee ORM internally, not SQLAlchemy
- The `start.sh` script is crucial for setting the correct DATABASE_URL format
- Cloud SQL connection uses Unix domain socket at `/cloudsql/$INSTANCE_CONNECTION_NAME`
- Memory requirements are high due to ML dependencies (PyTorch, etc.)
- All database credentials are passed via environment variables (no hardcoding)

## Github Commit Rollback
1. Find the commit hash(es):
```sh
git log --oneline
```

2. Revert them (example: last commit):
```sh
git revert HEAD
```

3. Push
```sh
git push origin main
```

## Adding Development Environment in Vercel

Go to Second Long Link for the environment

## 🎉 Success Indicators

- Service responds with HTTP status (404 is expected for root path)
- No authentication errors in logs
- Database migrations complete successfully
- Service starts within timeout period

