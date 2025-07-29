# Setting Up Optiflex Backend on Windows (Python 3.11)

## 1. Install Python 3.11
- Download Python 3.11 for Windows from the [official Python website](https://www.python.org/downloads/release/python-3110/).
- During installation, **check the box** that says "Add Python to PATH".

## 2. Open Command Prompt and Navigate to Backend
```sh
cd open-webui\backend
```

## 3. Check Python Version
Make sure you are using Python 3.11.x:
```sh
python --version
```
You should see output like:
```
Python 3.11.x
```
If not, ensure Python 3.11 is installed and available in your PATH.

## 4. Create and Activate a Virtual Environment
```sh
python -m venv venv
venv\Scripts\activate
```
If you see a security warning, you may need to set the execution policy (run as Administrator):
```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 5. Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Run the Backend Server
```sh
python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload
```
Or, you can use the provided batch file for Windows:
```sh
start_windows.bat
```

---
**You can now access the backend at** [http://localhost:8080](http://localhost:8080)


### 7. Update 

# Open WebUI: Direct Connections API Usage Guide

## Overview
This section explains how to configure, inspect, and update **Direct Connections** for Open WebUI (Optiflex) via the API. This is useful for users and developers who want to automate or debug the process of connecting to custom OpenAI-compatible endpoints.

---

## What Are Direct Connections?
- **Direct Connections** allow each user to add their own OpenAI-compatible API endpoints (e.g., LiteLLM, custom proxy, etc.) without admin access.
- These connections are stored in the user's settings and are not global.

---

## API Endpoint
- **URL:** `/api/v1/users/user/settings/update`
- **Method:** `POST`
- **Authentication:** Bearer token (user must be logged in)

---

## Example Payload
Below is a real example of the JSON payload sent by the frontend when saving direct connections:

```json
{
  "ui": {
    "directConnections": {
      "OPENAI_API_BASE_URLS": [
        "http://localhost:4000",
        "http://localhost:4000"
      ],
      "OPENAI_API_KEYS": [
        "sk-tn3WZUts7YHXB1jIJ_ZDvw",
        "sk-_XWMPOuQWWFTrvQmD1_w1g"
      ],
      "OPENAI_API_CONFIGS": {
        "0": {
          "enable": true,
          "tags": [],
          "prefix_id": "",
          "model_ids": [],
          "connection_type": "external"
        },
        "1": {
          "enable": true,
          "tags": [],
          "prefix_id": "",
          "model_ids": [],
          "connection_type": "external"
        }
      }
    },
    "webSearch": null
  }
}
```

---

## How to Inspect the Payload (Step-by-Step)
1. **Open the WebUI in your browser.**
2. **Open Developer Tools** (F12 or right-click → Inspect).
3. Go to the **Network** tab.
4. Filter for `/api/v1/users/user/settings/update`.
5. Add or edit a Direct Connection in the UI and click **Save**.
6. Click the request in the Network tab and view the **Payload** or **Request** section.
7. Copy the JSON for your own use or automation.

---

## Notes
- The `OPENAI_API_BASE_URLS`, `OPENAI_API_KEYS`, and `OPENAI_API_CONFIGS` arrays/objects must be kept in sync by index.
- The backend stores this data in the user's settings JSON field.
- This endpoint is **per-user**; each user can have their own set of direct connections.
- The `webSearch` key may be present or null, depending on your UI settings.

---

## Troubleshooting
- If you receive a `422 Unprocessable Entity` error, ensure your JSON is valid and matches the structure above.
- Do not include extra or misspelled keys.
- Always use double quotes for property names and string values in JSON.

---

## References
- Frontend: `src/lib/components/chat/Settings/Connections.svelte`, `SettingsModal.svelte`
- Backend: `open_webui/routers/users.py`, `models/users.py`

---

For further questions, inspect the browser network tab as described above, or consult the codebase for the latest structure. 


# LiteLLM: Virtual Keys Configuration Guide

## Overview
This section explains how to configure **virtual_keys** for LiteLLM, which is useful for managing API access, budgets, and user metadata in SaaS or multi-tenant environments.

---

## What Are Virtual Keys?
- **Virtual keys** allow you to create API keys that map to specific models, budgets, and user metadata.
- Useful for SaaS scenarios where you want to control access, spending, and features per user or subscription tier.

---

## Example Virtual Key Configuration
Below is an example configuration for generating a virtual key in LiteLLM:

```json
{
  "models": ["gpt-4o", "gemini-1.5-pro", "claude-3-haiku"],
  "max_budget": 10.00,
  "duration": "30d",
  "metadata": {
    "saas_user_id": "user-12345",
    "subscription_tier": "Pro"
  }
}
```

### **Field Descriptions**
- `models`: List of model names this key can access.
- `max_budget`: Maximum spend allowed for this key (in dollars or your currency).
- `duration`: Validity period for the key (e.g., `30d` for 30 days).
- `metadata`: Custom metadata for tracking user, subscription, or other info.

---

## How to Use
1. Add this configuration to your LiteLLM `config.yaml` or use the LiteLLM admin API/CLI to generate a new virtual key.
2. Distribute the generated virtual key to your user or application.
3. LiteLLM will enforce the model access, budget, and duration automatically.

---

## SaaS Use Case Example
- When a user upgrades to a "Pro" tier, generate a virtual key with higher `max_budget` and more models.
- Store the `saas_user_id` and `subscription_tier` in the `metadata` for tracking and analytics.

---

## References
- [LiteLLM Documentation](https://docs.litellm.ai/docs/virtual_keys)
- Example config: `config.yaml` in your LiteLLM deployment

---

For more advanced usage, see the LiteLLM docs or your SaaS backend logic for dynamic key generation. 


# Stripe Webhook Setup Guide

## Overview
This section explains how to set up and test webhooks for Stripe, which are crucial for handling payment events and user subscriptions.

---

### **The Core Problem: Stripe Can't See Your `localhost`**

First, let's establish the fundamental problem.
*   When a payment happens, Stripe's servers need to tell your backend application about it. They do this by sending an HTTP request called a **webhook**.
*   Your backend, running with `sh dev.sh`, is listening on an address like `http://localhost:8080`.
*   The `localhost` address is only visible *to your computer*. Stripe's servers on the internet have no way to find or connect to it. It's like trying to mail a letter to someone by only writing "my house" as the address.

So, the challenge is: **How do we create a secure, temporary bridge from the public internet to our local backend server?**

### **The Solution: The Stripe CLI and Webhook Forwarding**

The official and standard way to solve this is by using the **Stripe CLI (Command Line Interface)**.

The Stripe CLI is a powerful developer tool that does two key things for you:

1.  **It provides a secure tunnel:** It has a command that connects to Stripe's servers, creates a temporary public URL, and forwards any webhook traffic sent to that URL directly to your `localhost`.
2.  **It lets you simulate events:** You can use it to trigger fake events (like a successful payment) without having to use a real credit card, which makes testing incredibly fast.

Here is my suggestion for how to set this up, step-by-step.

---

### **Suggested Step-by-Step Guide**

#### **Step 1: Install the Stripe CLI**

First, you need to install the tool itself. Open your terminal on your local machine.

*   **If you use Homebrew on macOS (most common):**
    ```bash
    brew install stripe/stripe-cli/stripe
    ```
*   **If you're on Linux or Windows:** Follow the official, easy-to-use instructions on the [Stripe CLI website](https://stripe.com/docs/stripe-cli).

#### **Step 2: Authenticate the CLI with Your Stripe Account**

Next, you need to link the CLI to your Stripe account. This is a one-time setup.

1.  Run the following command in your terminal:
    ```bash
    stripe login
    ```
2.  This command will print a URL. Copy and paste it into your browser.
3.  Your browser will ask you to log in to Stripe and grant access to the CLI. Click "Allow".
4.  You'll get a confirmation, and your terminal will now be connected to your Stripe account.

#### **Step 3: Start Your Local Backend Server**

This is the step you already know. In a separate terminal window:
1.  Navigate to the `open-webui/backend` directory.
2.  Run `sh dev.sh` to start the Python server.
3.  Make a note of the port it's running on (it's almost certainly `8080`).

