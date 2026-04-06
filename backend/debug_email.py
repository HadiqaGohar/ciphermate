from app.core.validation import validate_email_address

result = validate_email_address("user@example.com")
print(f"Is valid: {result.is_valid}")
print(f"Errors: {result.errors}")
print(f"Sanitized: {result.sanitized_value}")

for error in result.errors:
    print(f"Error: {error.code} - {error.message}")