"""
PostgreSQL & In-Memory Data Models for PersonaScript.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class User:
    """User entity model."""

    id: str
    email: str
    hashed_password: str
    full_name: str
    role: str = "marketer"  # admin, marketer, user
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Persona:
    """Persona profile entity model."""

    id: str
    user_id: str
    name: str
    role: str
    company_size: str
    goals: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ContentGeneration:
    """AI Content Generation record entity model."""

    id: str
    user_id: str
    persona_id: str
    prompt: str
    output_text: str
    model_used: str
    funnel_stage: str
    token_count: int
    execution_time_ms: int
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AuditLog:
    """Security and compliance audit log entity model."""

    id: str
    user_id: str
    action: str
    resource: str
    ip_address: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
