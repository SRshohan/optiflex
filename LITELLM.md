# OptiFlex Setup Guide: TigerVNC and Model Configuration

## Prerequisites
- A Raspberry Pi running OptiFlex
- Network access to the Raspberry Pi (IP: 192.168.1.214)
- Admin credentials for OptiFlex

## Step 1: Download and Install TigerVNC

1. **Download TigerVNC Viewer**
   - Go to the official TigerVNC website: https://sourceforge.net/projects/tigervnc/files/stable/
   - Download the appropriate version for your operating system (Windows, macOS, or Linux)
   - Install the downloaded application

2. **Launch TigerVNC Viewer**
   - Open TigerVNC Viewer from your applications menu
   - The main connection window will appear

## Step 2: Create New VNC Connection

1. **Enter Connection Details**
   - In the "VNC Server" field, enter: `192.168.1.214`
   - Leave the port as default 
   - Click "Connect" or "OK"

2. **Security Warning**
   - If a security warning window appears asking about the connection
   - Click "Yes" to proceed with the connection

## Step 3: Login to Raspberry Pi

1. **Authentication**
   - Username: `sr`
   - Password: `1999`
   - Click "OK" or press Enter

2. **Desktop Access**
   - You should now see the Raspberry Pi desktop
   - The VNC connection is established

## Step 4: Access OptiFlex Web Interface

1. **Open Web Browser**
   - In the Raspberry Pi desktop, open a web browser (Chromium, Firefox, etc.)
   - Navigate to: `http://localhost:4000`

2. **Login to OptiFlex**
   - Username: `admin`
   - Password: `sk-1234`
   - Click "Login"

## Step 5: Add Models to OptiFlex

1. **Navigate to Models Section**
   - From the main dashboard, click on "Models" in the navigation menu
   - Click "Add Models" or the "+" button

2. **Select Service Provider**
   - Choose your desired service provider from the dropdown menu
   - Options may include: OpenAI, Anthropic, Google, etc.

3. **Select Model**
   - Choose the specific model you want to add
   - If you want to add all available models from the provider, select "Wildcards"

4. **Configure API Key**
   - In the bottom section, enter your API key for the selected service provider
   - Make sure the API key is valid and has the necessary permissions

5. **Test Connection**
   - Click "Test Connect" to verify the API key and connection
   - Wait for the connection test to complete

6. **Add Model**
   - If the connection test is successful, click "Add Model"
   - The model should now appear in your OptiFlex admin panel

## Step 6: Configure Model Visibility (Make Models Public)

1. **Access Admin Panel**
   - Click on your profile icon/avatar in the top-right corner
   - Select "Admin Panel" from the dropdown menu, Then Select "settings"

2. **Navigate to Models Settings**
   - In the settings menu, click on "Models"
   - You'll see a list of all configured models

3. **Change Model Visibility**
   - Find the model you want to make public
   - Click on the edit icon (pen/pencil) next to the model
   - Change the "Visibility" setting from "Private" to "Public"
   - Save the changes

4. **Verify Public Access**
   - The model should now be visible to all users
   - Users can access the model without needing special permissions

## Troubleshooting

### Connection Issues
- Ensure the Raspberry Pi is powered on and connected to the network
- Verify the IP address (192.168.1.214) is correct
- Check if VNC service is running on the Raspberry Pi
- Ensure firewall settings allow VNC connections

### Model Configuration Issues
- Verify API keys are valid and have sufficient credits/permissions
- Check if the service provider is supported by OptiFlex
- Ensure network connectivity for API calls
- Review error messages in the OptiFlex logs

### Access Issues
- Confirm admin credentials are correct
- Check if the OptiFlex service is running on port 4000
- Verify user permissions and role assignments

## Security Notes

- Keep API keys secure and don't share them
- Regularly update passwords for admin accounts
- Monitor model usage and costs
- Consider implementing user authentication for production environments
- Backup configuration settings regularly

## Support

For additional support or troubleshooting:
- Check OptiFlex documentation
- Review system logs for error messages
- Contact system administrator for network-related issues


### /budget/new (Create a new budget Litellm)

bash```

{
  "budget_id": "pro",
  "max_budget": 20.0,
  "soft_budget": 0,
  "max_parallel_requests": 10,
  "tpm_limit": 100000,
  "rpm_limit": 100,
  "budget_duration": "30d",       
  "model_max_budget": {
    "gemini-2.5-flash": {
      "max_budget": 7.0,
      "budget_duration": "1d",
      "tpm_limit": 40000,
      "rpm_limit": 50
    },
    "grok-3": {
      "max_budget": 6.0,
      "budget_duration": "1d",
      "tpm_limit": 30000,
      "rpm_limit": 40
    },
    "gpt-4.1-mini": {
      "max_budget": 4.0,
      "budget_duration": "1d",
      "tpm_limit": 20000,
      "rpm_limit": 30
    }
  }
}
```