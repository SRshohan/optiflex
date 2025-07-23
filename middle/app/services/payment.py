import stripe
import os
from flask import Flask, request, redirect

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_51RnVkeRoIzbn9VW93cGgiTl3K3XuncMdCP2D3WkEEKc2qLGiAe4V2gBHKRSAOdTKgzBBZY3CTqFOwNDHqzUgmP7900Yv2TTFvH")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_e33ed9d908019d2b044b89c8fe14725e2a26c29fb9785b8138802333e3f840bc")
pro_product_id = "prod_Sixq5Bk1SPx82Q"

# Set your test success and cancel URLs
STRIPE_SUCCESS_URL = os.environ.get("STRIPE_SUCCESS_URL", "http://localhost:3000/success")
STRIPE_CANCEL_URL = os.environ.get("STRIPE_CANCEL_URL", "http://localhost:3000/cancel")

# --- Stripe Functions ---

def create_checkout_session(user_email: str):
    """Creates and returns a Stripe Checkout Session."""
    try:
        price_id = "price_1RnVuMRoIzbn9VW9UJ5PimsV"  # Replace with your actual Price ID

        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=request.host_url + 'success', # URL for successful payment
            cancel_url=request.host_url + 'cancel',   # URL for canceled payment
        )
        return checkout_session
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

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


# --- Flask Routes ---

@app.route('/create-checkout-session/<user_email>')
def start_checkout(user_email: str):
    """An endpoint to create a checkout session and redirect the user."""
    session = create_checkout_session(user_email)
    if session:
        # Redirect the user to the Stripe Checkout page
        return redirect(session.url, code=303)
    return "Error creating checkout session.", 500


@app.route('/stripe-webhook', methods=['POST'])
def handle_stripe_webhook():
    """Endpoint for receiving Stripe webhook events."""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        # Invalid payload or signature
        return 'Invalid request', 400

    # Handle the 'checkout.session.completed' event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get("customer_email")

        if customer_email:
            print(f"Checkout completed for: {customer_email}")
            # Here you would typically update your database to mark the user as subscribed
            # For now, we'll just verify it with the is_user_subscribed function
            if is_user_subscribed(customer_email):
                 print(f"Verified: {customer_email} now has an active subscription.")
            else:
                 print(f"Verification failed for {customer_email}.")

    return 'Success', 200

def is_user_subscribed(user_email: str) -> bool:
    # Find the customer by email
    customers = stripe.Customer.list(email=user_email).data
    if not customers:
        return False
    customer_id = customers[0].id

    # List active subscriptions for this customer
    subscriptions = stripe.Subscription.list(customer=customer_id, status="all").data
    for sub in subscriptions:
        if sub.status in ["active", "trialing"]:
            return True
    return False



# Simple routes for success and cancel pages
@app.route('/success')
def success():
    return "Payment Successful!"

@app.route('/cancel')
def cancel():
    return "Payment Canceled."

# --- Run the App ---

if __name__ == '__main__':
    # For development, you can run the app like this
    app.run(port=8000, debug=True)
