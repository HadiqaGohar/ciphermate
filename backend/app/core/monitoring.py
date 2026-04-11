"""Application performance monitoring and metrics collection"""

import time
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import psutil
import logging
from contextlib import asynccontextmanager

from app.core.cache import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Individual metric data point"""
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics container"""
    request_count: int = 0
    error_count: int = 0
    total_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    active_requests: int = 0
    
    @property
    def avg_response_time(self) -> float:
        return self.total_response_time / self.request_count if self.request_count > 0 else 0.0
    
    @property
    def error_rate(self) -> float:
        return self.error_count / self.request_count if self.request_count > 0 else 0.0


class MetricsCollector:
    """Collect and store application metrics"""
    
    def __init__(self, max_points: int = 1000):
        self.max_points = max_points
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_points))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.performance_metrics = PerformanceMetrics()
        self._lock = asyncio.Lock()
    
    async def record_counter(self, name: str, value: int = 1, labels: Dict[str, str] = None):
        """Record a counter metric"""
        async with self._lock:
            key = self._make_key(name, labels)
            self.counters[key] += value
            
            # Also store as time series
            point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {}
            )
            self.metrics[name].append(point)
    
    async def record_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a gauge metric"""
        async with self._lock:
            key = self._make_key(name, labels)
            self.gauges[key] = value
            
            point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {}
            )
            self.metrics[name].append(point)
    
    async def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram metric"""
        async with self._lock:
            key = self._make_key(name, labels)
            self.histograms[key].append(value)
            
            # Keep only recent values
            if len(self.histograms[key]) > self.max_points:
                self.histograms[key] = self.histograms[key][-self.max_points:]
            
            point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {}
            )
            self.metrics[name].append(point)
    
    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """Create a unique key for metric with labels"""
        if not labels:
            return name
        
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}[{label_str}]"
    
    async def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        async with self._lock:
            return {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "histograms": {
                    name: {
                        "count": len(values),
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0,
                        "avg": sum(values) / len(values) if values else 0,
                        "p95": self._percentile(values, 95) if values else 0,
                        "p99": self._percentile(values, 99) if values else 0,
                    }
                    for name, values in self.histograms.items()
                },
                "performance": {
                    "request_count": self.performance_metrics.request_count,
                    "error_count": self.performance_metrics.error_count,
                    "error_rate": self.performance_metrics.error_rate,
                    "avg_response_time": self.performance_metrics.avg_response_time,
                    "min_response_time": self.performance_metrics.min_response_time,
                    "max_response_time": self.performance_metrics.max_response_time,
                    "active_requests": self.performance_metrics.active_requests,
                }
            }
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    async def record_request_start(self):
        """Record the start of a request"""
        async with self._lock:
            self.performance_metrics.active_requests += 1
    
    async def record_request_end(self, response_time: float, is_error: bool = False):
        """Record the end of a request"""
        async with self._lock:
            self.performance_metrics.active_requests -= 1
            self.performance_metrics.request_count += 1
            self.performance_metrics.total_response_time += response_time
            
            if response_time < self.performance_metrics.min_response_time:
                self.performance_metrics.min_response_time = response_time
            if response_time > self.performance_metrics.max_response_time:
                self.performance_metrics.max_response_time = response_time
            
            if is_error:
                self.performance_metrics.error_count += 1


