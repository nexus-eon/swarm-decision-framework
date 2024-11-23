"""
Configuration management for the Decision Framework.
Handles environment variables, settings, and configuration validation.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

@dataclass
class FrameworkConfig:
    """Configuration settings for the Decision Framework."""
    
    # OpenAI Configuration
    openai_api_key: str
    temperature: float = 0.7
    
    # Environment Configuration
    environment: str = "development"
    log_level: str = "DEBUG"
    enable_cognitive_monitoring: bool = True
    
    # Cache Configuration
    enable_response_cache: bool = True
    cache_ttl: int = 3600  # seconds
    
    @classmethod
    def from_env(cls) -> 'FrameworkConfig':
        """Create configuration from environment variables."""
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it in your .env file or environment."
            )
        
        return cls(
            openai_api_key=openai_api_key,
            temperature=float(os.getenv('TEMPERATURE', cls.temperature)),
            environment=os.getenv('ENVIRONMENT', cls.environment),
            log_level=os.getenv('LOG_LEVEL', cls.log_level),
            enable_cognitive_monitoring=os.getenv(
                'ENABLE_COGNITIVE_MONITORING', 
                str(cls.enable_cognitive_monitoring)
            ).lower() == 'true',
            enable_response_cache=os.getenv(
                'ENABLE_RESPONSE_CACHE',
                str(cls.enable_response_cache)
            ).lower() == 'true',
            cache_ttl=int(os.getenv('CACHE_TTL', cls.cache_ttl))
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        valid_environments = {'development', 'staging', 'production'}
        if self.environment not in valid_environments:
            raise ValueError(
                f"Invalid environment: {self.environment}. "
                f"Must be one of: {valid_environments}"
            )
        
        valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.log_level not in valid_log_levels:
            raise ValueError(
                f"Invalid log level: {self.log_level}. "
                f"Must be one of: {valid_log_levels}"
            )
        
        if not isinstance(self.temperature, float) or not 0 <= self.temperature <= 1:
            raise ValueError("Temperature must be a float between 0 and 1")
        
        if not isinstance(self.cache_ttl, int) or self.cache_ttl < 0:
            raise ValueError("Cache TTL must be a positive integer")


@lru_cache()
def get_config() -> FrameworkConfig:
    """Get framework configuration (cached)."""
    config = FrameworkConfig.from_env()
    config.validate()
    return config
