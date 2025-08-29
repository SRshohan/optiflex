import requests
import os

OPENWEBUI_API_URL = os.environ.get("OPENWEBUI_API_URL", "http://127.0.0.1:8080")
OPENWEBUI_ADMIN_EMAIL = os.environ.get("OPENWEBUI_ADMIN_EMAIL")
OPENWEBUI_ADMIN_PASSWORD = os.environ.get("OPENWEBUI_ADMIN_PASSWORD")



def get_user_id_by_email(email: str) -> str:
    """
    Uses an admin token to find a user's ID by their email.
    NOTE: OpenWebUI API might not have a direct search endpoint.
    This is a placeholder for that logic. You might need to list all users and find the one you need.
    """
    # This is a conceptual function. You'll need to implement the actual user search logic.
    # For now, let's assume you can get the user's ID.
    print(f"Fetching user ID for email {email}...")
    # In a real scenario, you would call GET /api/v1/users/ and search the list.
    # We will need to add this logic if it doesn't exist.
    # For now, we mock it.
    admin_token = get_admin_token()
    users_response = requests.get(f"{OPENWEBUI_API_URL}/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    if users_response.status_code == 200:
        users = users_response.json()["users"]
        for user in users:
            if user['email'] == email:
                return user['id']
    raise Exception(f"User with email {email} not found.")



def add_model_to_user(user_id: str, litellm_key: str, plan: str, admin_token: str):
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
        "Authorization": f"Bearer {admin_token}",
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
    response = requests.post(f"{OPENWEBUI_API_URL}/api/v1/users/{user_id}/settings/update", json=model_payload, headers=headers)
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


def get_admin_token() -> str:
    """
    Gets a user's token from Open WebUI.
    """
    user_email = os.environ.get("OPENWEBUI_ADMIN_EMAIL", "admin@example.com")
    user_password = os.environ.get("OPENWEBUI_ADMIN_PASSWORD", "admin123")
    response = requests.post(f"{OPENWEBUI_API_URL}/api/v1/auths/signin", json={"email": user_email, "password": user_password})
    return response.json()["token"]

if __name__ == "__main__":
    token = get_admin_token()
    add_model_to_user("admin2@example.com", "sk-1234", "pro", token)