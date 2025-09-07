"""
Configuration management for upGrad AI Marketing Automation
"""

import os
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv

# Load environment variables
config_path = Path(__file__).parent.parent.parent.parent / "config" / ".env"
load_dotenv(config_path)

class Settings(BaseSettings):
    """Application settings with validation"""

    # API Configuration
    gemini_api_key: Optional[str] = None
    stability_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    reload: bool = False

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: List[str] = ["*"]

    # Rate Limiting
    rate_limit_per_minute: int = 60
    request_timeout: int = 30

    # AI Configuration
    max_content_length: int = 2000
    content_temperature: float = 0.7
    max_tokens: int = 1500

    # Image Generation
    max_image_size: int = 1024
    image_quality: str = "high"
    default_image_format: str = "png"

    # Localization
    default_language: str = "en"
    supported_cities: str = "Bangalore,Mumbai,Delhi NCR,Hyderabad,Chennai,Pune,Ahmedabad,Kolkata"

    # Performance
    cache_ttl: int = 3600
    max_concurrent_requests: int = 10

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Paths
    data_dir: Path = Path(__file__).parent.parent.parent.parent / "data"
    static_dir: Path = Path(__file__).parent.parent.parent.parent / "frontend" / "static"
    templates_dir: Path = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"

    @validator('gemini_api_key')
    def validate_gemini_key(cls, v):
        if v and not v.startswith('AIza'):
            raise ValueError('Invalid Gemini API key format')
        return v

    @validator('stability_api_key')
    def validate_stability_key(cls, v):
        if v and not v.startswith('sk-'):
            raise ValueError('Invalid Stability API key format')
        return v

    @validator('supported_cities')
    def validate_cities(cls, v):
        if isinstance(v, str):
            cities = [city.strip() for city in v.split(',')]
            if len(cities) == 0:
                raise ValueError('At least one city must be supported')
            return cities
        return v

    def get_supported_cities(self) -> List[str]:
        """Get supported cities as a list"""
        if isinstance(self.supported_cities, str):
            return [city.strip() for city in self.supported_cities.split(',')]
        return self.supported_cities

    class Config:
        env_file = "config/.env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Environment-specific configurations
class DevelopmentConfig(Settings):
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"

class ProductionConfig(Settings):
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"
    cors_origins: List[str] = ["https://yourdomain.com"]

class TestingConfig(Settings):
    debug: bool = True
    log_level: str = "DEBUG"
    # Use dummy API keys for testing
    gemini_api_key: str = "test-gemini-key"
    stability_api_key: str = "test-stability-key"

def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()