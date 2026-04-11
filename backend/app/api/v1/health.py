"""Health check and monitoring endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from datetime import datetime

from app.core.monitoring import health_checker, metrics_collector, SystemMonitor
from app.core.cache import cache_service
from app.core.auth import get_optional_user

router = APIRouter(prefix="/health", tags=["health"])
    # // done hadiqa


@router.get("/")
async def basic_health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ciphermate-backend"
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with all services"""
    try:
        health_status = await health_checker.run_all_checks()
        return health_status
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@router.get("/metrics")
async def get_metrics(current_user: Optional[Dict] = Depends(get_optional_user)) -> Dict[str, Any]:
    """Get application metrics (requires authentication for detailed metrics)"""
    try:
        # Basic metrics for unauthenticated users
        basic_metrics = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": "available"
        }
        
        if current_user:
            # Detailed metrics for authenticated users
            metrics_summary = await metrics_collector.get_metrics_summary()
            system_monitor = SystemMonitor()
            system_metrics = await system_monitor.get_system_metrics()
            
            return {
                **basic_metrics,
                "application_metrics": metrics_summary,
                "system_metrics": system_metrics,
                "cache_stats": await cache_service.get_stats()
            }
        
        return basic_metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics collection failed: {str(e)}")


@router.get("/database")
async def database_health() -> Dict[str, Any]:
    """Check database connectivity and performance"""
    try:
        from app.core.database import engine
        import time
        
        start_time = time.time()
        
        async with engine.begin() as conn:
            # Test basic connectivity
            result = await conn.execute("SELECT 1 as test")
            test_value = result.scalar()
            
            # Test a simple query performance
            result = await conn.execute("SELECT COUNT(*) FROM users")
            user_count = result.scalar()
            
        response_time = time.time() - start_time
        
        return {
            "status": "healthy",
            "connected": True,
            "response_time_ms": round(response_time * 1000, 2),
            "test_query_result": test_value,
            "user_count": user_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/redis")
async def redis_health() -> Dict[str, Any]:
    """Check Redis connectivity and performance"""
    return await cache_service.health_check()


@router.get("/external-services")
async def external_services_health(
    current_user: Optional[Dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """Check external service connectivity (requires authentication)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        import httpx
        import asyncio
        
        services = {
            "auth0": f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json",
            "google": "https://www.googleapis.com/oauth2/v1/tokeninfo",
            "github": "https://api.github.com/",
            "slack": "https://slack.com/api/api.test"
        }
        
        results = {}
        
        async def check_service(name: str, url: str):
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    start_time = time.time()
                    response = await client.get(url)
                    response_time = time.time() - start_time
                    
                    return {
                        "status": "healthy" if response.status_code < 500 else "degraded",
                        "status_code": response.status_code,
                        "response_time_ms": round(response_time * 1000, 2),
                        "reachable": True
                    }
            except Exception as e:
                return {
                    "status": "unhealthy",
                    "error": str(e),
                    "reachable": False
                }
        
        # Check all services concurrently
        tasks = [check_service(name, url) for name, url in services.items()]
        service_results = await asyncio.gather(*tasks)
        
        for (name, _), result in zip(services.items(), service_results):
            results[name] = result
        
        # Determine overall status
        overall_status = "healthy"
        if any(result["status"] == "unhealthy" for result in results.values()):
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "services": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"External service check failed: {str(e)}")


@router.get("/performance")
async def performance_metrics(
    current_user: Optional[Dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """Get performance metrics (requires authentication)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Get cached metrics if available
        cached_metrics = await cache_service.get("app_metrics", prefix="monitoring")
        if cached_metrics:
            return {
                "cached": True,
                "timestamp": datetime.utcnow().isoformat(),
                **cached_metrics
            }
        
        # Generate fresh metrics
        metrics_summary = await metrics_collector.get_metrics_summary()
        system_monitor = SystemMonitor()
        system_metrics = await system_monitor.get_system_metrics()
        
        result = {
            "cached": False,
            "timestamp": datetime.utcnow().isoformat(),
            "application_metrics": metrics_summary,
            "system_metrics": system_metrics
        }
        
        # Cache for future requests
        await cache_service.set("app_metrics", result, ttl=60, prefix="monitoring")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance metrics failed: {str(e)}")


@router.post("/reset-metrics")
async def reset_metrics(
    current_user: Optional[Dict] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """Reset application metrics (requires authentication)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Reset metrics collector
        global metrics_collector
        metrics_collector = MetricsCollector()
        
        # Clear cached metrics
        await cache_service.flush_prefix("monitoring")
        
        return {
            "status": "success",
            "message": "Metrics reset successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics reset failed: {str(e)}")


# Import settings at the end to avoid circular imports
from app.core.config import settings
import time