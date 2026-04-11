"""
Security monitoring service for real-time threat detection
"""

import asyncio
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set
from collections import defaultdict, deque
import logging

from .audit_service import audit_service

logger = logging.getLogger(__name__)

    # // done hadiqa

class SecurityMonitor:
    """Real-time security monitoring and threat detection"""
    
    def __init__(self):
        # Threat detection thresholds
        self.failed_login_threshold = 5
        self.rapid_request_threshold = 20  # requests per minute
        self.error_rate_threshold = 0.5   # 50% error rate
        
        # Tracking data structures
        self.failed_logins = defaultdict(deque)  # IP -> deque of timestamps
        self.request_rates = defaultdict(deque)  # IP -> deque of timestamps
        self.error_rates = defaultdict(deque)    # IP -> deque of (timestamp, is_error)
        self.blocked_ips = set()
        self.suspicious_ips = set()
        
        # Monitoring windows
        self.login_window = 300    # 5 minutes
        self.rate_window = 60      # 1 minute
        self.error_window = 300    # 5 minutes
        
        # Monitoring task (will be started when needed)
        self._monitoring_task = None
        self._monitoring_started = False
    
    def start_monitoring(self):
        """Start background monitoring task"""
        if not self._monitoring_started and (self._monitoring_task is None or self._monitoring_task.done()):
            try:
                self._monitoring_task = asyncio.create_task(self._monitoring_loop())
                self._monitoring_started = True
            except RuntimeError:
                # No event loop running, monitoring will start when needed
                pass
    
    def _start_monitoring(self):
        """Internal method to start monitoring (deprecated, use start_monitoring)"""
        self.start_monitoring()
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        while True:
            try:
                await self._cleanup_old_data()
                await self._analyze_patterns()
                await asyncio.sleep(30)  # Run every 30 seconds
            except Exception as e:
                logger.error(f"Security monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _cleanup_old_data(self):
        """Clean up old tracking data"""
        current_time = time.time()
        
        # Clean failed logins
        for ip in list(self.failed_logins.keys()):
            cutoff = current_time - self.login_window
            while self.failed_logins[ip] and self.failed_logins[ip][0] < cutoff:
                self.failed_logins[ip].popleft()
            if not self.failed_logins[ip]:
                del self.failed_logins[ip]
        
        # Clean request rates
        for ip in list(self.request_rates.keys()):
            cutoff = current_time - self.rate_window
            while self.request_rates[ip] and self.request_rates[ip][0] < cutoff:
                self.request_rates[ip].popleft()
            if not self.request_rates[ip]:
                del self.request_rates[ip]
        
        # Clean error rates
        for ip in list(self.error_rates.keys()):
            cutoff = current_time - self.error_window
            while self.error_rates[ip] and self.error_rates[ip][0][0] < cutoff:
                self.error_rates[ip].popleft()
            if not self.error_rates[ip]:
                del self.error_rates[ip]
    
    async def _analyze_patterns(self):
        """Analyze patterns for threats"""
        current_time = time.time()
        
        # Analyze failed login patterns
        for ip, attempts in self.failed_logins.items():
            if len(attempts) >= self.failed_login_threshold:
                await self._handle_threat(ip, "excessive_failed_logins", {
                    "attempts": len(attempts),
                    "threshold": self.failed_login_threshold,
                    "window_minutes": self.login_window // 60
                })
        
        # Analyze request rate patterns
        for ip, requests in self.request_rates.items():
            if len(requests) >= self.rapid_request_threshold:
                await self._handle_threat(ip, "rapid_requests", {
                    "requests": len(requests),
                    "threshold": self.rapid_request_threshold,
                    "window_minutes": self.rate_window // 60
                })
        
        # Analyze error rate patterns
        for ip, errors in self.error_rates.items():
            if len(errors) >= 10:  # Minimum sample size
                error_count = sum(1 for _, is_error in errors if is_error)
                error_rate = error_count / len(errors)
                
                if error_rate >= self.error_rate_threshold:
                    await self._handle_threat(ip, "high_error_rate", {
                        "error_rate": error_rate,
                        "threshold": self.error_rate_threshold,
                        "total_requests": len(errors),
                        "error_count": error_count
                    })
    
    async def _handle_threat(self, ip: str, threat_type: str, details: dict):
        """Handle detected threat"""
        if ip in self.blocked_ips:
            return  # Already handled
        
        # Mark as suspicious first
        if ip not in self.suspicious_ips:
            self.suspicious_ips.add(ip)
            
            # Log security event
            if audit_service:
                try:
                    await audit_service.log_security_event(
                        user_id=0,
                        event_type=f"threat_detected_{threat_type}",
                        severity="warning",
                        details={
                            "client_ip": ip,
                            "threat_type": threat_type,
                            **details
                        },
                        ip_address=ip
                    )
                except Exception as e:
                    logger.error(f"Failed to log threat detection: {e}")
        
        # Escalate to blocking for severe threats
        if threat_type in ["excessive_failed_logins", "rapid_requests"]:
            self.blocked_ips.add(ip)
            
            # Schedule unblock after 15 minutes
            asyncio.create_task(self._schedule_unblock(ip, 900))
            
            logger.warning(f"Blocked IP {ip} due to {threat_type}")
    
    async def _schedule_unblock(self, ip: str, duration: int):
        """Schedule IP unblocking"""
        await asyncio.sleep(duration)
        self.blocked_ips.discard(ip)
        self.suspicious_ips.discard(ip)
        logger.info(f"Unblocked IP: {ip}")
    
    def track_failed_login(self, ip: str):
        """Track failed login attempt"""
        current_time = time.time()
        self.failed_logins[ip].append(current_time)
    
    def track_request(self, ip: str, is_error: bool = False):
        """Track request and error status"""
        current_time = time.time()
        self.request_rates[ip].append(current_time)
        self.error_rates[ip].append((current_time, is_error))
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips
    
    def is_ip_suspicious(self, ip: str) -> bool:
        """Check if IP is suspicious"""
        return ip in self.suspicious_ips
    
    def get_security_status(self) -> Dict:
        """Get current security monitoring status"""
        return {
            "blocked_ips": len(self.blocked_ips),
            "suspicious_ips": len(self.suspicious_ips),
            "monitored_ips": {
                "failed_logins": len(self.failed_logins),
                "request_rates": len(self.request_rates),
                "error_rates": len(self.error_rates)
            },
            "thresholds": {
                "failed_login_threshold": self.failed_login_threshold,
                "rapid_request_threshold": self.rapid_request_threshold,
                "error_rate_threshold": self.error_rate_threshold
            }
        }
    
    async def shutdown(self):
        """Shutdown monitoring"""
        if self._monitoring_task and not self._monitoring_task.done():
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass


# Global security monitor instance
security_monitor = SecurityMonitor()


class SecurityMetrics:
    """Security metrics collection and reporting"""
    
    def __init__(self):
        self.metrics = {
            "requests_blocked": 0,
            "threats_detected": 0,
            "ips_blocked": 0,
            "security_events": defaultdict(int),
            "attack_types": defaultdict(int)
        }
    
    def increment_blocked_requests(self):
        """Increment blocked requests counter"""
        self.metrics["requests_blocked"] += 1
    
    def increment_threats_detected(self, threat_type: str):
        """Increment threats detected counter"""
        self.metrics["threats_detected"] += 1
        self.metrics["attack_types"][threat_type] += 1
    
    def increment_ips_blocked(self):
        """Increment IPs blocked counter"""
        self.metrics["ips_blocked"] += 1
    
    def record_security_event(self, event_type: str):
        """Record security event"""
        self.metrics["security_events"][event_type] += 1
    
    def get_metrics(self) -> Dict:
        """Get current security metrics"""
        return {
            **self.metrics,
            "security_events": dict(self.metrics["security_events"]),
            "attack_types": dict(self.metrics["attack_types"])
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {
            "requests_blocked": 0,
            "threats_detected": 0,
            "ips_blocked": 0,
            "security_events": defaultdict(int),
            "attack_types": defaultdict(int)
        }


# Global security metrics instance
security_metrics = SecurityMetrics()