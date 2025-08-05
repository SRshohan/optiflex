import re
import uuid
import time
import datetime
import logging
import stripe
from aiohttp import ClientSession
from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from firebase_admin import auth as firebase_auth, credentials, initialize_app
import os
import requests
from pydantic import BaseModel

from open_webui.models.users import Users, UserSettings
from open_webui.utils.auth import get_verified_user
from open_webui.utils.access_control import has_permission
from open_webui.constants import ERROR_MESSAGES

router = APIRouter()

LITELLM_API_URL = os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000")
LITELLM_MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY", "sk-1234")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_51RnVkeRoIzbn9VW93cGgiTl3K3XuncMdCP2D3WkEEKc2qLGiAe4V2gBHKRSAOdTKgzBBZY3CTqFOwNDHqzUgmP7900Yv2TTFvH")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_e33ed9d908019d2b044b89c8fe14725e2a26c29fb9785b8138802333e3f840bc")
PLAN_TEST = os.environ.get("PLAN_TEST", "pro")

class EmailRequest(BaseModel):
    user_email: str

def check_user_in_litellm(email):
    """
    Check if user exists in LiteLLM and get their subscription status
    """
    try:
        # LiteLLM API endpoint to get user list
        url = f"{LITELLM_API_URL}/user/list"  
        
        headers = {
            "Authorization": f"Bearer {LITELLM_MASTER_KEY}", 
            "Content-Type": "application/json"
        }
        
        # Use the correct API parameter for email filtering
        params = {"user_email": email}
        response = requests.get(url, params=params, headers=headers)
        
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

# Create a user in LiteLLM
def create_user_in_litellm(user_email: str, headers: dict):
    """
    Creates a user in LiteLLM for a given user email.
    """
    payload = {
        "user_email": user_email,
        "user_role": "internal_user",
        "max_parallel_requests": 5,
        "user_id": user_email
    }

    print(f"Creating user with payload: {payload}")
    response = requests.post(f"{LITELLM_API_URL}/user/new", json=payload, headers=headers)
    print(f"User creation response status: {response.status_code}")
    print(f"User creation response: {response.text}")

    if response.status_code == 200:
        print(f"Successfully created LiteLLM user for {user_email}.")
        user_id = response.json()["user_id"]
        print(f"LiteLLM user ID: {user_id}")
        return user_id
    else:
        print(f"Error creating LiteLLM user for {user_email}: {response.text}")
        return None

# Create a virtual key in LiteLLM
def create_virtual_key(user_id: str, plan: str = "free", user_email: str = "admin@example.com") -> str:
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
        "starter": {"budget": 10.0, "duration": "30d", "models": ["gemini/gemini-2.5-flash", "xai/grok-3-mini", "gpt-4.1-mini"]},  # $10 budget
        "pro": {"budget": 20.0, "duration": "30d", "models": ["gemini/gemini-2.5-flash", "xai/grok-3", "gpt-4.1-mini", "xai/grok-3-mini", "xai/grok-4-0709", "claude-4-sonnet-20250514", "claude-4-opus-20250514", "gemini/gemini-2.5-pro", "openai/gpt-4o"]},      # $50 budget
        "superultra": {"budget": 200.0, "duration": "30d", "models": ["gemini/gemini-2.5-flash", "xai/grok-4", "gpt-4.1-mini", "claude-4-sonnet-20250514", "claude-4-opus-20250514", "	gemini/gemini-2.0-pro-exp-02-05"]}    # $200 budget
    }

    headers = {
        "Authorization": f"Bearer {LITELLM_MASTER_KEY}",
        "Content-Type": "application/json"
    }

    # Check if user exists in LiteLLM
    user_data = check_user_in_litellm(user_email)

    print(f"User data: {user_data}")
    if user_data["exists"]:
        litellm_user_id = user_data["user_data"]["user_id"]
    else:
        # Create user in LiteLLM
        litellm_user_id = create_user_in_litellm(user_email, headers)
        if not litellm_user_id:
            raise Exception("Failed to create or retrieve user in LiteLLM.")

    print(f"Retrieved LiteLLM user ID: {litellm_user_id}")
    
    payload = { 
        "user_id": litellm_user_id, # Use the ID from LiteLLM for the key owner
        "budget_id": PLAN_TEST,
        "models": budgets.get(plan, {}).get("models", []),
        # "max_budget": budgets.get(plan, {}).get("budget", 0.0),
        "duration": budgets.get(plan, {}).get("duration", "30d"),
        "metadata": {
            "saas_user_id": user_id, # Use the original Open WebUI user ID for tracking
            "subscription_tier": plan,
            "email": user_email
        }
    }

    print(f"Creating key with payload: {payload}")
    response = requests.post(f"{LITELLM_API_URL}/key/generate", json=payload, headers=headers)

    if response.status_code == 200:
        key_data = response.json()
        print("Successfully created LiteLLM key.")
        return key_data["key"]
    else:
        print(f"Error creating LiteLLM key: {response.text}")
        print(f"Response status: {response.status_code}")
        raise Exception("Failed to create LiteLLM virtual key.") 

