"""
Unit Tests for PersonaScriptBackendAPIDevelopmentAgent and Backend API Codebase.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.agents.backend_api_development_agent import (
    PersonaScriptBackendAPIDevelopmentAgent,
    BackendAPIInputs,
    BackendAPIOutputs
)
from src.backend.app.main import app
from src.backend.app.security import hash_password, verify_password, create_access_token, decode_access_token
from src.backend.app.database import db_session, cache_client, RedisCacheClient


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db_and_cache():
    """Reset database session and cache before each test."""
    db_session.clear()
    cache_client.flush_all()


def test_agent_initialization():
    """Test initializing PersonaScriptBackendAPIDevelopmentAgent."""
    agent = PersonaScriptBackendAPIDevelopmentAgent()
    assert agent is not None
    assert agent.github_integration is not None


def test_agent_execution_workflow():
    """Test full execution of PersonaScriptBackendAPIDevelopmentAgent."""
    agent = PersonaScriptBackendAPIDevelopmentAgent()
    inputs = BackendAPIInputs()

    outputs = agent.execute(inputs)
    assert outputs.status == "success"
    assert outputs.codebase_dir == "src/backend/app"
    assert outputs.schema_path == "src/backend/migrations/schema.sql"
    assert outputs.redis_config_path == "src/backend/redis.conf"
    assert outputs.docker_compose_path == "docker-compose.yml"
    assert outputs.openapi_spec_path == "src/backend/docs/openapi.json"
    assert outputs.github_issue_url != ""


def test_security_utilities():
    """Test password hashing, verification, and JWT creation/decoding."""
    password = "SecretPassword123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

    payload = {"sub": "usr_12345", "role": "marketer"}
    token = create_access_token(payload)
    assert isinstance(token, str)

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "usr_12345"
    assert decoded["role"] == "marketer"


def test_redis_cache_client():
    """Test RedisCacheClient set, get, delete, and flush operations."""
    client = RedisCacheClient()
    client.set("test_key", "test_value", ex=60)
    assert client.get("test_key") == "test_value"

    client.delete("test_key")
    assert client.get("test_key") is None


def test_fastapi_health_endpoint():
    """Test GET /api/v1/health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "cache" in data


def test_fastapi_auth_workflow():
    """Test registration, login, and protected /auth/me endpoint."""
    # 1. Register User
    reg_payload = {
        "email": "sarah.cmo@example.com",
        "password": "Password123!",
        "full_name": "Sarah CMO",
        "role": "marketer"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "sarah.cmo@example.com"
    assert "id" in user_data

    # 2. Login User
    login_payload = {
        "email": "sarah.cmo@example.com",
        "password": "Password123!"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 3. Access Protected /auth/me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "sarah.cmo@example.com"


def test_fastapi_personas_crud_and_ai_generation():
    """Test Personas CRUD operations and AI content generation with caching."""
    # Register & Login
    client.post("/api/v1/auth/register", json={
        "email": "alex.content@example.com",
        "password": "Password123!",
        "full_name": "Alex Content"
    })
    login_res = client.post("/api/v1/auth/login", json={
        "email": "alex.content@example.com",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Persona
    persona_payload = {
        "name": "Demand Gen Director Sarah",
        "role": "Director of Demand Generation",
        "company_size": "50-500",
        "goals": ["Scale leads"],
        "challenges": ["Brand alignment"],
        "pain_points": ["Generic content"]
    }
    create_res = client.post("/api/v1/personas", json=persona_payload, headers=headers)
    assert create_res.status_code == 201
    persona = create_res.json()
    persona_id = persona["id"]

    # 2. Get Persona
    get_res = client.get(f"/api/v1/personas/{persona_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Demand Gen Director Sarah"

    # 3. AI Generate Content
    gen_payload = {
        "persona_id": persona_id,
        "funnel_stage": "Awareness",
        "prompt_topic": "AI Content Automation for CMOs",
        "preferred_model": "gpt-4o",
        "target_format": "email"
    }
    gen_res1 = client.post("/api/v1/ai/generate", json=gen_payload, headers=headers)
    assert gen_res1.status_code == 200
    data1 = gen_res1.json()
    assert data1["cached"] is False
    assert "Demand Gen Director Sarah" in data1["generated_content"]

    # 4. Test Redis Caching (second request should return cached = True)
    gen_res2 = client.post("/api/v1/ai/generate", json=gen_payload, headers=headers)
    assert gen_res2.status_code == 200
    data2 = gen_res2.json()
    assert data2["cached"] is True


def test_deliverable_files_exist():
    """Verify presence and validity of generated deliverable files."""
    assert os.path.exists("src/backend/app/main.py")
    assert os.path.exists("src/backend/migrations/schema.sql")
    assert os.path.exists("src/backend/redis.conf")
    assert os.path.exists("Dockerfile.backend")
    assert os.path.exists("Dockerfile.postgres")
    assert os.path.exists("Dockerfile.redis")
    assert os.path.exists("docker-compose.yml")
    assert os.path.exists("src/backend/docs/openapi.json")

    with open("src/backend/docs/openapi.json") as f:
        doc = json.load(f)
        assert doc["openapi"] == "3.0.3"
        assert "/api/v1/auth/register" in doc["paths"]
