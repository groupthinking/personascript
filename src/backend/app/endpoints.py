"""
FastAPI Route Endpoints for Auth, Personas, AI Orchestration, and Health.
"""

import time
import json
import uuid
from typing import List, Optional
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings
from .security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)
from .database import db_session, cache_client
from .models import User, Persona, ContentGeneration, AuditLog
from .schemas import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    PersonaCreate,
    PersonaUpdate,
    PersonaResponse,
    AIGenerateRequest,
    AIGenerateResponse,
    HealthCheckResponse
)

router = APIRouter()
security_bearer = HTTPBearer(auto_error=False)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> User:
    """Dependency to retrieve and validate authenticated user from JWT Bearer token."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token"
        )

    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )

    user_id = payload["sub"]
    user_dict = db_session.users.get(user_id)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return User(**user_dict)


# --- Authentication Routes ---

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate):
    """Register a new user."""
    # Check if user already exists
    for u in db_session.users.values():
        if u["email"].lower() == user_in.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    hashed_pwd = hash_password(user_in.password)
    new_user = User(
        id=user_id,
        email=user_in.email,
        hashed_password=hashed_pwd,
        full_name=user_in.full_name,
        role=user_in.role or "marketer"
    )
    db_session.users[user_id] = new_user.__dict__

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )


@router.post("/auth/login", response_model=Token)
def login_user(user_in: UserLogin):
    """Authenticate user and return JWT access token."""
    found_user = None
    for u in db_session.users.values():
        if u["email"].lower() == user_in.email.lower():
            found_user = u
            break

    if not found_user or not verify_password(user_in.password, found_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token({"sub": found_user["id"], "role": found_user["role"]})
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=found_user["id"],
        email=found_user["email"],
        role=found_user["role"]
    )


@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Fetch current authenticated user profile."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


# --- Persona Management Routes ---

@router.post("/personas", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(persona_in: PersonaCreate, current_user: User = Depends(get_current_user)):
    """Create a new buyer persona profile."""
    persona_id = f"per_{uuid.uuid4().hex[:12]}"
    persona = Persona(
        id=persona_id,
        user_id=current_user.id,
        name=persona_in.name,
        role=persona_in.role,
        company_size=persona_in.company_size,
        goals=persona_in.goals,
        challenges=persona_in.challenges,
        pain_points=persona_in.pain_points
    )
    db_session.personas[persona_id] = persona.__dict__
    return PersonaResponse(**persona.__dict__)


@router.get("/personas", response_model=List[PersonaResponse])
def list_personas(current_user: User = Depends(get_current_user)):
    """List all personas owned by current user."""
    user_personas = [
        p for p in db_session.personas.values()
        if p["user_id"] == current_user.id
    ]
    return [PersonaResponse(**p) for p in user_personas]


@router.get("/personas/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: str, current_user: User = Depends(get_current_user)):
    """Retrieve a specific persona profile."""
    persona_dict = db_session.personas.get(persona_id)
    if not persona_dict or persona_dict["user_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")
    return PersonaResponse(**persona_dict)


@router.put("/personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: str, persona_in: PersonaUpdate, current_user: User = Depends(get_current_user)):
    """Update a persona profile."""
    persona_dict = db_session.personas.get(persona_id)
    if not persona_dict or persona_dict["user_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")

    update_data = persona_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            persona_dict[key] = value
    persona_dict["updated_at"] = datetime.now(timezone.utc).isoformat()
    db_session.personas[persona_id] = persona_dict
    return PersonaResponse(**persona_dict)


@router.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: str, current_user: User = Depends(get_current_user)):
    """Delete a persona profile."""
    persona_dict = db_session.personas.get(persona_id)
    if not persona_dict or persona_dict["user_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")
    del db_session.personas[persona_id]
    return None


# --- AI Orchestration Routes ---

@router.post("/ai/generate", response_model=AIGenerateResponse)
def generate_content(req: AIGenerateRequest, current_user: User = Depends(get_current_user)):
    """Orchestrate AI call for personalized marketing content with Redis caching."""
    start_time = time.time()

    # Verify persona exists
    persona_dict = db_session.personas.get(req.persona_id)
    if not persona_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target persona not found")

    # Cache key based on persona, funnel stage, topic, and model
    cache_key = f"ai_gen:{req.persona_id}:{req.funnel_stage}:{req.target_format}:{hash(req.prompt_topic)}"
    cached_output = cache_client.get(cache_key)

    if cached_output:
        cached_data = json.loads(cached_output)
        cached_data["cached"] = True
        return AIGenerateResponse(**cached_data)

    # Simulated/Injected AI generation logic
    generated_text = (
        f"[{req.funnel_stage.upper()} STAGE - {req.target_format.upper()}]\n"
        f"Target Persona: {persona_dict['name']} ({persona_dict['role']})\n"
        f"Subject: {req.prompt_topic}\n\n"
        f"Dear {persona_dict['name']},\n"
        f"Are you struggling with {persona_dict['pain_points'][0] if persona_dict['pain_points'] else 'scaling marketing ROI'}? "
        f"PersonaScript streamlines content creation tailored specifically to {persona_dict['role']} needs. "
        f"Achieve your goal of {persona_dict['goals'][0] if persona_dict['goals'] else 'higher conversions'} effortlessly."
    )

    execution_time = int((time.time() - start_time) * 1000)
    gen_id = f"gen_{uuid.uuid4().hex[:12]}"

    response_payload = {
        "generation_id": gen_id,
        "persona_id": req.persona_id,
        "funnel_stage": req.funnel_stage,
        "model_used": req.preferred_model,
        "generated_content": generated_text,
        "cached": False,
        "token_count": len(generated_text.split()) * 2,
        "execution_time_ms": execution_time,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    # Store record in database
    db_session.generations[gen_id] = response_payload

    # Cache output in Redis with TTL of 3600s
    cache_client.set(cache_key, json.dumps(response_payload), ex=3600)

    return AIGenerateResponse(**response_payload)


# --- System Health Route ---

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Service health and connectivity status."""
    return HealthCheckResponse(
        status="healthy",
        version=settings.VERSION,
        database="connected (PostgreSQL/Mock)",
        cache="connected (Redis)" if cache_client.is_connected else "operating in fallback mode",
        ai_orchestration="ready"
    )
