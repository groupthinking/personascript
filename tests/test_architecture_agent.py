"""
Unit tests for PersonaScriptArchitectureAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.architecture_agent import (
    PersonaScriptArchitectureAgent,
    ArchitectureAgentInputs,
    AIModelEvaluation,
    ArchitectureComponent,
    SecurityProtocol,
    ComplianceSection
)


@pytest.fixture
def sample_inputs():
    """Create sample inputs for PersonaScriptArchitectureAgent testing."""
    return ArchitectureAgentInputs(
        business_requirements="PersonaScript needs high-volume, hyper-personalized, and brand-aligned content generation with strict GDPR security compliance.",
        value_proposition="Empowers growth-stage B2B SaaS teams to scale brand-consistent copy production.",
        existing_infrastructure="None",
        compliance_standards=["GDPR", "SOC 2 Type II"]
    )


@pytest.fixture
def agent():
    """Create an agent instance for testing."""
    return PersonaScriptArchitectureAgent()


def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = PersonaScriptArchitectureAgent()
    assert agent is not None
    assert agent.miro_integration is not None
    assert agent.google_docs_integration is not None
    assert agent.github_integration is not None
    assert len(agent.model_evaluations) == 0
    assert len(agent.architecture_components) == 0
    assert len(agent.security_protocols) == 0
    assert len(agent.compliance_plan) == 0


def test_agent_with_credentials():
    """Test agent initialization with credentials."""
    agent = PersonaScriptArchitectureAgent(
        miro_api_key="test_key",
        google_docs_credentials={"type": "service_account"},
        github_token="test_token",
        github_repo="owner/repo"
    )
    assert agent.miro_integration.api_key == "test_key"
    assert agent.google_docs_integration.credentials is not None
    assert agent.github_integration.token == "test_token"
    assert agent.github_integration.repo == "owner/repo"


def test_parse_requirements_and_valprop(agent, sample_inputs):
    """Test requirements and value proposition parsing."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    assert "functional_needs" in context
    assert "non_functional_needs" in context

    # Check that functional needs were identified
    assert len(context["functional_needs"]) > 0
    assert any("personal" in need.lower() for need in context["functional_needs"])
    assert any("volume" in need.lower() for need in context["functional_needs"])
    assert any("brand" in need.lower() for need in context["functional_needs"])


def test_evaluate_ai_models(agent, sample_inputs):
    """Test AI model evaluation logic."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)

    assert len(evals) > 0
    assert all(isinstance(e, AIModelEvaluation) for e in evals)
    assert any("GPT-4o" in e.model_name for e in evals)
    assert any("Claude 3.5 Sonnet" in e.model_name for e in evals)
    assert any("Llama 3" in e.model_name for e in evals)

    for e in evals:
        assert e.model_name
        assert e.type
        assert len(e.strengths) > 0
        assert len(e.weaknesses) > 0
        assert e.estimated_cost
        assert e.performance_rating
        assert e.suitability
        assert e.role_in_platform


def test_design_aws_architecture(agent, sample_inputs):
    """Test AWS architecture design component output."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)
    components = agent._design_aws_architecture(evals)

    assert len(components) > 0
    assert all(isinstance(c, ArchitectureComponent) for c in components)

    # Check for expected AWS services in design
    component_names = [c.name for c in components]
    assert any("ECS" in name for name in component_names)
    assert any("S3" in name for name in component_names)
    assert any("RDS" in name for name in component_names)
    assert any("DynamoDB" in name for name in component_names)
    assert any("KMS" in name or "Secrets" in name for name in component_names)

    for c in components:
        assert c.name
        assert c.category
        assert c.description
        assert len(c.key_features) > 0


def test_develop_security_protocols(agent, sample_inputs):
    """Test security protocol development."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)
    components = agent._design_aws_architecture(evals)
    protocols = agent._develop_security_protocols(components)

    assert len(protocols) > 0
    assert all(isinstance(p, SecurityProtocol) for p in protocols)

    domains = [p.domain for p in protocols]
    assert "Data Encryption" in domains
    assert "Access Control" in domains
    assert "Data Retention" in domains
    assert "Secure API Integration" in domains

    for p in protocols:
        assert p.name
        assert p.domain
        assert p.description
        assert len(p.guidelines) > 0


def test_outline_compliance_plan(agent, sample_inputs):
    """Test outline compliance plan matching standards."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)
    components = agent._design_aws_architecture(evals)
    protocols = agent._develop_security_protocols(components)

    plan = agent._outline_compliance_plan(protocols, sample_inputs.compliance_standards)

    assert len(plan) == 2
    assert all(isinstance(sec, ComplianceSection) for sec in plan)

    standards = [sec.standard for sec in plan]
    assert any("GDPR" in std for std in standards)
    assert any("SOC 2" in std for std in standards)

    for sec in plan:
        assert sec.standard
        assert sec.description
        assert len(sec.mapped_protocols) > 0
        assert len(sec.controls) > 0


