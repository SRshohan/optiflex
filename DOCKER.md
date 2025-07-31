# Docker Workflow Guide

This document explains the two primary Docker workflows for this project: one for rapid **development** and one for a stable **production** deployment.

## 1. Development Workflow

The development environment is designed for speed, live-reloading, and easy debugging. It achieves this by running the frontend and backend as two separate, coordinated servers.

### Architecture:

-   **Backend Server**: Runs inside a Docker container using the `docker-compose.dev.yml` file.
    -   It uses `uvicorn --reload` to automatically restart the Python server whenever you save a change to a `.py` file.
    -   Your local code from the `./open-webui` directory is mounted directly into the container as a volume. This means changes are reflected instantly without rebuilding the image.
-   **Frontend Server**: Runs on your **local machine** (not in Docker).
    -   You start it by running `npm run dev` from within the `open-webui` directory.
    -   It uses the SvelteKit development server, which provides Hot Module Replacement (HMR) for an incredibly fast UI development experience.

### How to Run:

You will need **two terminals** open simultaneously.

**Terminal 1: Start the Backend**
```bash
# From the project root directory
docker-compose -f docker-compose.yaml -f docker-compose.dev.yml up
```
*Leave this running. You will see live logs from your Python application here.*

**Terminal 2: Start the Frontend**
```bash
# Navigate into the frontend directory
cd open-webui

# Install dependencies (only needs to be done once)
npm install

# Start the dev server
npm run dev
```
*After it starts, you can access the application at the URL it provides, typically `http://localhost:5173`.*

---

## 2. Production Workflow

The production environment is designed for stability, performance, and simplicity of deployment. It achieves this by building the frontend and backend into a single, self-contained Docker image.

### Architecture:

-   **Single-Container Service**: The `Dockerfile.prod` uses a multi-stage build process:
    1.  **Build Stage**: An initial stage uses a Node.js image to run `npm run build`. This compiles all your SvelteKit code into a small, optimized set of static files (`index.html`, JavaScript, and CSS).
    2.  **Final Stage**: A second stage uses a Python image to set up the backend API server. It then **copies the built static files** from the first stage into the final image.
-   **Unified Server**: When the container runs, a single Python server is responsible for both:
    1.  Serving all API requests (e.g., `/api/v1/...`).
    2.  Serving the pre-built frontend website.
-   **Configuration**: The entire application is configured via environment variables set in the `docker-compose.prod.yml` file. For best practice, these should be moved to a `.env` file, which should **not** be committed to version control.

### How to Run:

You only need **one terminal** for deployment.

```bash
# From the project root directory, on your production server
# The --build flag is only necessary the first time or after code changes.
# The -d flag runs the container in the background (detached mode).
docker-compose -f docker-compose.prod.yml up --build -d
```

### How to Test Production Locally (Dress Rehearsal)

Before deploying to a live server, you should always test the production container on your local machine. This ensures the build process works and that the unified frontend/backend service runs correctly.

1.  **Stop all development servers** to avoid port conflicts (`npm run dev` and `docker-compose.dev.yml`).
2.  **Temporarily edit `docker-compose.prod.yml` for local testing:**
    -   Set `LITELLM_API_URL` to `http://host.docker.internal:4000`. This special DNS name allows the `open-webui` container to connect to the `litellm` service running on your host machine. `localhost` will **not** work from inside the container for this purpose.
    -   Set `WEBUI_URL` to `http://localhost:8080`.
3.  **Build and run the production container:**
    ```bash
    # From the project root, run without -d to see the logs
    docker-compose -f docker-compose.prod.yml up --build
    ```
4.  **Test the application** by visiting `http://localhost:8080` in your browser.

**Important**: Remember to change the URLs in `docker-compose.prod.yml` back to your real public domains before deploying to your server.

---

## Workflow Summary

| Aspect         | Development (`docker-compose.dev.yml`)                                | Production (`docker-compose.prod.yml`)                                |
| :------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| **Goal**       | Fast Reloading & Debugging                                            | Stability & Performance                                               |
| **Frontend**   | Runs as `npm run dev` on your Mac (Port `5173`)                       | Pre-built into static files inside the container                      |
| **Backend**    | Runs as `uvicorn` inside Docker (Port `8080`)                         | Runs as a single server inside Docker (Port `8080`)                   |
| **`WEBUI_URL`**  | `http://localhost:5173` (Tells backend where the separate frontend is) | `https://your-domain.com` (Tells the app its own public URL)          |
| **Code Changes** | Instantly reflected via live-reload and HMR                           | Requires rebuilding the Docker image (`--build`)                      | 