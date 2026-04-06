#!/usr/bin/env python3
"""
Test script to verify Auth0 token structure and kid header
"""

import base64
import json
import sys
from jose import jwt

def decode_token_header(token):
    """Decode JWT token header without verification"""
    try:
        # Split token into parts
        parts = token.split('.')
        if len(parts) != 3:
            return None, "Invalid JWT format"
        
        # Decode header
        header_b64 = parts[0]
        # Add padding if needed
        header_b64 += '=' * (4 - len(header_b64) % 4)
        header_bytes = base64.urlsafe_b64decode(header_b64)
        header = json.loads(header_bytes)
        
        return header, None
    except Exception as e:
        return None, str(e)

def main():
    print("🔍 Auth0 Token Structure Tester")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print("Please provide a token to test:")
        print("Usage: python test_token_structure.py <your_access_token>")
        print("\nTo get your token:")
        print("1. Login to your app")
        print("2. Open browser DevTools (F12)")
        print("3. Go to Application/Storage → Cookies")
        print("4. Find 'appSession' cookie")
        print("5. Copy the accessToken value from the JSON")
        return
    
    print(f"Token (first 50 chars): {token[:50]}...")
    print()
    
    # Test with jose library (same as backend)
    try:
        header = jwt.get_unverified_header(token)
        print("✅ Token header decoded successfully!")
        print(f"Header: {json.dumps(header, indent=2)}")
        
        if 'kid' in header:
            print(f"✅ 'kid' found: {header['kid']}")
        else:
            print("❌ 'kid' missing from header!")
            print("This is why you're getting 'Token missing kid in header' error")
        
        if 'alg' in header:
            print(f"✅ Algorithm: {header['alg']}")
        
    except Exception as e:
        print(f"❌ Error decoding token header: {e}")
    
    print()
    
    # Manual decode test
    header, error = decode_token_header(token)
    if error:
        print(f"❌ Manual decode error: {error}")
    else:
        print("✅ Manual decode successful!")
        print("Header structure:")
        for key, value in header.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()