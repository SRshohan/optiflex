# Setting Up Optiflex Backend on Windows (Python 3.11)

## 1. Install Python 3.11
- Download Python 3.11 for Windows from the [official Python website](https://www.python.org/downloads/release/python-3110/).
- During installation, **check the box** that says "Add Python to PATH".

## 2. Open Command Prompt and Navigate to Backend
```sh
cd open-webui\backend
```

## 3. Check Python Version
Make sure you are using Python 3.11.x:
```sh
python --version
```
You should see output like:
```
Python 3.11.x
```
If not, ensure Python 3.11 is installed and available in your PATH.

## 4. Create and Activate a Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate
```
If you see a security warning, you may need to set the execution policy (run as Administrator):
```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 5. Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run the Backend Server
```sh
python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload
```
Or, you can use the provided batch file for Windows:
```sh
start_windows.bat
```

---
**You can now access the backend at** [http://localhost:8080](http://localhost:8080)




# Open WebUI: Direct Connections API Usage Guide

## Overview
This section explains how to configure, inspect, and update **Direct Connections** for Open WebUI (Optiflex) via the API. This is useful for users and developers who want to automate or debug the process of connecting to custom OpenAI-compatible endpoints.

---

## What Are Direct Connections?
- **Direct Connections** allow each user to add their own OpenAI-compatible API endpoints (e.g., LiteLLM, custom proxy, etc.) without admin access.
- These connections are stored in the user's settings and are not global.

---

## API Endpoint
- **URL:** `/api/v1/users/user/settings/update`
- **Method:** `POST`
- **Authentication:** Bearer token (user must be logged in)

---

## Example Payload
Below is a real example of the JSON payload sent by the frontend when saving direct connections:

```json
{
  "ui": {
    "directConnections": {
      "OPENAI_API_BASE_URLS": [
        "http://localhost:4000",
        "http://localhost:4000"
      ],
      "OPENAI_API_KEYS": [
        "sk-tn3WZUts7YHXB1jIJ_ZDvw",
        "sk-_XWMPOuQWWFTrvQmD1_w1g"
      ],
      "OPENAI_API_CONFIGS": {
        "0": {
          "enable": true,
          "tags": [],
          "prefix_id": "",
          "model_ids": [],
          "connection_type": "external"
        },
        "1": {
          "enable": true,
          "tags": [],
          "prefix_id": "",
          "model_ids": [],
          "connection_type": "external"
        }
      }
    },
    "webSearch": null
  }
}
```

---

## How to Inspect the Payload (Step-by-Step)
1. **Open the WebUI in your browser.**
2. **Open Developer Tools** (F12 or right-click → Inspect).
3. Go to the **Network** tab.
4. Filter for `/api/v1/users/user/settings/update`.
5. Add or edit a Direct Connection in the UI and click **Save**.
6. Click the request in the Network tab and view the **Payload** or **Request** section.
7. Copy the JSON for your own use or automation.

---

## Notes
- The `OPENAI_API_BASE_URLS`, `OPENAI_API_KEYS`, and `OPENAI_API_CONFIGS` arrays/objects must be kept in sync by index.
- The backend stores this data in the user's settings JSON field.
- This endpoint is **per-user**; each user can have their own set of direct connections.
- The `webSearch` key may be present or null, depending on your UI settings.

---

## Troubleshooting
- If you receive a `422 Unprocessable Entity` error, ensure your JSON is valid and matches the structure above.
- Do not include extra or misspelled keys.
- Always use double quotes for property names and string values in JSON.

---

## References
- Frontend: `src/lib/components/chat/Settings/Connections.svelte`, `SettingsModal.svelte`
- Backend: `open_webui/routers/users.py`, `models/users.py`

---

For further questions, inspect the browser network tab as described above, or consult the codebase for the latest structure. 


# LiteLLM: Virtual Keys Configuration Guide

## Overview
This section explains how to configure **virtual_keys** for LiteLLM, which is useful for managing API access, budgets, and user metadata in SaaS or multi-tenant environments.

---

## What Are Virtual Keys?
- **Virtual keys** allow you to create API keys that map to specific models, budgets, and user metadata.
- Useful for SaaS scenarios where you want to control access, spending, and features per user or subscription tier.

---

## Example Virtual Key Configuration
Below is an example configuration for generating a virtual key in LiteLLM:

```json
{
  "models": ["gpt-4o", "gemini-1.5-pro", "claude-3-haiku"],
  "max_budget": 10.00,
  "duration": "30d",
  "metadata": {
    "saas_user_id": "user-12345",
    "subscription_tier": "Pro"
  }
}
```

### **Field Descriptions**
- `models`: List of model names this key can access.
- `max_budget`: Maximum spend allowed for this key (in dollars or your currency).
- `duration`: Validity period for the key (e.g., `30d` for 30 days).
- `metadata`: Custom metadata for tracking user, subscription, or other info.

---

## How to Use
1. Add this configuration to your LiteLLM `config.yaml` or use the LiteLLM admin API/CLI to generate a new virtual key.
2. Distribute the generated virtual key to your user or application.
3. LiteLLM will enforce the model access, budget, and duration automatically.

---

## SaaS Use Case Example
- When a user upgrades to a "Pro" tier, generate a virtual key with higher `max_budget` and more models.
- Store the `saas_user_id` and `subscription_tier` in the `metadata` for tracking and analytics.

---

## References
- [LiteLLM Documentation](https://docs.litellm.ai/docs/virtual_keys)
- Example config: `config.yaml` in your LiteLLM deployment

---

For more advanced usage, see the LiteLLM docs or your SaaS backend logic for dynamic key generation. 
