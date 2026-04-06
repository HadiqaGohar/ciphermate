"""
Test performance monitoring and optimization features
"""

import pytest
import asyncio
import time
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.monitoring import metrics_collector, health_checker, SystemMonitor
from app.core.cache import cache_service


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


class TestPerformanceMonitoring:
    """Test performance monitoring functionality"""
    
    def test_health_endpoint_basic(self, client):
        """Test basic health endpoint"""
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_health_endpoint_detailed(self, client):
        """Test detailed health endpoint"""
        response = client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert "timestamp" in data
    
    def test_metrics_endpoint_unauthenticated(self, client):
        """Test metrics endpoint without authentication"""
        response = client.get("/api/v1/health/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        # Should not include detailed metrics
        assert "application_metrics" not in data
    
    def test_database_health_endpoint(self, client):
        """Test database health endpoint"""
        response = client.get("/api/v1/health/database")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "connected" in data
    
    def test_redis_health_endpoint(self, client):
        """Test Redis health endpoint"""
        response = client.get("/api/v1/health/redis")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_performance_headers(self, client):
        """Test that performance headers are added"""
        response = client.get("/api/v1/health/")
        assert "X-Response-Time" in response.headers
        
        # Response time should be a valid float
        response_time = response.headers["X-Response-Time"]
        assert response_time.endswith("s")
        float(response_time[:-1])  # Should not raise exception


class TestMetricsCollection:
    """Test metrics collection functionality"""
    
    @pytest.mark.asyncio
    async def test_metrics_collector_counter(self):
        """Test counter metrics"""
        await metrics_collector.record_counter("test_counter", 5)
        
        summary = await metrics_collector.get_metrics_summary()
        assert "counters" in summary
        assert "test_counter" in summary["counters"]
        assert summary["counters"]["test_counter"] >= 5
    
    @pytest.mark.asyncio
    async def test_metrics_collector_gauge(self):
        """Test gauge metrics"""
        await metrics_collector.record_gauge("test_gauge", 42.5)
        
        summary = await metrics_collector.get_metrics_summary()
        assert "gauges" in summary
        assert "test_gauge" in summary["gauges"]
        assert summary["gauges"]["test_gauge"] == 42.5
    
    @pytest.mark.asyncio
    async def test_metrics_collector_histogram(self):
        """Test histogram metrics"""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        for value in values:
            await metrics_collector.record_histogram("test_histogram", value)
        
        summary = await metrics_collector.get_metrics_summary()
        assert "histograms" in summary
        assert "test_histogram" in summary["histograms"]
        
        histogram = summary["histograms"]["test_histogram"]
        assert histogram["count"] == len(values)
        assert histogram["min"] == min(values)
        assert histogram["max"] == max(values)
        assert histogram["avg"] == sum(values) / len(values)
    
    @pytest.mark.asyncio
    async def test_request_metrics_tracking(self):
        """Test request metrics tracking"""
        initial_summary = await metrics_collector.get_metrics_summary()
        initial_count = initial_summary["performance"]["request_count"]
        
        await metrics_collector.record_request_start()
        await metrics_collector.record_request_end(0.1, is_error=False)
        
        final_summary = await metrics_collector.get_metrics_summary()
        assert final_summary["performance"]["request_count"] == initial_count + 1
        assert final_summary["performance"]["error_count"] == initial_summary["performance"]["error_count"]


class TestCacheService:
    """Test cache service functionality"""
    
    @pytest.mark.asyncio
    async def test_cache_basic_operations(self):
        """Test basic cache operations"""
        # Set a value
        success = await cache_service.set("test_key", "test_value", ttl=60)
        assert success
        
        # Get the value
        value = await cache_service.get("test_key")
        assert value == "test_value"
        
        # Check if key exists
        exists = await cache_service.exists("test_key")
        assert exists
        
        # Delete the key
        deleted = await cache_service.delete("test_key")
        assert deleted
        
        # Verify deletion
        value = await cache_service.get("test_key")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_cache_complex_data(self):
        """Test caching complex data structures"""
        test_data = {
            "string": "value",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        success = await cache_service.set("complex_key", test_data, ttl=60)
        assert success
        
        retrieved_data = await cache_service.get("complex_key")
        assert retrieved_data == test_data
    
    @pytest.mark.asyncio
    async def test_cache_with_prefix(self):
        """Test cache operations with prefixes"""
        success = await cache_service.set("test_key", "test_value", prefix="user")
        assert success
        
        value = await cache_service.get("test_key", prefix="user")
        assert value == "test_value"
        
        # Should not find without prefix
        value_no_prefix = await cache_service.get("test_key")
        assert value_no_prefix is None
    
    @pytest.mark.asyncio
    async def test_cache_multiple_operations(self):
        """Test multiple cache operations"""
        test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        
        # Set multiple values
        success = await cache_service.set_many(test_data, ttl=60)
        assert success
        
        # Get multiple values
        retrieved_data = await cache_service.get_many(list(test_data.keys()))
        assert retrieved_data == test_data
    
    @pytest.mark.asyncio
    async def test_cache_health_check(self):
        """Test cache health check"""
        health = await cache_service.health_check()
        assert "status" in health
        assert "connected" in health


class TestSystemMonitor:
    """Test system monitoring functionality"""
    
    @pytest.mark.asyncio
    async def test_system_metrics_collection(self):
        """Test system metrics collection"""
        monitor = SystemMonitor()
        metrics = await monitor.get_system_metrics()
        
        assert "cpu" in metrics
        assert "memory" in metrics
        assert "disk" in metrics
        assert "uptime_seconds" in metrics
        
        # CPU metrics
        assert "percent" in metrics["cpu"]
        assert "count" in metrics["cpu"]
        assert isinstance(metrics["cpu"]["percent"], (int, float))
        assert isinstance(metrics["cpu"]["count"], int)
        
        # Memory metrics
        assert "total" in metrics["memory"]
        assert "available" in metrics["memory"]
        assert "percent" in metrics["memory"]
        assert isinstance(metrics["memory"]["percent"], (int, float))
        
        # Disk metrics
        assert "total" in metrics["disk"]
        assert "used" in metrics["disk"]
        assert "free" in metrics["disk"]
        assert "percent" in metrics["disk"]
    
    @pytest.mark.asyncio
    async def test_system_health_check(self):
        """Test system health check"""
        monitor = SystemMonitor()
        health = await monitor.check_system_health()
        
        assert "status" in health
        assert "issues" in health
        assert "metrics" in health
        assert "timestamp" in health
        
        assert health["status"] in ["healthy", "warning", "critical"]
        assert isinstance(health["issues"], list)


class TestHealthChecker:
    """Test health checker functionality"""
    
    @pytest.mark.asyncio
    async def test_health_checker_registration(self):
        """Test health check registration"""
        async def test_check():
            return {"status": "healthy", "test": True}
        
        health_checker.register_check("test_service", test_check)
        
        results = await health_checker.run_all_checks()
        assert "test_service" in results["checks"]
        assert results["checks"]["test_service"]["status"] == "healthy"
        assert results["checks"]["test_service"]["test"] is True
    
    @pytest.mark.asyncio
    async def test_health_checker_failure_handling(self):
        """Test health check failure handling"""
        async def failing_check():
            raise Exception("Test failure")
        
        health_checker.register_check("failing_service", failing_check)
        
        results = await health_checker.run_all_checks()
        assert "failing_service" in results["checks"]
        assert results["checks"]["failing_service"]["status"] == "unhealthy"
        assert "error" in results["checks"]["failing_service"]


class TestPerformanceOptimizations:
    """Test performance optimization features"""
    
    def test_response_time_tracking(self, client):
        """Test that response times are tracked"""
        # Make multiple requests
        for _ in range(5):
            response = client.get("/api/v1/health/")
            assert response.status_code == 200
            assert "X-Response-Time" in response.headers
    
    def test_slow_request_detection(self, client):
        """Test slow request detection"""
        # This would require a slow endpoint to test properly
        # For now, just verify the middleware is working
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_cache_decorator(self):
        """Test cache decorator functionality"""
        from app.core.cache import cached
        
        call_count = 0
        
        @cached(ttl=60, prefix="test")
        async def test_function(arg1, arg2):
            nonlocal call_count
            call_count += 1
            return f"{arg1}_{arg2}_{call_count}"
        
        # First call should execute function
        result1 = await test_function("a", "b")
        assert call_count == 1
        
        # Second call should use cache
        result2 = await test_function("a", "b")
        assert call_count == 1  # Should not increment
        assert result1 == result2
        
        # Different arguments should execute function again
        result3 = await test_function("c", "d")
        assert call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])