from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os
import json


class Settings(BaseSettings):
    """Application settings"""

    # App Configuration
    APP_NAME: str = "CipherMate"
    APP_ENV: str = "development"
    DEBUG: bool = True
    APP_BASE_URL: str = "http://localhost:8080"

    # Database Configuration
    #done
    DATABASE_URL: str = "sqlite+aiosqlite:///./ciphermate.db"

    # Redis Configuration
    REDIS_URL: str = ""
    DISABLE_REDIS: bool = False

    @property
    def redis_url_validated(self) -> str:
        """Get validated Redis URL with proper scheme"""
        if not self.REDIS_URL or self.REDIS_URL.strip() == "":
            return ""
        
        url = self.REDIS_URL.strip()
        
        # Ensure URL has proper scheme
        if not (url.startswith("redis://") or url.startswith("rediss://") or url.startswith("unix://")):
            # If it looks like a host:port format, add redis:// prefix
            if ":" in url and "//" not in url:
                return f"redis://{url}"
            return ""  # Invalid format
        
        return url
    
    # Auth0 Configuration
    AUTH0_DOMAIN: str = ""
    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: str = ""
    AUTH0_AUDIENCE: str = ""
    AUTH0_ALGORITHMS: str = "RS256"  # Changed to string for env var compatibility
    
    @property
    def auth0_algorithms_list(self) -> List[str]:
        """Get AUTH0_ALGORITHMS as a list (supports both comma-separated and JSON formats)"""
        if not self.AUTH0_ALGORITHMS:
            return ["RS256"]
        
        # Try to parse JSON array first
        try:
            parsed = json.loads(self.AUTH0_ALGORITHMS)
            if isinstance(parsed, list):
                return parsed
        except:
            pass
        
        # Fall back to comma-separated string
        return [alg.strip() for alg in self.AUTH0_ALGORITHMS.split(",") if alg.strip()]
    
    # AI Configuration
    GEMINI_API_KEY: str = ""
    
    # Third-party Service Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    SLACK_CLIENT_ID: str = ""
    SLACK_CLIENT_SECRET: str = ""
    
    # Gmail Configuration
    GMAIL_ENABLED: bool = False
    GMAIL_SCOPES: str = "https://www.googleapis.com/auth/gmail.send"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,https://localhost:3000"
    
    # Frontend URL for OAuth redirects
    FRONTEND_URL: str = "http://localhost:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get ALLOWED_ORIGINS as a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


    # Security Configuration
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST_SIZE: int = 10
    MAX_REQUEST_SIZE_MB: int = 10
    MAX_HEADER_SIZE_KB: int = 8
    ENABLE_SECURITY_HEADERS: bool = True
    ENABLE_RATE_LIMITING: bool = True
    
    # Security monitoring thresholds
    FAILED_LOGIN_THRESHOLD: int = 5
    RAPID_REQUEST_THRESHOLD: int = 20
    ERROR_RATE_THRESHOLD: float = 0.5
    
    # IP blocking configuration
    IP_BLOCK_DURATION_MINUTES: int = 15
    SUSPICIOUS_IP_THRESHOLD: int = 3
    
    # Request validation limits
    MAX_JSON_DEPTH: int = 5
    MAX_JSON_KEYS: int = 100
    MAX_ARRAY_SIZE: int = 1000
    
    # SQL Injection Prevention
    ENABLE_SQL_INJECTION_DETECTION: bool = True
    SQL_INJECTION_PATTERNS: List[str] = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
        r"(INFORMATION_SCHEMA|SYSOBJECTS|SYSCOLUMNS)",
    ]
    
    # XSS Prevention
    ENABLE_XSS_DETECTION: bool = True
    XSS_PATTERNS: List[str] = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"data:text/html",
        r"vbscript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]
    
    @property
    def auth0_issuer_url(self) -> str:
        """Get Auth0 issuer URL"""
        return f"https://{self.AUTH0_DOMAIN}/"
    
    @property
    def auth0_jwks_url(self) -> str:
        """Get Auth0 JWKS URL"""
        return f"https://{self.AUTH0_DOMAIN}/.well-known/jwks.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in .env without error


settings = Settings()