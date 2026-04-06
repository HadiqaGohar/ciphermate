# #!/usr/bin/env python3
# """
# Demo script to showcase performance monitoring and optimization features
# """

# import asyncio
# import time
# import random
# from app.core.monitoring import metrics_collector, SystemMonitor, health_checker
# from app.core.cache import cache_service, cached


# async def demo_metrics_collection():
#     """Demonstrate metrics collection"""
#     print("🔍 Demonstrating Metrics Collection")
#     print("=" * 50)
    
#     # Record various types of metrics
#     print("Recording counter metrics...")
#     for i in range(10):
#         await metrics_collector.record_counter("demo_requests", 1, {"endpoint": f"/api/v{i%3+1}"})
#         await asyncio.sleep(0.1)
    
#     print("Recording gauge metrics...")
#     for i in range(5):
#         cpu_usage = random.uniform(10, 90)
#         await metrics_collector.record_gauge("demo_cpu_usage", cpu_usage)
#         await asyncio.sleep(0.2)
    
#     print("Recording histogram metrics...")
#     for i in range(20):
#         response_time = random.uniform(0.1, 2.0)
#         await metrics_collector.record_histogram("demo_response_time", response_time, {"service": "api"})
#         await asyncio.sleep(0.05)
    
#     # Get metrics summary
#     summary = await metrics_collector.get_metrics_summary()
    
#     print("\n📊 Metrics Summary:")
#     print(f"  Counters: {len(summary['counters'])} metrics")
#     print(f"  Gauges: {len(summary['gauges'])} metrics")
#     print(f"  Histograms: {len(summary['histograms'])} metrics")
    
#     # Show histogram details
#     if "demo_response_time" in summary["histograms"]:
#         hist = summary["histograms"]["demo_response_time"]
#         print(f"\n  Response Time Histogram:")
#         print(f"    Count: {hist['count']}")
#         print(f"    Min: {hist['min']:.3f}s")
#         print(f"    Max: {hist['max']:.3f}s")
#         print(f"    Avg: {hist['avg']:.3f}s")
#         print(f"    P95: {hist['p95']:.3f}s")
#         print(f"    P99: {hist['p99']:.3f}s")


# async def demo_system_monitoring():
#     """Demonstrate system monitoring"""
#     print("\n🖥️  Demonstrating System Monitoring")
#     print("=" * 50)
    
#     monitor = SystemMonitor()
    
#     # Get system metrics
#     metrics = await monitor.get_system_metrics()
    
#     print("System Resource Usage:")
#     print(f"  CPU: {metrics['cpu']['percent']:.1f}% ({metrics['cpu']['count']} cores)")
#     print(f"  Memory: {metrics['memory']['percent']:.1f}% ({metrics['memory']['used'] / 1024**3:.1f}GB used)")
#     print(f"  Disk: {metrics['disk']['percent']:.1f}% ({metrics['disk']['free'] / 1024**3:.1f}GB free)")
#     print(f"  Uptime: {metrics['uptime_seconds']:.0f} seconds")
    
#     if metrics.get('network'):
#         net = metrics['network']
#         print(f"  Network: {net['bytes_sent'] / 1024**2:.1f}MB sent, {net['bytes_recv'] / 1024**2:.1f}MB received")
    
#     # Check system health
#     health = await monitor.check_system_health()
#     print(f"\nSystem Health: {health['status'].upper()}")
#     if health['issues']:
#         print("Issues detected:")
#         for issue in health['issues']:
#             print(f"  ⚠️  {issue}")


# async def demo_cache_operations():
#     """Demonstrate cache operations"""
#     print("\n💾 Demonstrating Cache Operations")
#     print("=" * 50)
    
#     # Test basic cache operations
#     print("Testing basic cache operations...")
    
#     # Set some values
#     test_data = {
#         "user:123": {"name": "John Doe", "email": "john@example.com"},
#         "session:abc": {"user_id": 123, "expires": "2024-03-29T10:00:00Z"},
#         "config:app": {"theme": "dark", "language": "en"}
#     }
    
#     for key, value in test_data.items():
#         success = await cache_service.set(key, value, ttl=300)
#         print(f"  Set {key}: {'✓' if success else '✗'}")
    
#     # Get values
#     print("\nRetrieving cached values...")
#     for key in test_data.keys():
#         value = await cache_service.get(key)
#         print(f"  Get {key}: {'✓' if value else '✗'}")
    
#     # Test cache with prefixes
#     print("\nTesting cache with prefixes...")
#     await cache_service.set("temp_data", {"timestamp": time.time()}, prefix="session")
#     cached_value = await cache_service.get("temp_data", prefix="session")
#     print(f"  Prefix cache: {'✓' if cached_value else '✗'}")
    
#     # Get cache health
#     health = await cache_service.health_check()
#     print(f"\nCache Health: {health['status'].upper()}")
#     if health.get('connected'):
#         print(f"  Memory Usage: {health.get('memory_usage', 'N/A')}")
#         print(f"  Connected Clients: {health.get('connected_clients', 'N/A')}")