def test_create_miro_board(agent, sample_inputs):
    """Test Miro board creation URL."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)
    components = agent._design_aws_architecture(evals)
    protocols = agent._develop_security_protocols(components)

    url = agent._create_miro_board(evals, components, protocols)
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("miro.com")


def test_create_compliance_document(agent, sample_inputs):
    """Test Google Doc compliance report creation."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    evals = agent._evaluate_ai_models(context)
    components = agent._design_aws_architecture(evals)
    protocols = agent._develop_security_protocols(components)
    plan = agent._outline_compliance_plan(protocols, sample_inputs.compliance_standards)

    url = agent._create_compliance_document(plan, protocols)
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("docs.google.com")


def test_create_github_issue(agent, sample_inputs):
    """Test Github issue publication URL."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    agent.model_evaluations = agent._evaluate_ai_models(context)
    agent.architecture_components = agent._design_aws_architecture(agent.model_evaluations)
    agent.security_protocols = agent._develop_security_protocols(agent.architecture_components)
    agent.compliance_plan = agent._outline_compliance_plan(agent.security_protocols, sample_inputs.compliance_standards)

    miro_url = "https://miro.com/app/board/mock-tech/"
    doc_url = "https://docs.google.com/document/d/mock-sec/edit"

    url = agent._create_github_issue(miro_url, doc_url, sample_inputs)
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")
    assert "issues" in parsed.path.split("/")


def test_full_execution(agent, sample_inputs):
    """Test full agent execute pipeline."""
    outputs = agent.execute(sample_inputs)

    # Check outputs exist and are structured correctly
    assert outputs.miro_board_url
    assert outputs.compliance_document_url
    assert outputs.github_issue_url
    assert len(outputs.model_evaluations) == 3
    assert len(outputs.architecture_components) == 9
    assert len(outputs.security_protocols) == 4
    assert len(outputs.compliance_plan) == 2

    # Verify outputs are valid URLs
    miro_parsed = urlparse(outputs.miro_board_url)
    assert miro_parsed.scheme == "https"
    assert miro_parsed.netloc.endswith("miro.com")

    doc_parsed = urlparse(outputs.compliance_document_url)
    assert doc_parsed.scheme == "https"
    assert doc_parsed.netloc.endswith("docs.google.com")

    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc.endswith("github.com")
    assert "issues" in github_parsed.path.split("/")

    # Check state was stored internally
    assert len(agent.model_evaluations) == len(outputs.model_evaluations)
    assert len(agent.architecture_components) == len(outputs.architecture_components)
    assert len(agent.security_protocols) == len(outputs.security_protocols)
    assert len(agent.compliance_plan) == len(outputs.compliance_plan)


def test_compose_issue_content(agent, sample_inputs):
    """Test the detailed markdown composition content for Github issues."""
    context = agent._parse_requirements_and_valprop(sample_inputs)
    agent.model_evaluations = agent._evaluate_ai_models(context)
    agent.architecture_components = agent._design_aws_architecture(agent.model_evaluations)
    agent.security_protocols = agent._develop_security_protocols(agent.architecture_components)
    agent.compliance_plan = agent._outline_compliance_plan(agent.security_protocols, sample_inputs.compliance_standards)

    miro_url = "https://miro.com/app/board/mock-tech/"
    doc_url = "https://docs.google.com/document/d/mock-sec/edit"

    content = agent._compose_issue_content(miro_url, doc_url, sample_inputs)

    assert "# PersonaScript Architecture & Security Design Completed" in content
    assert "Optimal AI Model Selections" in content
    assert "High-Level AWS Infrastructure" in content
    assert "Core Data Security Protocols" in content
    assert "Workflow Execution Log" in content
    assert "GDPR (General Data Protection Regulation)" in content
    assert "SOC 2 Type II Certification" in content
    assert miro_url in content
    assert doc_url in content
