"""
Test script for error handling and validation
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.validation import (
    validate_email_address,
    validate_message_content,
    validate_service_name,
    RequestValidator
)
from app.core.exceptions import (
    ValidationError,
    AuthenticationError,
    create_validation_error,
    create_missing_permission_error
)


def test_validation():
    """Test validation functions"""
    print("Testing validation functions...")
    
    # Test email validation
    print("\n1. Email validation:")
    valid_email = validate_email_address("user@example.com")
    print(f"Valid email: {valid_email.is_valid}")
    
    invalid_email = validate_email_address("invalid-email")
    print(f"Invalid email: {invalid_email.is_valid}, errors: {len(invalid_email.errors)}")
    
    # Test message validation
    print("\n2. Message validation:")
    valid_message = validate_message_content("Hello, this is a test message")
    print(f"Valid message: {valid_message.is_valid}")
    
    long_message = validate_message_content("x" * 6000)  # Too long
    print(f"Long message: {long_message.is_valid}, warnings: {len(long_message.warnings)}")
    
    # Test service name validation
    print("\n3. Service name validation:")
    valid_service = validate_service_name("google_calendar")
    print(f"Valid service: {valid_service.is_valid}")
    
    invalid_service = validate_service_name("Invalid-Service!")
    print(f"Invalid service: {invalid_service.is_valid}, errors: {len(invalid_service.errors)}")


def test_exceptions():
    """Test custom exceptions"""
    print("\nTesting custom exceptions...")
    
    # Test validation error
    print("\n1. Validation error:")
    try:
        raise create_validation_error("email", "Invalid email format", "not-an-email")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Field errors: {len(e.field_errors)}")
    
    # Test permission error
    print("\n2. Permission error:")
    try:
        raise create_missing_permission_error("google", ["calendar.read", "calendar.write"])
    except Exception as e:
        print(f"Permission error: {e.message}")
        print(f"User action: {e.user_action}")


async def test_request_validator():
    """Test request validator"""
    print("\nTesting request validator...")
    
    # Test chat request validation
    print("\n1. Chat request validation:")
    valid_chat = RequestValidator.validate_chat_request(
        "Create a calendar event for tomorrow",
        {"user_id": "123"}
    )
    print(f"Valid chat request: {valid_chat.is_valid}")
    
    invalid_chat = RequestValidator.validate_chat_request(
        "",  # Empty message
        None
    )
    print(f"Invalid chat request: {invalid_chat.is_valid}, errors: {len(invalid_chat.errors)}")
    
    # Test permission request validation
    print("\n2. Permission request validation:")
    valid_permission = RequestValidator.validate_permission_request(
        "google",
        ["calendar.read", "calendar.write"]
    )
    print(f"Valid permission request: {valid_permission.is_valid}")
    
    invalid_permission = RequestValidator.validate_permission_request(
        "Invalid Service!",
        ["invalid.scope!"]
    )
    print(f"Invalid permission request: {invalid_permission.is_valid}, errors: {len(invalid_permission.errors)}")


def main():
    """Run all tests"""
    print("=== CipherMate Error Handling Tests ===")
    
    test_validation()
    test_exceptions()
    
    # Run async tests
    asyncio.run(test_request_validator())
    
    print("\n=== Tests completed ===")


if __name__ == "__main__":
    main()