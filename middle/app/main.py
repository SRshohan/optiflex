# middle/app/main.py
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated
import stripe
import os

# Import your service modules
from .services import (
    litellm_service,
    openwebui_service,
    payment,
    payment_db
)

app = FastAPI()

# --- Endpoint to START the payment process ---
@app.post("/upgrade-plan")
async def upgrade_user_plan(
    user_email: str,
):
    
    try:
        # 1. Get user info from OpenWebUI using their token
        
        user_id = openwebui_service.get_user_id_by_email(user_email)

        # 2. Add/get user in our local database
        payment_db.add_user(email=user_email, stripe_customer_id=None) # You can add stripe_customer_id later

        # 3. Create a Stripe Checkout Session
        print(f"Creating Stripe checkout session for {user_email}...")
        checkout_session = payment.create_checkout_session(user_email=user_email, plan="pro")

        # 4. Return the checkout URL for the frontend to redirect to
        return {"checkout_url": checkout_session.url}

    except Exception as e:
        print(f"Error during upgrade plan process: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Endpoint for SUCCESSFUL payment redirect from Stripe ---
@app.get("/payment-success")
async def payment_success(session_id: str):
    try:
        # 1. Retrieve the session from Stripe to verify payment and get customer info
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        if checkout_session.payment_status == "paid":
            customer_email = checkout_session.customer_details.email
            stripe_subscription_id = checkout_session.subscription
            
            print(f"Payment successful for {customer_email}. Subscription ID: {stripe_subscription_id}")

            # 2. Get user from our local database
            user_data = payment_db.get_user_by_email(customer_email)
            if not user_data:
                raise Exception(f"User with email {customer_email} not found in our database.")
            
            user_id_in_db = user_data[0] # The user ID from our payment.db

            # 3. Create the LiteLLM Virtual Key for the user
            virtual_key_data = litellm_service.create_virtual_key(
                models=["gpt-4o", "claude-3-opus-20240229"],
                max_budget=20.00,
                duration="30d",
                metadata={"saas_user_email": customer_email, "plan": "Pro"}
            )
            virtual_key = virtual_key_data['key']
            
            # 4. Store payment and virtual key info in our database
            payment_db.add_payment(
                user_id=user_id_in_db,
                stripe_subscription_id=stripe_subscription_id,
                amount=checkout_session.amount_total / 100, # Amount is in cents
                currency=checkout_session.currency,
                status="active",
                plan="pro"
            )
            payment_db.add_virtual_key(
                user_id=user_id_in_db,
                key=virtual_key,
                models=virtual_key_data['models'],
                max_budget=virtual_key_data['max_budget'],
                duration=virtual_key_data.get('duration'),
                metadata=virtual_key_data.get('metadata')
            )

            # IMPORTANT: This success endpoint does NOT have the user's OpenWebUI token.
            # A more robust solution uses Stripe Webhooks to trigger this logic.
            # The webhook would then need an ADMIN token to update the user's settings.
            # For now, we return a success message. The final step is manual/omitted.
            print("User account upgraded in local DB. To reflect this in OpenWebUI, a webhook with an admin token is recommended.")

            return JSONResponse(
                status_code=200,
                content={"status": "success", "message": "Your payment was successful! Your account has been upgraded."}
            )
        else:
             return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Payment not successful."}
            )

    except Exception as e:
        print(f"Error in payment success callback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint for CANCELLED payment redirect from Stripe ---
@app.get("/payment-cancel")
async def payment_cancel():
    return JSONResponse(
        status_code=200,
        content={"status": "cancelled", "message": "Your payment was cancelled."}
    )
