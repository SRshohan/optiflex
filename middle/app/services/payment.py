import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_51RnVkeRoIzbn9VW93cGgiTl3K3XuncMdCP2D3WkEEKc2qLGiAe4V2gBHKRSAOdTKgzBBZY3CTqFOwNDHqzUgmP7900Yv2TTFvH")

pro_product_id = "prod_Sixq5Bk1SPx82Q"

# Set your test success and cancel URLs
STRIPE_SUCCESS_URL = os.environ.get("STRIPE_SUCCESS_URL", "http://localhost:3000/success")
STRIPE_CANCEL_URL = os.environ.get("STRIPE_CANCEL_URL", "http://localhost:3000/cancel")

def create_checkout_session(user_email: str, plan: str = "pro"):
    """
    Create a Stripe Checkout Session for the given user and plan.
    Returns the session object (including the URL for redirect).
    """
    # You can expand this logic for multiple plans/products
    price_id = "price_1RnVuMRoIzbn9VW9UJ5PimsV"  # For now, only 'pro' is supported

    session = stripe.checkout.Session.create(
        customer_email=user_email,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=STRIPE_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=STRIPE_CANCEL_URL,
        payment_method_types=["card"],
        billing_address_collection="auto",
    )
    return session

# Example usage for testing
if __name__ == "__main__":
    # Replace with a test email
    test_email = "testuser@example.com"
    session = create_checkout_session(test_email, "pro")
    print("Checkout session created!")
    print("Session ID:", session.id)
    print("Session URL:", session.url)