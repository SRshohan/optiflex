# Project API Documentation

This document describes the Project API endpoints for organizing chats into project folders.

## Access Swagger UI

Visit: `http://localhost:8080/docs` to test all endpoints interactively.

## API Endpoints

### 1. **GET** `/api/v1/projects`
**Purpose:** List all projects for the authenticated user  
**Returns:** Array of projects (owned + shared)  
**Auth:** Required  

### 2. **POST** `/api/v1/projects`
**Purpose:** Create a new project  
**Body:**
```json
{
  "name": "string (required)",
  "description": "string (optional)", 
  "color": "string (optional, hex color)"
}
```
**Returns:** Created project object  
**Auth:** Required  

### 3. **GET** `/api/v1/projects/{project_id}`
**Purpose:** Get details of a specific project  
**Returns:** Project object  
**Auth:** Required (must own or have access to project)  

### 4. **PATCH** `/api/v1/projects/{project_id}`
**Purpose:** Update project details  
**Body:** Any combination of name, description, color  
**Returns:** Updated project object  
**Auth:** Required (must own project)  

### 5. **DELETE** `/api/v1/projects/{project_id}`
**Purpose:** Delete a project and unassign all its chats  
**Returns:** Success message  
**Auth:** Required (must own project)  

### 6. **GET** `/api/v1/projects/{project_id}/chats`
**Purpose:** Get all chats assigned to a project  
**Returns:** Array of chat objects  
**Auth:** Required (must have access to project)  

### 7. **POST** `/api/v1/projects/{project_id}/chats/{chat_id}`
**Purpose:** Assign an existing chat to a project  
**Returns:** Success message  
**Auth:** Required (must own both project and chat)  

### 8. **DELETE** `/api/v1/projects/{project_id}/chats/{chat_id}`
**Purpose:** Remove chat from project (chat still exists, just unassigned)  
**Returns:** Success message  
**Auth:** Required (must own project and chat)  

## Backend Implementation

### Database Schema
- **Table:** `project`
- **Key Fields:** id, user_id, name, description, color, created_at, updated_at
- **Relationship:** Chat.folder_id → Project.id (reuses existing folder_id field)

### Models
- **SQLAlchemy Model:** `open_webui/models/projects.py`
- **Router:** `open_webui/routers/projects.py`
- **Migration:** `019_add_projects.py`

### Key Functions

**ProjectTable.get_projects_by_user_id()**  
- Fetches projects owned by or shared with user
- Includes SQLite/PostgreSQL JSON queries for sharing permissions

**ProjectTable.insert_new_project()**  
- Creates new project with UUID
- Sets timestamps and default values

**Chats.update_chat_project_id_by_id_and_user_id()**  
- Assigns/unassigns chat to project via folder_id field
- Unpins chat when moved to project

### Authentication
- Uses JWT tokens via `get_verified_user` dependency
- All endpoints require authentication
- Users can only access their own projects and chats

### Error Handling
- **401:** Not authenticated
- **404:** Project/chat not found or no access
- **400:** Validation errors (missing required fields)

## Usage Flow

1. **Create Project** → Get project_id
2. **Create/Find Chats** → Get chat_id(s) 
3. **Assign Chats to Project** → Organize conversations
4. **View Project Chats** → See organized conversations
5. **Update/Delete** → Manage projects as needed

## Testing

Use FastAPI Swagger UI at `http://localhost:8080/docs` for interactive testing.

For automated testing, run:
```bash
./test_projects_api.sh
```

---

**That's it!** Simple project organization for Open WebUI chats. 🚀
