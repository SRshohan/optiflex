import requests

LITELLM_API_URL = "http://localhost:4000"
LITELLM_MASTER_KEY = "sk-1234"


def check_user_in_litellm(email):
    """
    Check if user exists in LiteLLM and get their subscription status
    """
    try:
        # LiteLLM API endpoint to get user info
        url = f"{LITELLM_API_URL}/user/info"  
        
        headers = {
            "Authorization": f"Bearer {LITELLM_MASTER_KEY}", 
            "Content-Type": "application/json"
        }
        # Use the correct API parameter for email filtering
        payload = {"user_id": email}
        response = requests.get(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            
            # Check if any users were returned
            users = user_data.get("users", [])
            if users:
                # Return the first user (API already filtered by email)
                return {
                    "exists": True,
                    "user_data": users[0]
                }
            else:
                return {
                    "exists": False,
                    "user_data": None
                }
        else:
            return {
                "exists": False,
                "error": f"API error: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "exists": False,
            "error": f"Connection error: {str(e)}"
        }

print(check_user_in_litellm("test@test.com"))