# --- Stripe Functions ---

# def create_checkout_session(user_email: str):
#     """Creates and returns a Stripe Checkout Session."""
#     try:
#         price_id = "price_1RnVuMRoIzbn9VW9UJ5PimsV"  # Replace with your actual Price ID

#         checkout_session = stripe.checkout.Session.create(
#             customer_email=user_email,
#             line_items=[{"price": price_id, "quantity": 1}],
#             mode="subscription",
#             success_url=request.host_url + 'success', # URL for successful payment
#             cancel_url=request.host_url + 'cancel',   # URL for canceled payment
#         )
#         return checkout_session
#     except Exception as e:
#         print(f"Error creating checkout session: {e}")
#         return None


# Update user settings by session user
@router.post("/user/plan/update", name="update_user_settings_by_session_user")
async def update_user_settings_by_session_user(
    request: Request, user=Depends(get_verified_user)
):  
   
    form_data = {
        "ui": {
            "directConnections": {
            "OPENAI_API_BASE_URLS": [
                os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000")
            ],
            "OPENAI_API_KEYS": [
                create_virtual_key(user.id, "pro", user.email)
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
        },
        "additionalProp1":{}
    }
    updated_user_settings = form_data
    if (
        user.role != "admin"
        and "toolServers" in updated_user_settings.get("ui").keys()
        and not has_permission(
            user.id,
            "features.direct_tool_servers",
            request.app.state.config.USER_PERMISSIONS,
        )
    ):
        # If the user is not an admin and does not have permission to use tool servers, remove the key
        updated_user_settings["ui"].pop("toolServers", None)

    user = Users.update_user_settings_by_id(user.id, updated_user_settings)
    if user:
        return user.settings
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.USER_NOT_FOUND,
        )

# Check if a user has an active subscription
def is_user_subscribed(user_email: str) -> bool:
    """Checks if a user has an active subscription."""
    try:
        # Find the customer by email
        customers = stripe.Customer.list(email=user_email, limit=1).data
        if not customers:
            print(f"No customer found for email: {user_email}")
            return False
        
        customer_id = customers[0].id

        # Find active subscriptions for that customer
        subscriptions = stripe.Subscription.list(customer=customer_id, status="active", limit=1).data
        
        # Return True if any active subscription is found
        return len(subscriptions) > 0
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False


# Create a checkout session
@router.post("/checkout/stripe-webhook")
async def create_checkout_session(user_email: EmailRequest, user=Depends(get_verified_user)):
    # Use WEBUI_URL for the frontend, which is where Stripe should redirect the user.
    # The default value points to the typical SvelteKit dev server address.
    webui_url = os.environ.get("WEBUI_URL", "http://localhost:5173")
    price_id = os.environ.get("STRIPE_PRICE_ID", "price_1RnVuMRoIzbn9VW9UJ5PimsV")

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email.user_email,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            # This now correctly points to your frontend success page
            success_url=f"{webui_url}/success",
            cancel_url=f"{webui_url}/cancel",
        )
        print(f"Checkout session created. Success URL: {checkout_session.success_url}")
        return {"checkout_url": checkout_session.url}
    
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None
    
@router.get("/checkout/success", name="success")
async def success(request: Request):

    return {"message": "Payment Successful!"}

@router.get("/checkout/cancel", name="cancel")
async def cancel(request: Request):
    return {"message": "Payment Canceled."}