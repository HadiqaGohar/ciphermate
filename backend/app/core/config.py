from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "CipherMate"
    APP_ENV: str = "development"
    DEBUG: bool = True
    APP_BASE_URL: str = "http://localhost:8080"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/ciphermate"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # Auth0 Configuration
    AUTH0_DOMAIN: str = ""
    AUTH0_CLIENT_ID: str = ""
    AUTH0_CLIENT_SECRET: str = ""
    AUTH0_AUDIENCE: str = ""
    AUTH0_ALGORITHMS: List[str] = ["RS256"]
    
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