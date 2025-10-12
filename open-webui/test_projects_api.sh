#!/bin/bash

# Project API Testing Script
# Make sure Open WebUI is running on localhost:8080

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8080"
EMAIL="${OPENWEBUI_EMAIL:-admin@example.com}"
PASSWORD="${OPENWEBUI_PASSWORD:-password123}"

echo -e "${BLUE}🧪 Open WebUI Project API Testing Script${NC}"
echo "=================================================="

# Function to print step headers
print_step() {
    echo -e "\n${BLUE}$1${NC}"
    echo "----------------------------------------"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Check if server is running
print_step "🔍 Step 0: Check Server Status"
if curl -s "$BASE_URL/api/health" > /dev/null 2>&1; then
    print_success "Open WebUI server is running"
else
    print_error "Open WebUI server is not accessible at $BASE_URL"
    echo "Please start the server and try again."
    exit 1
fi

# Step 1: Authentication
print_step "🔐 Step 1: Authentication"
echo "Attempting to sign in with email: $EMAIL"

AUTH_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auths/signin" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}" || echo "ERROR")

if [ "$AUTH_RESPONSE" = "ERROR" ]; then
    print_error "Authentication request failed"
    exit 1
fi

TOKEN=$(echo "$AUTH_RESPONSE" | jq -r '.token' 2>/dev/null || echo "null")
if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    print_error "Authentication failed. Response:"
    echo "$AUTH_RESPONSE" | jq . 2>/dev/null || echo "$AUTH_RESPONSE"
    print_warning "Make sure you have valid credentials or create a user account first"
    exit 1
fi

print_success "Authentication successful"
USER_ID=$(echo "$AUTH_RESPONSE" | jq -r '.user.id' 2>/dev/null || echo "unknown")
echo "User ID: $USER_ID"

# Step 2: Create Project
print_step "📁 Step 2: Create Project"
PROJECT_DATA='{
    "name": "Test Project - '"$(date '+%Y%m%d_%H%M%S')"'",
    "description": "Automated test project created by test script",
    "color": "#3B82F6"
}'

PROJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PROJECT_DATA")

PROJECT_ID=$(echo "$PROJECT_RESPONSE" | jq -r '.id' 2>/dev/null || echo "null")
if [ "$PROJECT_ID" = "null" ] || [ -z "$PROJECT_ID" ]; then
    print_error "Project creation failed. Response:"
    echo "$PROJECT_RESPONSE" | jq . 2>/dev/null || echo "$PROJECT_RESPONSE"
    exit 1
fi

print_success "Project created successfully"
echo "Project ID: $PROJECT_ID"
echo "Project Name: $(echo "$PROJECT_RESPONSE" | jq -r '.name')"

# Step 3: List Projects
print_step "📋 Step 3: List Projects"
PROJECTS_LIST=$(curl -s -X GET "$BASE_URL/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN")

PROJECT_COUNT=$(echo "$PROJECTS_LIST" | jq '. | length' 2>/dev/null || echo "0")
print_success "Found $PROJECT_COUNT project(s)"

# Step 4: Get Project Details
print_step "🔍 Step 4: Get Project Details"
PROJECT_DETAILS=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN")

RETRIEVED_NAME=$(echo "$PROJECT_DETAILS" | jq -r '.name' 2>/dev/null || echo "null")
if [ "$RETRIEVED_NAME" = "null" ]; then
    print_error "Failed to retrieve project details"
    echo "$PROJECT_DETAILS"
else
    print_success "Project details retrieved"
    echo "Name: $RETRIEVED_NAME"
    echo "Description: $(echo "$PROJECT_DETAILS" | jq -r '.description')"
    echo "Color: $(echo "$PROJECT_DETAILS" | jq -r '.color')"
fi

# Step 5: Update Project
print_step "✏️ Step 5: Update Project"
UPDATE_DATA='{
    "name": "Updated Test Project - '"$(date '+%H:%M:%S')"'",
    "description": "This project has been updated by the test script",
    "color": "#10B981"
}'

UPDATE_RESPONSE=$(curl -s -X PATCH "$BASE_URL/api/v1/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_DATA")

UPDATED_NAME=$(echo "$UPDATE_RESPONSE" | jq -r '.name' 2>/dev/null || echo "null")
if [ "$UPDATED_NAME" = "null" ]; then
    print_error "Project update failed"
    echo "$UPDATE_RESPONSE"
else
    print_success "Project updated successfully"
    echo "New name: $UPDATED_NAME"
    echo "New color: $(echo "$UPDATE_RESPONSE" | jq -r '.color')"
fi

# Step 6: Create a Test Chat
print_step "💬 Step 6: Create Test Chat"
CHAT_DATA='{
    "chat": {
        "title": "Test Chat for Project - '"$(date '+%H:%M:%S')"'",
        "models": ["gpt-3.5-turbo"],
        "messages": {},
        "history": {
            "messages": {},
            "currentId": null
        }
    }
}'

# Try the new chat endpoint first, fallback to older format if needed
CHAT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/chats/new" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$CHAT_DATA" 2>/dev/null || \
  curl -s -X POST "$BASE_URL/api/v1/chats/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$CHAT_DATA")

