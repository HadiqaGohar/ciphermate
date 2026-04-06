#!/usr/bin/env python3
"""
Comprehensive security implementation test for CipherMate
Tests all security measures including rate limiting, input validation, and security monitoring
"""

import asyncio
import json
import time
from typing import Dict, Any
import httpx
import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
from app.main import app
from app.core.security_monitor import security_monitor, security_metrics
from app.core.validation import (
    validate_against_injection_attacks,
    validate_email_address,
    validate_url,
    validate_service_name,
    validate_message_content
)

# Test client
client = TestClient(app)


class SecurityTestSuite:
    """Comprehensive security test suite"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = {}
    
    def test_rate_limiting(self):
        """Test rate limiting middleware"""
        print("Testing rate limiting...")
        
        # Make rapid requests to trigger rate limiting
        responses = []
        for i in range(15):  # Exceed burst limit
            response = client.get("/api/v1/health")
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay
        
        # Check if rate limiting kicked in
        rate_limited = any(status == 429 for status in responses)
        
        self.test_results["rate_limiting"] = {
            "passed": rate_limited,
            "details": f"Rate limiting {'activated' if rate_limited else 'not activated'} after {len(responses)} requests",
            "response_codes": responses
        }
        
        print(f"✓ Rate limiting test: {'PASSED' if rate_limited else 'FAILED'}")
    
    def test_input_validation_sql_injection(self):
        """Test SQL injection prevention"""
        print("Testing SQL injection prevention...")
        
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users --",
            "1; DELETE FROM audit_logs; --"
        ]
        
        results = []
        for payload in sql_injection_payloads:
            result = validate_against_injection_attacks(payload)
            results.append({
                "payload": payload,
                "blocked": not result.is_valid,
                "errors": len(result.errors)
            })
        
        blocked_count = sum(1 for r in results if r["blocked"])
        passed = blocked_count == len(sql_injection_payloads)
        
        self.test_results["sql_injection_prevention"] = {
            "passed": passed,
            "details": f"Blocked {blocked_count}/{len(sql_injection_payloads)} SQL injection attempts",
            "results": results
        }
        
        print(f"✓ SQL injection prevention: {'PASSED' if passed else 'FAILED'}")
    
    def test_input_validation_xss(self):
        """Test XSS prevention"""
        print("Testing XSS prevention...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "data:text/html,<script>alert('XSS')</script>"
        ]
        
        results = []
        for payload in xss_payloads:
            result = validate_against_injection_attacks(payload)
            results.append({
                "payload": payload,
                "blocked": not result.is_valid,
                "errors": len(result.errors)
            })
        
        blocked_count = sum(1 for r in results if r["blocked"])
        passed = blocked_count == len(xss_payloads)
        
        self.test_results["xss_prevention"] = {
            "passed": passed,
            "details": f"Blocked {blocked_count}/{len(xss_payloads)} XSS attempts",
            "results": results
        }
        
        print(f"✓ XSS prevention: {'PASSED' if passed else 'FAILED'}")
    
    def test_security_headers(self):
        """Test security headers"""
        print("Testing security headers...")
        
        response = client.get("/api/v1/health")
        headers = response.headers
        
        required_headers = {
            "x-content-type-options": "nosniff",
            "x-frame-options": "DENY",
            "x-xss-protection": "1; mode=block",
            "referrer-policy": "strict-origin-when-cross-origin",
            "content-security-policy": True,  # Just check if present
        }
        
        header_results = {}
        for header, expected in required_headers.items():
            present = header in headers
            if expected is True:
                header_results[header] = {"present": present, "value": headers.get(header, "")}
            else:
                correct_value = headers.get(header) == expected
                header_results[header] = {
                    "present": present,
                    "correct_value": correct_value,
                    "expected": expected,
                    "actual": headers.get(header, "")
                }
        
        passed = all(
            result["present"] and (result.get("correct_value", True))
            for result in header_results.values()
        )
        
        self.test_results["security_headers"] = {
            "passed": passed,
            "details": "Security headers validation",
            "headers": header_results
        }
        
        print(f"✓ Security headers: {'PASSED' if passed else 'FAILED'}")
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        print("Testing CORS configuration...")
        
        # Test preflight request
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Authorization"
            }
        )
        
        cors_headers = {
            "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
            "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
            "access-control-allow-headers": response.headers.get("access-control-allow-headers"),
            "access-control-allow-credentials": response.headers.get("access-control-allow-credentials")
        }
        
        # Test unauthorized origin
        bad_response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://malicious-site.com",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        passed = (
            response.status_code == 200 and
            "localhost:3000" in cors_headers.get("access-control-allow-origin", "") and
            cors_headers.get("access-control-allow-credentials") == "true"
        )
        
        self.test_results["cors_configuration"] = {
            "passed": passed,
            "details": "CORS configuration validation",
            "cors_headers": cors_headers,
            "preflight_status": response.status_code,
            "bad_origin_status": bad_response.status_code
        }
        
        print(f"✓ CORS configuration: {'PASSED' if passed else 'FAILED'}")
    
    def test_request_size_limits(self):
        """Test request size limits"""
        print("Testing request size limits...")
        
        # Test large JSON payload
        large_payload = {"data": "x" * (2 * 1024 * 1024)}  # 2MB payload
        
        response = client.post(
            "/api/v1/health",  # Using health endpoint for testing
            json=large_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Should be rejected due to size
        size_limit_enforced = response.status_code in [413, 400]
        
        # Test large header
        large_header_response = client.get(
            "/api/v1/health",
            headers={"X-Large-Header": "x" * (10 * 1024)}  # 10KB header
        )
        
        header_limit_enforced = large_header_response.status_code in [400, 413]
        
        passed = size_limit_enforced and header_limit_enforced
        
        self.test_results["request_size_limits"] = {
            "passed": passed,
            "details": "Request size limit validation",
            "large_payload_status": response.status_code,
            "large_header_status": large_header_response.status_code,
            "size_limit_enforced": size_limit_enforced,
            "header_limit_enforced": header_limit_enforced
        }
        
        print(f"✓ Request size limits: {'PASSED' if passed else 'FAILED'}")
    
    def test_content_type_validation(self):
        """Test content type validation"""
        print("Testing content type validation...")
        
        # Test unsupported content type
        response = client.post(
            "/api/v1/health",
            data="test data",
            headers={"Content-Type": "text/plain"}
        )
        
        # Should be rejected
        content_type_enforced = response.status_code == 415
        
        self.test_results["content_type_validation"] = {
            "passed": content_type_enforced,
            "details": "Content type validation",
            "unsupported_type_status": response.status_code,
            "content_type_enforced": content_type_enforced
        }
        
        print(f"✓ Content type validation: {'PASSED' if content_type_enforced else 'FAILED'}")
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        print("Testing input sanitization...")
        
        test_cases = [
            {
                "input": "user@example.com",
                "validator": validate_email_address,
                "should_pass": True
            },
            {
                "input": "invalid-email",
                "validator": validate_email_address,
                "should_pass": False
            },
            {
                "input": "https://example.com",
                "validator": validate_url,
                "should_pass": True
            },
            {
                "input": "http://example.com",
                "validator": lambda x: validate_url(x, require_https=False),
                "should_pass": True
            },
            {
                "input": "valid_service",
                "validator": validate_service_name,
                "should_pass": True
            },
            {
                "input": "Invalid Service!",
                "validator": validate_service_name,
                "should_pass": False
            }
        ]
        
        results = []
        for case in test_cases:
            result = case["validator"](case["input"])
            passed = result.is_valid == case["should_pass"]
            results.append({
                "input": case["input"],
                "expected_valid": case["should_pass"],
                "actual_valid": result.is_valid,
                "test_passed": passed
            })
        
        all_passed = all(r["test_passed"] for r in results)
        
        self.test_results["input_sanitization"] = {
            "passed": all_passed,
            "details": "Input sanitization validation",
            "test_cases": results
        }
        
        print(f"✓ Input sanitization: {'PASSED' if all_passed else 'FAILED'}")
    
    def test_security_monitoring(self):
        """Test security monitoring functionality"""
        print("Testing security monitoring...")
        
        # Test security monitor status
        status = security_monitor.get_security_status()
        metrics = security_metrics.get_metrics()
        
        # Check if monitoring is working
        monitoring_active = (
            isinstance(status, dict) and
            "blocked_ips" in status and
            "suspicious_ips" in status and
            isinstance(metrics, dict)
        )
        
        # Test IP tracking
        test_ip = "192.168.1.100"
        security_monitor.track_failed_login(test_ip)
        security_monitor.track_request(test_ip, is_error=True)
        
        # Check if tracking worked
        tracking_works = (
            test_ip in security_monitor.failed_logins or
            test_ip in security_monitor.error_rates
        )
        
        passed = monitoring_active and tracking_works
        
        self.test_results["security_monitoring"] = {
            "passed": passed,
            "details": "Security monitoring functionality",
            "monitoring_active": monitoring_active,
            "tracking_works": tracking_works,
            "status_keys": list(status.keys()) if isinstance(status, dict) else [],
            "metrics_keys": list(metrics.keys()) if isinstance(metrics, dict) else []
        }
        
        print(f"✓ Security monitoring: {'PASSED' if passed else 'FAILED'}")
    
    def test_suspicious_pattern_detection(self):
        """Test suspicious pattern detection"""
        print("Testing suspicious pattern detection...")
        
        suspicious_inputs = [
            "../../../etc/passwd",
            "javascript:alert('test')",
            "<script>document.cookie</script>",
            "eval(malicious_code)",
            "document.write('xss')"
        ]
        
        results = []
        for input_text in suspicious_inputs:
            result = validate_against_injection_attacks(input_text)
            detected = not result.is_valid or len(result.warnings) > 0
            results.append({
                "input": input_text,
                "detected": detected,
                "errors": len(result.errors),
                "warnings": len(result.warnings)
            })
        
        detection_rate = sum(1 for r in results if r["detected"]) / len(results)
        passed = detection_rate >= 0.8  # At least 80% detection rate
        
        self.test_results["suspicious_pattern_detection"] = {
            "passed": passed,
            "details": f"Suspicious pattern detection rate: {detection_rate:.2%}",
            "detection_rate": detection_rate,
            "results": results
        }
        
        print(f"✓ Suspicious pattern detection: {'PASSED' if passed else 'FAILED'}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("=" * 60)
        print("CIPHERMATE SECURITY IMPLEMENTATION TEST SUITE")
        print("=" * 60)
        
        test_methods = [
            self.test_rate_limiting,
            self.test_input_validation_sql_injection,
            self.test_input_validation_xss,
            self.test_security_headers,
            self.test_cors_configuration,
            self.test_request_size_limits,
            self.test_content_type_validation,
            self.test_input_sanitization,
            self.test_security_monitoring,
            self.test_suspicious_pattern_detection
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                test_name = test_method.__name__
                print(f"✗ {test_name}: FAILED with exception: {e}")
                self.test_results[test_name] = {
                    "passed": False,
                    "details": f"Exception: {str(e)}",
                    "error": str(e)
                }
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["passed"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result["passed"]:
                    print(f"  - {test_name}: {result['details']}")
        
        print("\nDETAILED RESULTS:")
        print(json.dumps(self.test_results, indent=2, default=str))


def main():
    """Main test execution"""
    test_suite = SecurityTestSuite()
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()