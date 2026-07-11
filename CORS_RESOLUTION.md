# CORS Issue Resolution Guide

## Overview
This guide documents the CORS (Cross-Origin Resource Sharing) configuration and resolution steps for the ITSM microservices project.

## What Was Fixed

### 1. **Dynamic CORS Configuration**
   - **File**: `itsm-microservices/src/shared/infrastructure/config.py`
   - **Change**: Moved CORS origins from hardcoded list to environment-configurable settings
   - **Benefit**: Allows different CORS settings per environment (development, staging, production)

### 2. **Backend CORS Setup**
   - **File**: `itsm-microservices/src/main.py`
   - **Change**: Updated to use dynamic settings instead of hardcoded origins
   - **Configuration**:
     - `allow_origins`: Dynamically loaded from `CORS_ORIGINS` environment variable
     - `allow_credentials`: Set to `true` for authentication headers
     - `allow_methods`: GET, POST, PUT, PATCH, DELETE, OPTIONS
     - `allow_headers`: Accepts all headers (wildcard)
     - `max_age`: 3600 seconds for preflight caching

### 3. **Frontend API Client Enhancement**
   - **File**: `frontend/src/services/api.ts`
   - **Change**: Smart URL selection based on environment
   - **Logic**:
     - **Development**: Uses Vite proxy (`/api/v1`) to avoid direct CORS
     - **Production/Staging**: Uses full API URLs from environment variables
   - **Benefit**: Eliminates CORS issues in development while maintaining production compatibility

### 4. **Vite Proxy Configuration**
   - **File**: `frontend/vite.config.ts`
   - **Change**: Added error logging to proxy configuration
   - **Proxy Rule**: `/api` → `http://localhost:8000`
   - **Benefit**: In development, frontend calls go through proxy, no CORS needed

## Environment Configuration

### Development (`.env` files)

**Backend** (`itsm-microservices/.env`):
```
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost,http://127.0.0.1
CORS_ALLOW_CREDENTIALS=true
CORS_MAX_AGE=3600
```

**Frontend** (`frontend/.env`):
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_ENVIRONMENT=development
```

### Staging

**Backend** (`itsm-microservices/.env.staging`):
```
CORS_ORIGINS=https://staging-api.itsm.example.com,https://itsm-staging.example.com,http://localhost:3000,http://localhost:5173
```

**Frontend** (`frontend/.env.staging`):
```
VITE_API_BASE_URL=https://staging-api.itsm.example.com/api/v1
VITE_ENVIRONMENT=staging
```

### Production

**Backend** (`itsm-microservices/.env.production`):
```
CORS_ORIGINS=https://itsm.example.com,https://www.itsm.example.com,https://api.itsm.example.com
```

**Frontend** (`frontend/.env.production`):
```
VITE_API_BASE_URL=https://api.itsm.example.com/api/v1
VITE_ENVIRONMENT=production
```

## How to Test CORS

### 1. Run the Verification Script
```bash
cd itsm-microservices
python verify_cors_complete.py
```

This script will:
- Display current CORS configuration
- Test preflight OPTIONS requests from various origins
- Test actual POST requests
- Verify CORS headers are present

### 2. Manual Testing with curl

**Preflight Request:**
```bash
curl -X OPTIONS http://localhost:8000/api/v1/auth/login \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

Expected response should include:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: *
Access-Control-Allow-Credentials: true
```

### 3. Browser Console Testing
Open browser dev tools console and check for CORS errors.

## Common CORS Issues and Solutions

### Issue 1: "No 'Access-Control-Allow-Origin' header"
**Cause**: Origin not in allowed list
**Solution**: 
- Check `CORS_ORIGINS` environment variable
- Add your origin to the list
- Restart the backend service

### Issue 2: "Method not allowed in CORS policy"
**Cause**: HTTP method not in `allow_methods`
**Solution**:
- Backend already includes all standard methods
- Verify the API endpoint exists

### Issue 3: "Request header not allowed"
**Cause**: Header not in `allow_headers`
**Solution**:
- Backend is configured to allow all headers (`*`)
- If specific headers fail, check they're in the request

### Issue 4: CORS works in dev but not in production
**Cause**: Different origin in production
**Solution**:
- Update `CORS_ORIGINS` in `.env.production`
- Deploy the updated configuration
- Clear CDN cache if using one

## Docker Deployment CORS Notes

When deploying with Docker, ensure:

1. **Environment variables are passed**:
```yaml
environment:
  - CORS_ORIGINS=https://itsm.example.com,https://www.itsm.example.com
  - CORS_ALLOW_CREDENTIALS=true
```

2. **Network communication**: Frontend and backend must be reachable from each other

3. **SSL/TLS**: Production should use HTTPS origins

4. **CDN considerations**: If using CDN, add CDN domain to allowed origins

## Quick Checklist for Debugging

- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 3000 (dev) or configured API URL
- [ ] CORS_ORIGINS environment variable is set correctly
- [ ] No typos in origin URLs (exact match required)
- [ ] Using http for local, https for production
- [ ] Preflight requests return 200 status
- [ ] CORS headers are present in responses
- [ ] Browser console shows no CORS errors

## Files Modified

1. `itsm-microservices/src/shared/infrastructure/config.py` - Added CORS settings
2. `itsm-microservices/src/main.py` - Updated to use dynamic CORS config
3. `frontend/src/services/api.ts` - Smart API URL selection
4. `frontend/vite.config.ts` - Enhanced proxy configuration
5. `itsm-microservices/.env` - Development CORS config
6. `frontend/.env` - Development frontend config
7. Created `.env.staging` and `.env.production` for environment-specific configs
8. Created `verify_cors_complete.py` - Comprehensive CORS testing script

## Next Steps

1. Test CORS with verification script
2. Deploy to staging environment
3. Test with production domains before final deployment
4. Monitor browser console for any CORS-related errors in production
