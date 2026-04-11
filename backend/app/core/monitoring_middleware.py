"""Performance monitoring middleware integration"""

import time
import asyncio
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.monitoring import track_request_metrics, metrics_collector, record_api_call_metric
from app.core.cache import cache_service

    # // done hadiqa

class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to track performance metrics for all requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.slow_request_threshold = 2.0  # 2 seconds
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Monitor request performance and collect metrics"""
        start_time = time.time()
        endpoint = f"{request.method} {request.url.path}"
        
        try:
            # Use the monitoring context manager
            async with track_request_metrics(endpoint):
                response = await call_next(request)
                
            response_time = time.time() - start_time
            
            # Log slow requests
            if response_time > self.slow_request_threshold:
                await metrics_collector.record_counter("slow_requests_total", 1, {
                    "endpoint": endpoint,
                    "response_time": f"{response_time:.1f}s"
                })
            
            # Add performance headers
            response.headers["X-Response-Time"] = f"{response_time:.3f}s"
            
            # Record additional metrics
            await self._record_endpoint_metrics(endpoint, response_time, response.status_code)
            
            return response
            
        except Exception as e:
            response_time = time.time() - start_time
            
            # Record error metrics
            await metrics_collector.record_histogram("request_duration", response_time, {
                "endpoint": endpoint,
                "status": "error"
            })
            
            await metrics_collector.record_counter("request_errors_total", 1, {
                "endpoint": endpoint,
                "error_type": type(e).__name__
            })
            
            raise
    
    async def _record_endpoint_metrics(self, endpoint: str, response_time: float, status_code: int):
        """Record detailed endpoint metrics"""
        labels = {
            "endpoint": endpoint,
            "status_code": str(status_code),
            "status_class": f"{status_code // 100}xx"
        }
        
        # Record response time histogram
        await metrics_collector.record_histogram("http_request_duration_seconds", response_time, labels)
        
        # Record request counter
        await metrics_collector.record_counter("http_requests_total", 1, labels)
        
        # Record error counter for 4xx and 5xx responses
        if status_code >= 400:
            error_labels = {**labels, "error_type": "http_error"}
            await metrics_collector.record_counter("http_errors_total", 1, error_labels)


class CacheMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track cache performance"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track cache usage metrics"""
        # Record cache stats periodically
        if hasattr(request.state, "cache_stats_recorded"):
            # Already recorded for this request cycle
            pass
        else:
            # Record cache statistics
            try:
                cache_stats = await cache_service.get_stats()
                if cache_stats:
                    await metrics_collector.record_gauge("cache_hit_rate", cache_stats.get("hit_rate", 0))
                    await metrics_collector.record_gauge("cache_memory_usage", cache_stats.get("used_memory", 0))
                    await metrics_collector.record_gauge("cache_connected_clients", cache_stats.get("connected_clients", 0))
                
                request.state.cache_stats_recorded = True
            except Exception:
                # Don't fail requests due to cache metrics
                pass
        
        return await call_next(request)


class BusinessMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track business-specific metrics"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track business metrics based on endpoints"""
        response = await call_next(request)
        
        # Track specific business events
        await self._track_business_events(request, response)
        
        return response
    
    async def _track_business_events(self, request: Request, response: Response):
        """Track business-specific events"""
        try:
            path = request.url.path
            method = request.method
            status_code = response.status_code
            
            # Track authentication events
            if "/api/v1/auth" in path:
                if method == "POST" and status_code == 200:
                    await metrics_collector.record_counter("auth_successful_logins", 1)
                elif method == "POST" and status_code in [401, 403]:
                    await metrics_collector.record_counter("auth_failed_logins", 1)
                elif method == "DELETE" and status_code == 200:
                    await metrics_collector.record_counter("auth_logouts", 1)
            
            # Track token vault operations
            elif "/api/v1/token-vault" in path:
                if method == "POST" and status_code == 200:
                    await metrics_collector.record_counter("token_vault_stores", 1)
                elif method == "GET" and status_code == 200:
                    await metrics_collector.record_counter("token_vault_retrievals", 1)
                elif method == "DELETE" and status_code == 200:
                    await metrics_collector.record_counter("token_vault_revocations", 1)
            
            # Track permission operations
            elif "/api/v1/permissions" in path:
                if method == "POST" and status_code == 200:
                    await metrics_collector.record_counter("permission_grants", 1)
                elif method == "DELETE" and status_code == 200:
                    await metrics_collector.record_counter("permission_revocations", 1)
            
            # Track AI agent interactions
            elif "/api/v1/ai-agent" in path or "/api/v1/agent" in path:
                if method == "POST" and status_code == 200:
                    await metrics_collector.record_counter("ai_agent_requests", 1)
                elif status_code >= 400:
                    await metrics_collector.record_counter("ai_agent_errors", 1)
            
            # Track API integration calls
            elif "/api/v1/integrations" in path:
                if status_code == 200:
                    await metrics_collector.record_counter("api_integration_success", 1)
                elif status_code >= 400:
                    await metrics_collector.record_counter("api_integration_errors", 1)
            
        except Exception:
            # Don't fail requests due to metrics collection
            pass


class ResourceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to monitor system resources during requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self._last_resource_check = 0
        self._resource_check_interval = 30  # Check every 30 seconds
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Monitor system resources"""
        current_time = time.time()
        
        # Check resources periodically
        if current_time - self._last_resource_check > self._resource_check_interval:
            asyncio.create_task(self._collect_resource_metrics())
            self._last_resource_check = current_time
        
        return await call_next(request)
    
    async def _collect_resource_metrics(self):
        """Collect system resource metrics"""
        try:
            import psutil
            
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            await metrics_collector.record_gauge("system_cpu_usage_percent", cpu_percent)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            await metrics_collector.record_gauge("system_memory_usage_percent", memory.percent)
            await metrics_collector.record_gauge("system_memory_available_bytes", memory.available)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            await metrics_collector.record_gauge("system_disk_usage_percent", disk.percent)
            await metrics_collector.record_gauge("system_disk_free_bytes", disk.free)
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            await metrics_collector.record_gauge("process_memory_rss_bytes", process_memory.rss)
            await metrics_collector.record_gauge("process_memory_vms_bytes", process_memory.vms)
            await metrics_collector.record_gauge("process_cpu_percent", process.cpu_percent())
            
        except Exception as e:
            # Don't fail if resource monitoring fails
            import logging
            logging.getLogger(__name__).error(f"Resource monitoring error: {e}")


# Function to add monitoring middleware to the app
def add_monitoring_middleware(app):
    """Add all monitoring middleware to the FastAPI app"""
    
    # Add in reverse order (last added is executed first)
    app.add_middleware(ResourceMonitoringMiddleware)
    app.add_middleware(BusinessMetricsMiddleware)
    app.add_middleware(CacheMetricsMiddleware)
    app.add_middleware(PerformanceMonitoringMiddleware)