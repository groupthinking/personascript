"""
Database and Redis Cache Connection Managers for PersonaScript.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MockDatabaseSession:
    """In-memory database session simulation for SQLite/PostgreSQL fallback."""

    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.personas: Dict[str, Dict[str, Any]] = {}
        self.generations: Dict[str, Dict[str, Any]] = {}
        self.audit_logs: Dict[str, Dict[str, Any]] = {}

    def clear(self):
        self.users.clear()
        self.personas.clear()
        self.generations.clear()
        self.audit_logs.clear()


# Global database instance
db_session = MockDatabaseSession()


class RedisCacheClient:
    """Redis caching manager with graceful mock fallback."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._store: Dict[str, str] = {}
        self.is_connected = False
        self._initialize_client()

    def _initialize_client(self):
        """Attempt connection or fallback to in-memory store."""
        try:
            # Check if redis package is available
            import redis
            client = redis.from_url(self.redis_url, socket_timeout=1)
            client.ping()
            self._redis_client = client
            self.is_connected = True
            logger.info(f"Successfully connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.warning(f"Redis connection failed ({e}). Operating in-memory cache mode.")
            self._redis_client = None
            self.is_connected = False

    def get(self, key: str) -> Optional[str]:
        """Retrieve value by key."""
        if self.is_connected and self._redis_client:
            try:
                val = self._redis_client.get(key)
                return val.decode("utf-8") if isinstance(val, bytes) else val
            except Exception:
                pass
        return self._store.get(key)

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Store key-value pair with optional expiration (TTL in seconds)."""
        if self.is_connected and self._redis_client:
            try:
                self._redis_client.set(key, value, ex=ex)
                return True
            except Exception:
                pass
        self._store[key] = value
        return True

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if self.is_connected and self._redis_client:
            try:
                self._redis_client.delete(key)
                return True
            except Exception:
                pass
        if key in self._store:
            del self._store[key]
            return True
        return False

    def flush_all(self):
        """Flush cache store."""
        self._store.clear()


cache_client = RedisCacheClient()