# @cached(ttl=60, prefix="demo")
# async def expensive_computation(n: int) -> dict:
#     """Simulate an expensive computation that benefits from caching"""
#     print(f"  Computing expensive operation for n={n}...")
#     await asyncio.sleep(1)  # Simulate work
#     return {
#         "input": n,
#         "result": n ** 2,
#         "computed_at": time.time()
#     }


# async def demo_cache_decorator():
#     """Demonstrate cache decorator"""
#     print("\n🚀 Demonstrating Cache Decorator")
#     print("=" * 50)
    
#     print("First call (should compute):")
#     start_time = time.time()
#     result1 = await expensive_computation(42)
#     duration1 = time.time() - start_time
#     print(f"  Result: {result1['result']}")
#     print(f"  Duration: {duration1:.3f}s")
    
#     print("\nSecond call (should use cache):")
#     start_time = time.time()
#     result2 = await expensive_computation(42)
#     duration2 = time.time() - start_time
#     print(f"  Result: {result2['result']}")
#     print(f"  Duration: {duration2:.3f}s")
    
#     print(f"\nSpeedup: {duration1/duration2:.1f}x faster with cache!")


# async def demo_health_checks():
#     """Demonstrate health checking system"""
#     print("\n🏥 Demonstrating Health Checks")
#     print("=" * 50)
    
#     # Register a custom health check
#     async def demo_service_health():
#         # Simulate a service check
#         await asyncio.sleep(0.1)
#         return {
#             "status": "healthy",
#             "version": "1.0.0",
#             "connections": 5,
#             "last_check": time.time()
#         }
    
#     health_checker.register_check("demo_service", demo_service_health)
    
#     # Run all health checks
#     print("Running comprehensive health checks...")
#     results = await health_checker.run_all_checks()
    
#     print(f"\nOverall Status: {results['status'].upper()}")
#     print(f"Timestamp: {results['timestamp']}")
#     print("\nService Health:")
    
#     for service, health in results['checks'].items():
#         status_icon = "✓" if health['status'] == 'healthy' else "⚠️" if health['status'] == 'warning' else "✗"
#         print(f"  {status_icon} {service}: {health['status']}")
        
#         if health['status'] != 'healthy' and 'error' in health:
#             print(f"    Error: {health['error']}")


# async def demo_performance_tracking():
#     """Demonstrate performance tracking"""
#     print("\n⚡ Demonstrating Performance Tracking")
#     print("=" * 50)
    
#     # Simulate request processing with metrics
#     endpoints = ["/api/v1/users", "/api/v1/auth", "/api/v1/data"]
    
#     print("Simulating API requests with performance tracking...")
    
#     for i in range(15):
#         endpoint = random.choice(endpoints)
        
#         # Track request start
#         await metrics_collector.record_request_start()
        
#         # Simulate request processing
#         processing_time = random.uniform(0.05, 0.5)
#         await asyncio.sleep(processing_time)
        
#         # Simulate occasional errors
#         is_error = random.random() < 0.1
        
#         # Track request end
#         await metrics_collector.record_request_end(processing_time, is_error)
        
#         # Record additional metrics
#         status_code = 500 if is_error else 200
#         await metrics_collector.record_histogram("request_duration", processing_time, {
#             "endpoint": endpoint,
#             "status_code": str(status_code)
#         })
        
#         print(f"  {endpoint}: {processing_time:.3f}s {'(ERROR)' if is_error else ''}")
    
#     # Show performance summary
#     summary = await metrics_collector.get_metrics_summary()
#     perf = summary['performance']
    
#     print(f"\nPerformance Summary:")
#     print(f"  Total Requests: {perf['request_count']}")
#     print(f"  Error Rate: {perf['error_rate']:.1%}")
#     print(f"  Avg Response Time: {perf['avg_response_time']:.3f}s")
#     print(f"  Min Response Time: {perf['min_response_time']:.3f}s")
#     print(f"  Max Response Time: {perf['max_response_time']:.3f}s")
#     print(f"  Active Requests: {perf['active_requests']}")


# async def main():
#     """Run all demonstrations"""
#     print("🎯 CipherMate Performance Monitoring & Optimization Demo")
#     print("=" * 60)
#     print("This demo showcases the performance optimization features implemented:")
#     print("• Comprehensive metrics collection")
#     print("• System resource monitoring")
#     print("• Redis caching with decorators")
#     print("• Health checking system")
#     print("• Performance tracking")
#     print("=" * 60)
    
#     try:
#         await demo_metrics_collection()
#         await demo_system_monitoring()
#         await demo_cache_operations()
#         await demo_cache_decorator()
#         await demo_health_checks()
#         await demo_performance_tracking()
        
#         print("\n🎉 Demo completed successfully!")
#         print("\nKey Benefits Demonstrated:")
#         print("✓ Real-time performance metrics collection")
#         print("✓ System resource monitoring and alerting")
#         print("✓ Intelligent caching for improved response times")
#         print("✓ Comprehensive health checking")
#         print("✓ Database query optimization with advanced indexing")
#         print("✓ Request/response performance tracking")
        
#     except Exception as e:
#         print(f"\n❌ Demo failed with error: {e}")
#         import traceback
#         traceback.print_exc()
    
#     finally:
#         # Cleanup
#         await cache_service.close()


# if __name__ == "__main__":
#     asyncio.run(main())