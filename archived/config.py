import os
from dataclasses import dataclass
from typing import List, Optional, Dict
import json
from datetime import datetime

@dataclass
class TokenConfig:
    """Token management configuration"""
    # Context and response limits
    MAX_CONTEXT_TOKENS: int = 3000  # Keep within model limit
    MAX_RESPONSE_TOKENS: int = 1000  # Keep within model limit
    MAX_EMBEDDING_TOKENS: int = 16000  # Increased from 8000

    # Daily usage limits
    DAILY_TOKEN_LIMIT: int = 100000  # Increased from 50000
    WARNING_THRESHOLD: float = 0.8  # Warn at 80% of daily limit

    # Model-specific limits
    MODEL_LIMITS: Dict[str, int] = None

    def __post_init__(self):
        if self.MODEL_LIMITS is None:
            self.MODEL_LIMITS = {
                "gpt-3.5-turbo": 4096,
                "gpt-4": 8192,
                "gpt-4-turbo": 128000,
                "text-embedding-ada-002": 8191
            }

@dataclass
class Config:
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    LLM_MODEL: str = "gpt-3.5-turbo"

    # Document Processing - Optimized for token efficiency
    CHUNK_SIZE: int = 1024  # Increased from 512
    CHUNK_OVERLAP: int = 100  # Increased from 50
    TOP_K_RETRIEVAL: int = 5  # Increased from 3

    # Retrieval Quality Control
    SIMILARITY_THRESHOLD: float = 0.75  # Minimum similarity for chunk inclusion
    MAX_CHUNKS_PER_QUERY: int = 3  # Hard limit on retrieved chunks

    # File Paths
    VECTOR_DB_PATH: str = "./vector_db"
    DOCUMENTS_PATH: str = "./documents"
    TOKEN_USAGE_FILE: str = "./token_usage.json"

    # Token Management
    token_config: TokenConfig = None

    # API Settings
    TEMPERATURE: float = 0.1  # Lower temperature for more focused responses
    REQUEST_TIMEOUT: int = 30  # API request timeout in seconds
    MAX_RETRIES: int = 3  # Number of API retry attempts

    def __post_init__(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Initialize token configuration
        if self.token_config is None:
            self.token_config = TokenConfig()

        # Validate token limits against model capabilities
        model_limit = self.token_config.MODEL_LIMITS.get(self.LLM_MODEL, 4096)
        if self.token_config.MAX_CONTEXT_TOKENS + self.token_config.MAX_RESPONSE_TOKENS > model_limit:
            raise ValueError(
                f"Token limits exceed model capacity. "
                f"Context ({self.token_config.MAX_CONTEXT_TOKENS}) + "
                f"Response ({self.token_config.MAX_RESPONSE_TOKENS}) > "
                f"Model limit ({model_limit})"
            )

    def get_daily_usage(self) -> int:
        """Get current daily token usage"""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            with open(self.TOKEN_USAGE_FILE, "r") as f:
                usage = json.load(f)
            return usage.get(today, 0)
        except FileNotFoundError:
            return 0

    def save_token_usage(self, tokens_used: int) -> None:
        """Save token usage to file"""
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            with open(self.TOKEN_USAGE_FILE, "r") as f:
                usage = json.load(f)
        except FileNotFoundError:
            usage = {}

        usage[today] = usage.get(today, 0) + tokens_used

        with open(self.TOKEN_USAGE_FILE, "w") as f:
            json.dump(usage, f, indent=2)

    def is_daily_limit_exceeded(self) -> bool:
        """Check if daily token limit is exceeded"""
        return self.get_daily_usage() >= self.token_config.DAILY_TOKEN_LIMIT

    def is_warning_threshold_reached(self) -> bool:
        """Check if warning threshold is reached"""
        current_usage = self.get_daily_usage()
        warning_limit = self.token_config.DAILY_TOKEN_LIMIT * self.token_config.WARNING_THRESHOLD
        return current_usage >= warning_limit

    def get_remaining_tokens(self) -> int:
        """Get remaining tokens for today"""
        return max(0, self.token_config.DAILY_TOKEN_LIMIT - self.get_daily_usage())

    def calculate_estimated_cost(self, tokens: int = None) -> float:
        """Calculate estimated cost based on token usage"""
        if tokens is None:
            tokens = self.get_daily_usage()

        # Approximate costs (as of 2024)
        cost_per_1k_tokens = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.03,
            "text-embedding-ada-002": 0.0001
        }

        base_cost = cost_per_1k_tokens.get(self.LLM_MODEL, 0.002)
        return (tokens / 1000) * base_cost

# Global configuration instance
config = Config()