class SystemMonitor:
    """Monitor system resources and health"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = datetime.utcnow()
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            process_memory = self.process.memory_info()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics (if available)
            try:
                network = psutil.net_io_counters()
                network_stats = {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv,
                }
            except Exception:
                network_stats = {}
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count,
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "process_rss": process_memory.rss,
                    "process_vms": process_memory.vms,
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent,
                },
                "network": network_stats,
                "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            }
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    async def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        metrics = await self.get_system_metrics()
        
        # Define health thresholds
        cpu_threshold = 80.0
        memory_threshold = 85.0
        disk_threshold = 90.0
        
        health_status = "healthy"
        issues = []
        
        if metrics.get("cpu", {}).get("percent", 0) > cpu_threshold:
            health_status = "warning"
            issues.append(f"High CPU usage: {metrics['cpu']['percent']:.1f}%")
        
        if metrics.get("memory", {}).get("percent", 0) > memory_threshold:
            health_status = "warning"
            issues.append(f"High memory usage: {metrics['memory']['percent']:.1f}%")
        
        if metrics.get("disk", {}).get("percent", 0) > disk_threshold:
            health_status = "critical"
            issues.append(f"High disk usage: {metrics['disk']['percent']:.1f}%")
        
        return {
            "status": health_status,
            "issues": issues,
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat(),
        }


class HealthChecker:
    """Comprehensive health checking for all services"""
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.checks = {}
    
    def register_check(self, name: str, check_func):
        """Register a health check function"""
        self.checks[name] = check_func
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all registered health checks"""
        results = {}
        overall_status = "healthy"
        
        # System health
        system_health = await self.system_monitor.check_system_health()
        results["system"] = system_health
        
        if system_health["status"] != "healthy":
            overall_status = system_health["status"]
        
        # Database health
        try:
            from app.core.database import engine
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            results["database"] = {"status": "healthy", "connected": True}
        except Exception as e:
            results["database"] = {"status": "unhealthy", "error": str(e), "connected": False}
            overall_status = "critical"
        
        # Redis health
        redis_health = await cache_service.health_check()
        results["redis"] = redis_health
        
        if redis_health["status"] not in ["healthy", "unavailable"]:
            overall_status = "warning" if overall_status == "healthy" else overall_status
        
        # Custom checks
        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[name] = result
                
                if result.get("status") != "healthy":
                    overall_status = "warning" if overall_status == "healthy" else overall_status
                    
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
                overall_status = "warning" if overall_status == "healthy" else overall_status
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": results,
        }


# Global instances
metrics_collector = MetricsCollector()
health_checker = HealthChecker()


@asynccontextmanager
async def track_request_metrics(endpoint: str = "unknown"):
    """Context manager to track request metrics"""
    start_time = time.time()
    await metrics_collector.record_request_start()
    
    try:
        yield
        # Success
        response_time = time.time() - start_time
        await metrics_collector.record_request_end(response_time, is_error=False)
        await metrics_collector.record_histogram("request_duration", response_time, {"endpoint": endpoint})
        await metrics_collector.record_counter("requests_total", 1, {"endpoint": endpoint, "status": "success"})
        
    except Exception as e:
        # Error
        response_time = time.time() - start_time
        await metrics_collector.record_request_end(response_time, is_error=True)
        await metrics_collector.record_histogram("request_duration", response_time, {"endpoint": endpoint})
        await metrics_collector.record_counter("requests_total", 1, {"endpoint": endpoint, "status": "error"})
        await metrics_collector.record_counter("errors_total", 1, {"endpoint": endpoint, "error_type": type(e).__name__})
        raise


async def record_business_metric(metric_name: str, value: float, labels: Dict[str, str] = None):
    """Record a business-specific metric"""
    await metrics_collector.record_gauge(metric_name, value, labels)


async def record_api_call_metric(service: str, endpoint: str, response_time: float, status_code: int):
    """Record metrics for external API calls"""
    labels = {
        "service": service,
        "endpoint": endpoint,
        "status_code": str(status_code)
    }
    
    await metrics_collector.record_histogram("external_api_duration", response_time, labels)
    await metrics_collector.record_counter("external_api_calls", 1, labels)
    
    if status_code >= 400:
        await metrics_collector.record_counter("external_api_errors", 1, labels)


# Background task to periodically cache metrics
async def cache_metrics_task():
    """Background task to cache metrics for dashboard"""
    while True:
        try:
            metrics_summary = await metrics_collector.get_metrics_summary()
            await cache_service.set("app_metrics", metrics_summary, ttl=60, prefix="monitoring")
            
            health_status = await health_checker.run_all_checks()
            await cache_service.set("health_status", health_status, ttl=30, prefix="monitoring")
            
            # Sleep for 30 seconds
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"Error in metrics caching task: {e}")
            await asyncio.sleep(60)  # Wait longer on error