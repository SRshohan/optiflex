import requests
import os

OPENWEBUI_API_URL = os.environ.get("OPENWEBUI_API_URL", "http://127.0.0.1:8080")
OPENWEBUI_ADMIN_EMAIL = os.environ.get("OPENWEBUI_ADMIN_EMAIL")
OPENWEBUI_ADMIN_PASSWORD = os.environ.get("OPENWEBUI_ADMIN_PASSWORD")

def get_admin_auth_token() -> str:
    """Authenticates with Open WebUI as an admin to get a session token."""
    print("Authenticating with Open WebUI as admin...")
    
    payload = {
        "email": OPENWEBUI_ADMIN_EMAIL,
        "password": OPENWEBUI_ADMIN_PASSWORD
    }
    
    response = requests.post(f"{OPENWEBUI_API_URL}/auths/signin", json=payload)
    
    if response.status_code == 200:
        print("Successfully authenticated with Open WebUI.")
        return response.json()["token"]
    else:
        print(f"Error authenticating with Open WebUI: {response.text}")
        raise Exception("Failed to get Open WebUI admin token.")

def add_model_to_user(user_id: str, litellm_key: str, plan: str, user_token: str):
    """
    Adds a pre-configured model to a user's account in Open WebUI.
    This makes the model selectable in their UI without them needing to enter a key.

    Args:
        user_id: The ID of the user in Open WebUI.
        litellm_key: The LiteLLM virtual key to embed.
        plan: The name of the plan (e.g., "Pro") to use for the model name.
    """
    print(f"Adding model to Open WebUI for user '{user_id}'...")



    # admin_token = get_admin_auth_token()
    
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }

    # This payload creates a new "model" entry in Open WebUI.
    # The key is that we point it to our LiteLLM proxy and embed the user's key.
    model_payload = {
        "ui": {
            "directConnections": {
            "OPENAI_API_BASE_URLS": [
                os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000")
            ],
            "OPENAI_API_KEYS": [
                litellm_key
            ],
            "OPENAI_API_CONFIGS": {
                "0": {
                "enable": True,
                "tags": [],
                "prefix_id": "",
                "model_ids": [],
                "connection_type": "external"
                },
            }
            },
            "webSearch": None
        }
    }
    response = requests.post(f"{OPENWEBUI_API_URL}/api/v1/users/user/settings/update", json=model_payload, headers=headers)
    # We need to find the correct API endpoint in Open WebUI to add a model
    # This is a placeholder for the actual endpoint, which we'll confirm later.
    # It's likely something like /models/add or within the user's settings.
    # For now, we'll assume an endpoint like this exists.
    
    # response = requests.post(f"{OPENWEBUI_API_URL}/models", json=model_payload, headers=headers)
    
    if response.status_code == 201:
        print("Successfully added model to user's Open WebUI account.")
    else:
        print(f"Error adding model to Open WebUI: {response.text}")
        raise Exception("Failed to add model to user's Open WebUI account.")

    print("Successfully added model to user's Open WebUI account.")
    print(f"Payload would be: {model_payload}") 

if __name__ == "__main__":
    token = get_admin_auth_token()
    add_model_to_user("admin2@example.com", "sk-1234", "pro", token)