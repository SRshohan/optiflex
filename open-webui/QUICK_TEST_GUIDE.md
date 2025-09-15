# Quick Test Guide for Project API

## Quick Start

### 1. Make sure Open WebUI is running:
```bash
cd /Users/sohanurrahman/Desktop/optiflex/open-webui/backend
source venv/bin/activate
uvicorn open_webui.main:app --port 8080 --host 0.0.0.0 --reload
```

### 2. Run the automated test script:
```bash
cd /Users/sohanurrahman/Desktop/optiflex/open-webui
chmod +x test_projects_api.sh
./test_projects_api.sh
```

### 3. Or set custom credentials:
```bash
export OPENWEBUI_EMAIL="your-email@example.com"
export OPENWEBUI_PASSWORD="your-password"
./test_projects_api.sh
```

## Manual Testing

### 1. Get your auth token:
```bash
TOKEN=$(curl -s -X POST "http://localhost:8080/api/v1/auths/signin" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}' | jq -r '.token')

echo "Token: $TOKEN"
```

### 2. Test basic endpoints:

**Create Project:**
```bash
curl -X POST "http://localhost:8080/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Test Project",
    "description": "Testing the API",
    "color": "#3B82F6"
  }'
```

**List Projects:**
```bash
curl -X GET "http://localhost:8080/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

**Update Project (replace PROJECT_ID):**
```bash
PROJECT_ID="your-project-id-here"
curl -X PATCH "http://localhost:8080/api/v1/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Project Name",
    "color": "#10B981"
  }'
```

**Delete Project:**
```bash
curl -X DELETE "http://localhost:8080/api/v1/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

## Expected Results

✅ **Success indicators:**
- HTTP 200/201 responses
- JSON responses with project data
- Projects appear in database
- Authentication works properly

❌ **Error indicators:**
- `{"detail": "Not authenticated"}` - Need valid token
- `{"detail": "Project not found"}` - Invalid project ID
- Connection refused - Server not running

## Troubleshooting

**Server not running:**
```bash
ps aux | grep uvicorn
# If not running, start it:
cd backend && source venv/bin/activate && uvicorn open_webui.main:app --port 8080 --reload
```

**Database issues:**
```bash
# Check if project table exists
sqlite3 backend/data/webui.db ".tables" | grep project

# Check migration status
sqlite3 backend/data/webui.db "SELECT * FROM migratehistory WHERE name = '019_add_projects';"
```

**Authentication issues:**
- Make sure you have a valid user account
- Check if email/password are correct
- Token expires after some time, get a new one

## Database Verification

```bash
# Check projects in database
sqlite3 backend/data/webui.db "SELECT id, name, user_id FROM project;"

# Check chats assigned to projects
sqlite3 backend/data/webui.db "SELECT id, title, folder_id FROM chat WHERE folder_id IS NOT NULL;"
```

## API Documentation

For complete API documentation, see: `PROJECT_API_TESTING.md`

---

**Happy Testing! 🚀**
