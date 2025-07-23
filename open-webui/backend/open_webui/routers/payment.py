import re
import uuid
import time
import datetime
import logging
import stripe
from aiohttp import ClientSession
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from firebase_admin import auth as firebase_auth, credentials, initialize_app
import os
import requests


# from open_webui.models.auths import (
#     AddUserForm,
#     ApiKey,
#     Auths,
#     Token,
#     LdapForm,
#     SigninForm,
#     SigninResponse,
#     SignupForm,
#     UpdatePasswordForm,
#     UpdateProfileForm,
#     UserResponse,
# )
from open_webui.models.users import Users, UserSettings
from open_webui.utils.auth import get_verified_user
from open_webui.utils.access_control import has_permission
from open_webui.constants import ERROR_MESSAGES

router = FastAPI()

LITELLM_API_URL = os.environ.get("LITELLM_API_URL", "http://127.0.0.1:4000")
LITELLM_MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY", "sk-1234")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_51RnVkeRoIzbn9VW93cGgiTl3K3XuncMdCP2D3WkEEKc2qLGiAe4V2gBHKRSAOdTKgzBBZY3CTqFOwNDHqzUgmP7900Yv2TTFvH")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_e33ed9d908019d2b044b89c8fe14725e2a26c29fb9785b8138802333e3f840bc")


def create_virtual_key(user_id: str, plan: str = "pro", user_email: str = "admin@example.com") -> str:
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
        "custom": 200.0    # $200 budget
    }
    budget = budgets.get(plan, 0.0)

    headers = {
        "Authorization": f"Bearer {LITELLM_MASTER_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = { "key_alias":user_id,
        "models": ["gpt-4o", "gemini-1.5-pro", "claude-3-haiku"],
        "max_budget": budget.get(plan, 0.0),
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

@router.post("/user/plan/update", response_model=UserSettings, name="update_user_settings_by_session_user")
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
        }
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

@router.post("/checkout/stripe-webhook")
async def create_checkout_session(user_email: str, request: Request, user=Depends(get_verified_user)):
    base_url = os.environ.get("BASE_URL", "http://localhost:5000")

    try:
        price_id = "price_1RnVuMRoIzbn9VW9UJ5PimsV"
        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=base_url + 'update_user_settings_by_session_user', # URL for successful payment
            cancel_url=base_url + '/checkout/cancel',   # URL for canceled payment
        )
        return checkout_session
    
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None
    
@router.get("/checkout/success", name="success")
async def success(request: Request):

    return {"message": "Payment Successful!"}

@router.get("/checkout/cancel", name="cancel")
async def cancel(request: Request):
    return {"message": "Payment Canceled."}