"""
Pydantic Schemas for Request and Response Objects in PersonaScript API.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# User / Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: Optional[str] = "marketer"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: str


# Persona Schemas
class PersonaCreate(BaseModel):
    name: str
    role: str
    company_size: str
    goals: List[str] = []
    challenges: List[str] = []
    pain_points: List[str] = []


class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company_size: Optional[str] = None
    goals: Optional[List[str]] = None
    challenges: Optional[List[str]] = None
    pain_points: Optional[List[str]] = None


class PersonaResponse(BaseModel):
    id: str
    user_id: str
    name: str
    role: str
    company_size: str
    goals: List[str]
    challenges: List[str]
    pain_points: List[str]
    created_at: str


# AI Orchestration Schemas
class AIGenerateRequest(BaseModel):
    persona_id: str
    funnel_stage: str = Field("Awareness", description="Awareness, Consideration, or Decision")
    prompt_topic: str
    preferred_model: str = Field("gpt-4o", description="gpt-4o, claude-3-5-sonnet, or mock")
    target_format: str = Field("email", description="email, blog, landing_page, social")


class AIGenerateResponse(BaseModel):
    generation_id: str
    persona_id: str
    funnel_stage: str
    model_used: str
    generated_content: str
    cached: bool = False
    token_count: int
    execution_time_ms: int
    created_at: str


class HealthCheckResponse(BaseModel):
    status: str
    version: str
    database: str
    cache: str
    ai_orchestration: str
