#!/usr/bin/env python3
"""
CORS Verification Script
Tests CORS configuration and preflight requests
"""

import sys
from fastapi.testclient import TestClient
from src.main import app

def test_cors_preflight():
    """Test CORS preflight OPTIONS request"""
    client = TestClient(app)
    
    test_cases = [
        {
            "name": "localhost:3000 (Vite dev)",
            "origin": "http://localhost:3000",
            "method": "POST",
            "headers": "content-type",
        },
        {
            "name": "127.0.0.1:3000",
            "origin": "http://127.0.0.1:3000",
            "method": "PUT",
            "headers": "content-type,authorization",
        },
        {
            "name": "localhost:5173 (Vite alternative)",
            "origin": "http://localhost:5173",
            "method": "DELETE",
            "headers": "content-type",
        },
        {
            "name": "Production domain",
            "origin": "https://itsm.example.com",
            "method": "POST",
            "headers": "content-type,authorization",
        },
    ]
    
    print("=" * 70)
    print("CORS PREFLIGHT REQUEST VERIFICATION")
    print("=" * 70)
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Origin: {test['origin']}")
        print(f"Method: {test['method']}")
        print(f"Headers: {test['headers']}")
        print("-" * 70)
        
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": test["origin"],
                "Access-Control-Request-Method": test["method"],
                "Access-Control-Request-Headers": test["headers"],
            },
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Allow-Origin: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
        print(f"Allow-Methods: {response.headers.get('access-control-allow-methods', 'NOT SET')}")
        print(f"Allow-Headers: {response.headers.get('access-control-allow-headers', 'NOT SET')}")
        print(f"Allow-Credentials: {response.headers.get('access-control-allow-credentials', 'NOT SET')}")
        print(f"Max-Age: {response.headers.get('access-control-max-age', 'NOT SET')}")
        
        # Check if CORS headers are properly set
        if response.status_code == 200:
            if response.headers.get('access-control-allow-origin'):
                print("✓ CORS properly configured")
            else:
                print("✗ CORS headers missing!")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")


def test_actual_request():
    """Test actual POST request with CORS headers"""
    client = TestClient(app)
    
    print("\n" + "=" * 70)
    print("ACTUAL REQUEST VERIFICATION")
    print("=" * 70)
    
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test", "password": "test"},
        headers={
            "Origin": "http://localhost:3000",
            "Content-Type": "application/json",
        },
    )
    
    print(f"\nPOST to /api/v1/auth/login")
    print(f"Origin: http://localhost:3000")
    print(f"Status Code: {response.status_code}")
    print(f"Allow-Origin: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
    
    if response.headers.get('access-control-allow-origin'):
        print("✓ CORS headers present in actual request")
    else:
        print("✗ CORS headers missing in actual request!")


def test_cors_configuration():
    """Print current CORS configuration"""
    from src.shared.infrastructure.config import settings
    
    print("\n" + "=" * 70)
    print("CURRENT CORS CONFIGURATION")
    print("=" * 70)
    print(f"Environment: {settings.environment}")
    print(f"Debug: {settings.debug}")
    print(f"\nAllowed Origins:")
    for origin in settings.allowed_origins:
        print(f"  - {origin}")
    print(f"\nAllow Methods: {', '.join(settings.cors_allow_methods)}")
    print(f"Allow Headers: {', '.join(settings.cors_allow_headers)}")
    print(f"Allow Credentials: {settings.cors_allow_credentials}")
    print(f"Max Age: {settings.cors_max_age} seconds")


if __name__ == "__main__":
    try:
        test_cors_configuration()
        test_cors_preflight()
        test_actual_request()
        print("\n" + "=" * 70)
        print("VERIFICATION COMPLETE")
        print("=" * 70)
    except Exception as e:
        print(f"Error during verification: {e}", file=sys.stderr)
        sys.exit(1)
