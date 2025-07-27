# Cloudflared Setup with Custom Domain from Hostinger

This guide walks you through setting up cloudflared with a custom domain transferred from Hostinger to Cloudflare.

## Prerequisites

- A domain registered with Hostinger
- Cloudflare account
- Cloudflared installed on your system
- Access to your local server/application

## Step 1: Transfer Domain from Hostinger to Cloudflare

### 1.1 Add Domain to Cloudflare

1. **Log into Cloudflare**
   - Go to [dash.cloudflare.com](https://dash.cloudflare.com)
   - Sign in to your account

2. **Add Domain to Cloudflare**
   - Click "Add a Site"
   - Enter your domain name
   - Click "Add Site"

3. **Select Plan**
   - Choose the appropriate plan (Free plan works for most use cases)
   - Click "Continue"

4. **Review DNS Records**
   - Cloudflare will scan for existing DNS records
   - Review and confirm the records
   - Click "Continue"

5. **Get Cloudflare Nameservers**
   - Cloudflare will provide you with two nameservers
   - Copy these nameserver addresses (e.g., `nina.ns.cloudflare.com` and `rick.ns.cloudflare.com`)

### 1.2 Update Nameservers in Hostinger

1. **Log into Hostinger Control Panel**
   - Go to [hpanel.hostinger.com](https://hpanel.hostinger.com)
   - Navigate to "Domains" section

2. **Update Nameservers**
   - Find your domain in the list
   - Click on "Manage" next to your domain
   - Go to "DNS" or "Nameservers" section
   - Replace the existing nameservers with Cloudflare's nameservers
   - Save the changes

3. **Automatic Transfer**
   - Once you update the nameservers, the domain automatically transfers to Cloudflare
   - No additional transfer process needed
   - DNS propagation can take 24-48 hours

## Step 2: Install and Configure Cloudflared

### 2.1 Install Cloudflared

**macOS (using Homebrew):**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux:**
```bash
# Download the latest version
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install on Ubuntu/Debian
sudo dpkg -i cloudflared-linux-amd64.deb

# Or install on CentOS/RHEL
sudo yum install cloudflared-linux-amd64.rpm
```

**Windows:**
- Download from [Cloudflare releases page](https://github.com/cloudflare/cloudflared/releases)
- Extract and add to PATH

### 2.2 Login to Cloudflared

```bash
cloudflared tunnel login
```

This command will:
1. Open your browser to Cloudflare's authentication page
2. Ask you to authorize the tunnel
3. Download a certificate file (usually `~/.cloudflared/cert.pem`)

## Step 3: Create Tunnel Configuration

### 3.1 Create Config File

Create a configuration file `~/.cloudflared/config.yml`:

```yaml
tunnel: your-tunnel-name
credentials-file: /path/to/your/created_file.json (Full path)

ingress:
  # Route all traffic to your local application
  - hostname: yourdomain.com
    service: http://localhost:3000  # Replace with your app's port
  - hostname: www.yourdomain.com
    service: http://localhost:3000
  # Catch-all rule for unmatched hostnames
  - service: http_status:404
```

### 3.2 Create Tunnel

```bash
cloudflared tunnel create your-tunnel-name
```

This will create a tunnel and provide you with a tunnel ID.

## Step 4: Configure DNS Records

### 4.1 Add CNAME Record

1. **In Cloudflare Dashboard:**
   - Go to your domain's DNS settings
   - Click "Add record"
   - Set Type to "CNAME"
   - Set Name to "@" (for root domain) or "www" (for subdomain)
   - Set Target to: `your-tunnel-id.trycloudflare.com`
   - Enable "Proxy status" (orange cloud)
   - Click "Save"

2. **Alternative: Use Cloudflared Command**
```bash
cloudflared tunnel route dns your-tunnel-name yourdomain.com
cloudflared tunnel route dns your-tunnel-name www.yourdomain.com
```

### 4.2 Add A Record (Optional)

If you prefer using A records instead of CNAME:

1. **Get Tunnel IP:**
```bash
cloudflared tunnel info your-tunnel-name
```

2. **Add A Record in Cloudflare:**
   - Type: A
   - Name: "@" (for root domain)
   - IPv4 address: [Tunnel IP from step 1]
   - Enable "Proxy status"
   - Click "Save"

## Step 5: Start the Tunnel

### 5.1 Run Tunnel

```bash
cloudflared tunnel run your-tunnel-name
```

### 5.2 Run as Service (Recommended)

**Install as System Service:**
```bash
cloudflared service install
```

**Start the Service:**
```bash
# On macOS/Linux
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# On Windows
sc start cloudflared
```

## Step 6: Verify Setup

### 6.1 Check Tunnel Status

```bash
cloudflared tunnel list
cloudflared tunnel info your-tunnel-name
```

### 6.2 Test Your Domain

1. Open your browser
2. Navigate to `https://yourdomain.com`
3. Verify your application loads correctly

### 6.3 Check SSL Certificate

- Your domain should automatically have SSL enabled
- Check for the padlock icon in your browser
- Verify certificate is issued by Cloudflare

## Step 7: Advanced Configuration

### 7.1 Custom Subdomains

Add additional subdomains to your config:

```yaml
ingress:
  - hostname: api.yourdomain.com
    service: http://localhost:8000
  - hostname: admin.yourdomain.com
    service: http://localhost:8080
  - hostname: yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
```

### 7.2 Load Balancing

For multiple backend services:

```yaml
ingress:
  - hostname: yourdomain.com
    service: http://localhost:3000
    originRequest:
      loadBalancer:
        pool: your-pool-name
```

### 7.3 Security Headers

Add security headers:

```yaml
ingress:
  - hostname: yourdomain.com
    service: http://localhost:3000
    originRequest:
      httpHostHeader: yourdomain.com
    headers:
      - name: X-Frame-Options
        value: DENY
      - name: X-Content-Type-Options
        value: nosniff
```

## Troubleshooting

### Common Issues

1. **Tunnel Not Connecting:**
   - Verify your local application is running
   - Check firewall settings
   - Ensure correct port in config

2. **DNS Not Resolving:**
   - Wait for DNS propagation (up to 48 hours)
   - Verify CNAME/A records are correct
   - Check proxy status is enabled

3. **SSL Issues:**
   - Ensure proxy is enabled (orange cloud)
   - Check SSL/TLS encryption mode in Cloudflare
   - Verify certificate is active

### Useful Commands

```bash
# Check tunnel logs
cloudflared tunnel info your-tunnel-name

# Test connection
cloudflared tunnel run your-tunnel-name --url http://localhost:3000

# Update tunnel
cloudflared tunnel update your-tunnel-name

# Delete tunnel
cloudflared tunnel delete your-tunnel-name
```

## Security Considerations

1. **Keep Certificates Secure:**
   - Store `cert.pem` in a secure location
   - Set appropriate file permissions
   - Don't share or commit to version control

2. **Monitor Access:**
   - Use Cloudflare Analytics to monitor traffic
   - Set up alerts for unusual activity
   - Regularly review access logs

3. **Update Regularly:**
   - Keep cloudflared updated
   - Monitor for security updates
   - Update configuration as needed

## Next Steps

- Set up monitoring and alerting
- Configure backup tunnels
- Implement rate limiting
- Set up custom error pages
- Configure caching rules

Your cloudflared tunnel with custom domain is now ready to use!
