# Environment Variables Configuration

## Vercel Environment Variables

Set these in your Vercel dashboard (Settings → Environment Variables):

### Production Environment
- **Variable**: `VITE_BACKEND_URL`
- **Value**: `https://openwebui-backend-953676742197.us-central1.run.app`
- **Environments**: Production ✅

### Preview Environment  
- **Variable**: `VITE_BACKEND_URL`
- **Value**: `https://openwebui-backend-953676742197.us-central1.run.app`
- **Environments**: Preview ✅

### Development Environment
- **Variable**: `VITE_BACKEND_URL`
- **Value**: `https://openwebui-backend-953676742197.us-central1.run.app`
- **Environments**: Development ✅

## Local Development

Create `.env.local` file in your project root:
```
VITE_BACKEND_URL=https://openwebui-backend-953676742197.us-central1.run.app
```

## Fallback Strategy

The frontend will use URLs in this priority order:
1. **Environment Variable** (`VITE_BACKEND_URL`) - Highest priority
2. **Development Mode** (`localhost:8080`) - For local dev
3. **Production Fallback** (Cloud Run URL) - Safe default

## Testing Different Backends

To test with different backends, change the `VITE_BACKEND_URL` value:
- **Test Backend**: `https://test-backend.example.com`
- **Staging Backend**: `https://staging-backend.example.com`
- **Production Backend**: `https://openwebui-backend-953676742197.us-central1.run.app`