#### **Step 4: Start the Stripe Webhook Tunnel**

This is the main event. In the terminal where you have the Stripe CLI installed:

1.  Run the following command:
    ```bash
    stripe listen --forward-to localhost:8080/api/v1/webhooks/stripe
    ```

Let's break down that command:
*   `stripe listen`: This tells the CLI to start listening for webhook events.
*   `--forward-to`: This tells the CLI where to send the events it receives.
*   `localhost:8080`: This is the address of your local backend server.
*   `/api/v1/webhooks/stripe`: This is the specific API endpoint within your backend code that is designed to process incoming webhooks from Stripe.

When you run this, the Stripe CLI will output a webhook signing secret that looks like `whsec_...`. Your application needs this key to verify that the webhooks are actually from Stripe. You'll likely need to set this as an environment variable (e.g., `STRIPE_WEBHOOK_SECRET`) for your backend to use.

#### **Step 5: Test by Triggering a Fake Event**

Now you have a tunnel running. How do you test it?

Open a **third** terminal window. Use the Stripe CLI to trigger a test event. For example, to simulate a successful payment:

```bash
stripe trigger payment_intent.succeeded
```

**What will happen:**
1.  The `stripe trigger` command tells Stripe's servers to create a fake "payment succeeded" event.
2.  Stripe's servers will send a webhook for this event to your `stripe listen` process.
3.  Your `stripe listen` process will receive the webhook and instantly forward it to `http://localhost:8080/api/v1/webhooks/stripe`.
4.  You should see activity in the terminal window where your `dev.sh` server is running, as it processes the request.

This setup allows you to fully test your payment integration locally without deploying anything or using real credit card data. It's the standard, professional workflow for Stripe development. 