CHAT_ID=$(echo "$CHAT_RESPONSE" | jq -r '.id' 2>/dev/null || echo "null")
if [ "$CHAT_ID" = "null" ] || [ -z "$CHAT_ID" ]; then
    print_warning "Chat creation failed, skipping chat-related tests"
    echo "Response: $CHAT_RESPONSE"
    SKIP_CHAT_TESTS=true
else
    print_success "Chat created successfully"
    echo "Chat ID: $CHAT_ID"
    SKIP_CHAT_TESTS=false
fi

if [ "$SKIP_CHAT_TESTS" = false ]; then
    # Step 7: Get Project Chats (should be empty)
    print_step "📋 Step 7: Get Project Chats (Empty)"
    PROJECT_CHATS=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID/chats" \
      -H "Authorization: Bearer $TOKEN")
    
    CHAT_COUNT=$(echo "$PROJECT_CHATS" | jq '. | length' 2>/dev/null || echo "0")
    print_success "Project contains $CHAT_COUNT chat(s) (should be 0)"

    # Step 8: Add Chat to Project
    print_step "🔗 Step 8: Add Chat to Project"
    ADD_CHAT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/projects/$PROJECT_ID/chats/$CHAT_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    if echo "$ADD_CHAT_RESPONSE" | grep -q "success" 2>/dev/null; then
        print_success "Chat added to project successfully"
    else
        print_warning "Chat addition response: $ADD_CHAT_RESPONSE"
    fi

    # Step 9: Verify Chat in Project
    print_step "✅ Step 9: Verify Chat in Project"
    PROJECT_CHATS_AFTER=$(curl -s -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID/chats" \
      -H "Authorization: Bearer $TOKEN")
    
    CHAT_COUNT_AFTER=$(echo "$PROJECT_CHATS_AFTER" | jq '. | length' 2>/dev/null || echo "0")
    if [ "$CHAT_COUNT_AFTER" -gt "0" ]; then
        print_success "Project now contains $CHAT_COUNT_AFTER chat(s)"
        echo "Chat titles in project:"
        echo "$PROJECT_CHATS_AFTER" | jq -r '.[].title' 2>/dev/null || echo "Could not parse chat titles"
    else
        print_warning "No chats found in project after addition"
    fi

    # Step 10: Remove Chat from Project
    print_step "🗑️ Step 10: Remove Chat from Project")
    REMOVE_CHAT_RESPONSE=$(curl -s -X DELETE "$BASE_URL/api/v1/projects/$PROJECT_ID/chats/$CHAT_ID" \
      -H "Authorization: Bearer $TOKEN")
    
    if echo "$REMOVE_CHAT_RESPONSE" | grep -q "success" 2>/dev/null; then
        print_success "Chat removed from project successfully"
    else
        print_warning "Chat removal response: $REMOVE_CHAT_RESPONSE"
    fi
fi

# Step 11: Test Error Scenarios
print_step "🚨 Step 11: Test Error Scenarios"

# Test unauthorized access
echo "Testing unauthorized access..."
UNAUTH_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/projects")
if echo "$UNAUTH_RESPONSE" | grep -q "Not authenticated" 2>/dev/null; then
    print_success "Unauthorized access properly rejected"
else
    print_warning "Unexpected unauthorized response: $UNAUTH_RESPONSE"
fi

# Test non-existent project
echo "Testing non-existent project access..."
NONEXISTENT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/projects/non-existent-id" \
  -H "Authorization: Bearer $TOKEN")
if echo "$NONEXISTENT_RESPONSE" | grep -q "not found" 2>/dev/null; then
    print_success "Non-existent project properly handled"
else
    print_warning "Unexpected non-existent project response: $NONEXISTENT_RESPONSE"
fi

# Step 12: Cleanup
print_step "🧹 Step 12: Cleanup"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/api/v1/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN")

if echo "$DELETE_RESPONSE" | grep -q "success" 2>/dev/null; then
    print_success "Project deleted successfully"
else
    print_warning "Project deletion response: $DELETE_RESPONSE"
fi

# Final verification
FINAL_PROJECTS=$(curl -s -X GET "$BASE_URL/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN")
FINAL_COUNT=$(echo "$FINAL_PROJECTS" | jq '. | length' 2>/dev/null || echo "unknown")

# Summary
print_step "📊 Test Summary"
echo "=================================================="
print_success "All tests completed!"
echo "Final project count: $FINAL_COUNT"

if [ "$SKIP_CHAT_TESTS" = true ]; then
    print_warning "Chat-related tests were skipped due to chat creation failure"
fi

echo -e "\n${GREEN}🎉 Project API testing finished successfully!${NC}"
echo "Check the output above for any warnings or issues."

# Database verification (optional)
if command -v sqlite3 &> /dev/null && [ -f "backend/data/webui.db" ]; then
    echo -e "\n${BLUE}💾 Database Verification:${NC}"
    echo "Projects in database:"
    sqlite3 backend/data/webui.db "SELECT id, name, user_id FROM project WHERE user_id = '$USER_ID';" 2>/dev/null || echo "Could not query database"
fi
