from fastapi import FastAPI, Request, HTTPException
import stripe
import os

app = FastAPI()

# This should be a secret environment variable
# e.g., STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """
    Listens for webhook events from Stripe.
    This is the entry point for your core business logic.
    """
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_successful_payment(session)

    return {"status": "success"}

def handle_successful_payment(session):
    """
    This is where the orchestration happens.
    1. Extract user info and plan details from the Stripe session.
    2. Call LiteLLM to create a virtual key with a budget.
    3. Call Open WebUI to add the new model with the key to the user's account.
    """
    print("Payment successful for session:", session["id"])
    
    # Example of extracting metadata you would set during checkout creation
    user_id = session.get("client_reference_id") # Open WebUI user ID
    plan = session.get("metadata", {}).get("plan") # e.g., "pro"
    
    if not user_id or not plan:
        print("Error: Missing user_id or plan in session metadata.")
        return

    print(f"Provisioning plan '{plan}' for user '{user_id}'...")

    # In a real implementation, you would call your services here:
    # litellm_key = litellm_service.create_virtual_key(user_id, plan)
    # openwebui_service.add_model_to_user(user_id, litellm_key, plan)

    print(f"Successfully provisioned plan for user '{user_id}'.")

@app.get("/health")
def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 