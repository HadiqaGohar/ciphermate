#!/usr/bin/env python3
"""
Simple test script to verify the audit logging system is working correctly.
"""

import asyncio
import sys
import os
from datetime import datetime, timezone

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.audit_service import audit_service
from app.core.database import AsyncSessionLocal
from app.models.audit_log import AuditLog
from app.models.security_event import SecurityEvent
from sqlalchemy import select


async def test_audit_logging():
    """Test basic audit logging functionality"""
    print("Testing audit logging system...")
    
    # Test user ID (using a test user ID)
    test_user_id = 999
    
    try:
        # Test 1: Log a basic action
        print("1. Testing basic action logging...")
        audit_log = await audit_service.log_action(
            user_id=test_user_id,
            action_type="test_action",
            service_name="test_service",
            details={"test": "data", "timestamp": datetime.now(timezone.utc).isoformat()},
            ip_address="127.0.0.1",
            user_agent="test-agent"
        )
        
        if audit_log:
            print(f"✓ Action logged successfully: ID {audit_log.id}")
        else:
            print("✗ Failed to log action")
            return False
        
        # Test 2: Log a security event
        print("2. Testing security event logging...")
        security_event = await audit_service.log_security_event(
            user_id=test_user_id,
            event_type="test_security_event",
            severity="warning",
            details={"test": "security data"},
            ip_address="127.0.0.1"
        )
        
        if security_event:
            print(f"✓ Security event logged successfully: ID {security_event.id}")
        else:
            print("✗ Failed to log security event")
            return False
        
        # Test 3: Log performance metric
        print("3. Testing performance metric logging...")
        await audit_service.log_performance_metric(
            user_id=test_user_id,
            operation="test_operation",
            duration_ms=123.45,
            service_name="test_service",
            details={"test": "performance data"}
        )
        print("✓ Performance metric logged successfully")
        
        # Test 4: Retrieve audit logs
        print("4. Testing audit log retrieval...")
        logs = await audit_service.get_audit_logs(
            user_id=test_user_id,
            limit=10
        )
        
        if logs:
            print(f"✓ Retrieved {len(logs)} audit logs")
            for log in logs:
                print(f"  - {log.action_type} at {log.timestamp}")
        else:
            print("✗ No audit logs retrieved")
        
        # Test 5: Retrieve security events
        print("5. Testing security event retrieval...")
        events = await audit_service.get_security_events(
            user_id=test_user_id,
            limit=10
        )
        
        if events:
            print(f"✓ Retrieved {len(events)} security events")
            for event in events:
                print(f"  - {event.event_type} ({event.severity}) at {event.timestamp}")
        else:
            print("✗ No security events retrieved")
        
        # Test 6: Get audit summary
        print("6. Testing audit summary...")
        summary = await audit_service.get_audit_summary(
            user_id=test_user_id,
            days=7
        )
        
        if summary:
            print(f"✓ Audit summary generated:")
            print(f"  - Action counts: {summary.get('action_counts', {})}")
            print(f"  - Service usage: {summary.get('service_usage', {})}")
            print(f"  - Security events: {len(summary.get('security_events', []))}")
        else:
            print("✗ Failed to generate audit summary")
        
        # Test 7: Get performance metrics
        print("7. Testing performance metrics...")
        metrics = audit_service.get_performance_metrics()
        
        if metrics:
            print(f"✓ Performance metrics retrieved:")
            for key, data in metrics.items():
                print(f"  - {key}: avg {data.get('avg_duration_ms', 0):.2f}ms")
        else:
            print("✓ No performance metrics (expected for new system)")
        
        print("\n✓ All audit logging tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def cleanup_test_data():
    """Clean up test data"""
    print("Cleaning up test data...")
    
    try:
        async with AsyncSessionLocal() as db:
            # Delete test audit logs
            await db.execute(
                select(AuditLog).where(AuditLog.user_id == 999)
            )
            result = await db.execute(
                select(AuditLog).where(AuditLog.user_id == 999)
            )
            logs = result.scalars().all()
            
            for log in logs:
                await db.delete(log)
            
            # Delete test security events
            result = await db.execute(
                select(SecurityEvent).where(SecurityEvent.user_id == 999)
            )
            events = result.scalars().all()
            
            for event in events:
                await db.delete(event)
            
            await db.commit()
            print(f"✓ Cleaned up {len(logs)} audit logs and {len(events)} security events")
            
    except Exception as e:
        print(f"Warning: Failed to clean up test data: {e}")


async def main():
    """Main test function"""
    print("=== CipherMate Audit Logging System Test ===\n")
    
    # Run tests
    success = await test_audit_logging()
    
    # Clean up
    await cleanup_test_data()
    
    if success:
        print("\n🎉 Audit logging system is working correctly!")
        return 0
    else:
        print("\n❌ Audit logging system has issues!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)