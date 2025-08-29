import requests
import os



LITELLM_API_URL = os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000")
LITELLM_MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY", "sk-1234")



def create_virtual_key(user_id: str, plan: str, user_email: str) -> str:
    """
    Creates a virtual key in LiteLLM for a given user and plan.

    Args:
        user_id: The unique identifier for the user (from Open WebUI).
        plan: The subscription plan (e.g., "starter", "pro").

    Returns:
        The generated LiteLLM virtual key.
    """
    print(f"Creating LiteLLM key for user '{user_id}' with plan '{plan}'...")

    # Define budget and tier based on the plan
    budgets = {
        "starter": 10.0,  # $10 budget
        "pro": 50.0,      # $50 budget
        "ultra": 200.0    # $200 budget
    }
    budget = budgets.get(plan, 0.0)

    headers = {
        "Authorization": f"Bearer {LITELLM_MASTER_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = { "key_alias":user_id,
        "models": ["gpt-4o", "gemini-1.5-pro", "claude-3-haiku"],
        "max_budget": budget,
        "duration": "30d",
        "metadata": {
            "saas_user_id": user_id,
            "subscription_tier": plan,
            "email": user_email

        }
    }

    response = requests.post(f"{LITELLM_API_URL}/key/generate", json=payload, headers=headers)

    if response.status_code == 200:
        key_data = response.json()
        print("Successfully created LiteLLM key.")
        return key_data["key"]
    else:
        print(f"Error creating LiteLLM key: {response.text}")
        raise Exception("Failed to create LiteLLM virtual key.") 
    

if __name__ == "__main__":
    create_virtual_key("admin2@example.com", "pro", "admin2@example.com")