#!/usr/bin/env python3
"""
Simple security test to verify core functionality
"""

from app.core.validation import (
    validate_against_injection_attacks,
    validate_email_address,
    validate_url,
    validate_service_name
)
from app.core.security_monitor import security_monitor, security_metrics
from app.core.config import settings

def test_sql_injection_detection():
    """Test SQL injection detection"""
    print("Testing SQL injection detection...")
    
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "1' OR '1'='1",
        "admin'--",
        "' UNION SELECT * FROM users --"
    ]
    
    blocked_count = 0
    for payload in malicious_inputs:
        result = validate_against_injection_attacks(payload)
        if not result.is_valid:
            blocked_count += 1
            print(f"  ✓ Blocked: {payload[:30]}...")
        else:
            print(f"  ✗ Allowed: {payload[:30]}...")
    
    success_rate = blocked_count / len(malicious_inputs)
    print(f"SQL injection detection rate: {success_rate:.1%}")
    return success_rate >= 0.8

def test_xss_detection():
    """Test XSS detection"""
    print("\nTesting XSS detection...")
    
    xss_inputs = [
        "<script>alert('XSS')</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert('XSS')>",
        "<iframe src='javascript:alert(\"XSS\")'></iframe>"
    ]
    
    blocked_count = 0
    for payload in xss_inputs:
        result = validate_against_injection_attacks(payload)
        if not result.is_valid:
            blocked_count += 1
            print(f"  ✓ Blocked: {payload[:30]}...")
        else:
            print(f"  ✗ Allowed: {payload[:30]}...")
    
    success_rate = blocked_count / len(xss_inputs)
    print(f"XSS detection rate: {success_rate:.1%}")
    return success_rate >= 0.8

def test_input_validation():
    """Test input validation functions"""
    print("\nTesting input validation...")
    
    # Test email validation
    valid_email = validate_email_address("user@gmail.com")
    invalid_email = validate_email_address("invalid-email")
    
    # Test URL validation
    valid_url = validate_url("https://example.com")
    invalid_url = validate_url("not-a-url")
    
    # Test service name validation
    valid_service = validate_service_name("valid_service")
    invalid_service = validate_service_name("Invalid Service!")
    
    tests_passed = (
        valid_email.is_valid and
        not invalid_email.is_valid and
        valid_url.is_valid and
        not invalid_url.is_valid and
        valid_service.is_valid and
        not invalid_service.is_valid
    )
    
    print(f"  Email validation: {'✓' if valid_email.is_valid and not invalid_email.is_valid else '✗'}")
    print(f"  URL validation: {'✓' if valid_url.is_valid and not invalid_url.is_valid else '✗'}")
    print(f"  Service name validation: {'✓' if valid_service.is_valid and not invalid_service.is_valid else '✗'}")
    
    return tests_passed

def test_security_monitoring():
    """Test security monitoring functionality"""
    print("\nTesting security monitoring...")
    
    # Test security monitor status
    status = security_monitor.get_security_status()
    metrics = security_metrics.get_metrics()
    
    # Test IP tracking
    test_ip = "192.168.1.100"
    security_monitor.track_failed_login(test_ip)
    security_monitor.track_request(test_ip, is_error=True)
    
    monitoring_works = (
        isinstance(status, dict) and
        "blocked_ips" in status and
        "suspicious_ips" in status and
        isinstance(metrics, dict)
    )
    
    print(f"  Security monitor status: {'✓' if monitoring_works else '✗'}")
    print(f"  Metrics collection: {'✓' if isinstance(metrics, dict) else '✗'}")
    
    return monitoring_works

def test_configuration():
    """Test security configuration"""
    print("\nTesting security configuration...")
    
    config_valid = (
        settings.ENABLE_RATE_LIMITING and
        settings.ENABLE_SECURITY_HEADERS and
        settings.ENABLE_SQL_INJECTION_DETECTION and
        settings.ENABLE_XSS_DETECTION and
        settings.RATE_LIMIT_REQUESTS_PER_MINUTE > 0 and
        settings.RATE_LIMIT_BURST_SIZE > 0
    )
    
    print(f"  Rate limiting enabled: {'✓' if settings.ENABLE_RATE_LIMITING else '✗'}")
    print(f"  Security headers enabled: {'✓' if settings.ENABLE_SECURITY_HEADERS else '✗'}")
    print(f"  SQL injection detection: {'✓' if settings.ENABLE_SQL_INJECTION_DETECTION else '✗'}")
    print(f"  XSS detection enabled: {'✓' if settings.ENABLE_XSS_DETECTION else '✗'}")
    print(f"  Rate limits configured: {'✓' if settings.RATE_LIMIT_REQUESTS_PER_MINUTE > 0 else '✗'}")
    
    return config_valid

def main():
    """Run all security tests"""
    print("=" * 60)
    print("CIPHERMATE SECURITY IMPLEMENTATION VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("SQL Injection Detection", test_sql_injection_detection),
        ("XSS Detection", test_xss_detection),
        ("Input Validation", test_input_validation),
        ("Security Monitoring", test_security_monitoring),
        ("Security Configuration", test_configuration)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"\n{test_name}: ✓ PASSED")
            else:
                print(f"\n{test_name}: ✗ FAILED")
        except Exception as e:
            print(f"\n{test_name}: ✗ FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All security measures are working correctly!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} security test(s) failed. Please review the implementation.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()