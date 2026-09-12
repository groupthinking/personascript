"""
Unit tests for CICDPipelineArchitectAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.cicd_pipeline_architect_agent import (
    CICDPipelineArchitectAgent,
    CICDInputs,
    CICDOutputs
)


@pytest.fixture
def sample_cicd_inputs():
    """Create sample input data for testing the CI/CD agent."""
    return CICDInputs(
        business_context="PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate hyper-personalized content.",
        task_to_automate="Implement CI/CD pipelines for automated testing, building, and deployment",
        target_platform="GitHub Actions"
    )


@pytest.fixture
def agent():
    """Create a CICDPipelineArchitectAgent instance for testing."""
    return CICDPipelineArchitectAgent()


def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = CICDPipelineArchitectAgent()
    assert agent is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with GitHub credentials."""
    agent = CICDPipelineArchitectAgent(
        github_token="test_token_123",
        github_repo="owner/repo"
    )
    assert agent.github_integration.token == "test_token_123"
    assert agent.github_integration.repo == "owner/repo"


def test_parse_scope(agent, sample_cicd_inputs):
    """Test scope parsing of the input task."""
    scope = agent._parse_scope(sample_cicd_inputs)
    assert "services" in scope
    assert "stages" in scope
    assert "target_platform" in scope
    assert "frontend" in scope["services"]
    assert "backend" in scope["services"]
    assert "ai_services" in scope["services"]


def test_formulate_architecture(agent, sample_cicd_inputs):
    """Test formulating the high-level architecture."""
    scope = agent._parse_scope(sample_cicd_inputs)
    architecture = agent._formulate_architecture(sample_cicd_inputs, scope)
    assert "High-Level CI/CD Architecture" in architecture
    assert "Frontend CI/CD Pipeline" in architecture
    assert "Backend CI/CD Pipeline" in architecture
    assert "AI/ML Service CI/CD Pipeline" in architecture


def test_draft_yamls(agent):
    """Test drafting GitHub Actions YAML configurations for all service types."""
    frontend_yaml = agent._draft_frontend_yaml()
    backend_yaml = agent._draft_backend_yaml()
    ai_service_yaml = agent._draft_ai_service_yaml()

    assert "name: Frontend CI/CD" in frontend_yaml
    assert "name: Backend CI/CD" in backend_yaml
    assert "name: AI Service CI/CD" in ai_service_yaml

    # Check key jobs & steps
    assert "actions/checkout" in frontend_yaml
    assert "actions/setup-node" in frontend_yaml
    assert "aws s3 sync" in frontend_yaml

    assert "ruff check" in backend_yaml
    assert "pytest" in backend_yaml
    assert "docker/build-push-action" in backend_yaml

    assert "validate_model.py" in ai_service_yaml
    assert "sagemaker" in ai_service_yaml


def test_consolidate_blueprint(agent, sample_cicd_inputs):
    """Test consolidation of high-level architecture and YAML configurations."""
    scope = agent._parse_scope(sample_cicd_inputs)
    architecture = agent._formulate_architecture(sample_cicd_inputs, scope)
    frontend_yaml = agent._draft_frontend_yaml()
    backend_yaml = agent._draft_backend_yaml()
    ai_service_yaml = agent._draft_ai_service_yaml()

    blueprint = agent._consolidate_blueprint(
        sample_cicd_inputs, architecture, frontend_yaml, backend_yaml, ai_service_yaml
    )

    assert "PersonaScript CI/CD Blueprint Document" in blueprint
    assert "Frontend Workflow" in blueprint
    assert "Backend Workflow" in blueprint
    assert "AI Service Workflow" in blueprint
    assert "PRODUCTION_API_URL" in blueprint


def test_create_github_issue(agent, sample_cicd_inputs):
    """Test simulated GitHub issue creation."""
    blueprint = "Dummy blueprint content"
    github_url = agent._create_github_issue(sample_cicd_inputs, blueprint)

    assert github_url
    parsed = urlparse(github_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")
    assert "issues" in parsed.path.split("/")


def test_full_execution(agent, sample_cicd_inputs):
    """Test full agent execution pipeline."""
    outputs = agent.execute(sample_cicd_inputs)

    assert isinstance(outputs, CICDOutputs)
    assert outputs.high_level_architecture
    assert outputs.frontend_yaml
    assert outputs.backend_yaml
    assert outputs.ai_service_yaml
    assert outputs.consolidated_blueprint
    assert outputs.github_issue_url

    # Verify consolidated blueprint has components
    assert "Frontend Workflow" in outputs.consolidated_blueprint
    assert "Backend Workflow" in outputs.consolidated_blueprint
    assert "AI Service Workflow" in outputs.consolidated_blueprint

    # Validate GitHub URL structure
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")
    assert "issues" in parsed.path.split("/")
