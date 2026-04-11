#!/usr/bin/env python3
"""
Test Slack channel validation fix
"""

import sys
sys.path.append('./backend')

from app.core.validation import validate_against_injection_attacks

def test_slack_channels():
    """Test that Slack channel names are not blocked"""
    
    test_cases = [
        "#general",
        "#random", 
        "#dev-team",
        "#project_updates",
        "#announcements"
    ]
    
    print("🧪 Testing Slack Channel Validation")
    print("=" * 40)
    
    for channel in test_cases:
        result = validate_against_injection_attacks(channel)
        status = "✅ PASS" if result.is_valid else "❌ FAIL"
        print(f"{status} Channel: {channel}")
        if not result.is_valid:
            print(f"     Errors: {[e.message for e in result.errors]}")
    
    print("\n🔍 Testing potential SQL injection (should be blocked):")
    malicious_cases = [
        "'; DROP TABLE users; --",
        "admin'--",
        "1' OR '1'='1"
    ]
    
    for malicious in malicious_cases:
        result = validate_against_injection_attacks(malicious)
        status = "✅ BLOCKED" if not result.is_valid else "❌ NOT BLOCKED"
        print(f"{status} Input: {malicious}")

if __name__ == "__main__":
    test_slack_channels()