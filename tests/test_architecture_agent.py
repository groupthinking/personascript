"""
Unit tests for PersonaScriptArchitectureAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.architecture_agent import (
    PersonaScriptArchitectureAgent,
    ArchitectureInputs,
    ArchitectureOutputs
)


@pytest.fixture
def sample_inputs():
    """Sample inputs for testing the ArchitectureAgent."""
    return ArchitectureInputs(
        business_requirements=(
            "High-volume, hyper-personalized B2B content generation platform requiring brand voice adherence, "
            "sub-15s response times, 99.9% availability, and strict multi-tenant isolation."
        ),
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
            "high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages."
        ),
        existing_infrastructure="AWS Cloud Infrastructure with Kubernetes (EKS)",
        compliance_standards=["GDPR", "SOC 2 Type II"]
    )


@pytest.fixture
def agent():
    """Default agent fixture."""
    return PersonaScriptArchitectureAgent()


def test_agent_initialization():
    """Test agent initialization and integration setup."""
    agent_instance = PersonaScriptArchitectureAgent()
    assert agent_instance is not None
    assert agent_instance.miro_integration is not None
    assert agent_instance.google_docs_integration is not None
    assert agent_instance.github_integration is not None
    assert len(agent_instance.execution_log) == 0


def test_agent_initialization_with_credentials():
    """Test initialization when explicit API keys/tokens are provided."""
    agent_instance = PersonaScriptArchitectureAgent(
        miro_api_key="miro_test_key",
        google_docs_credentials={"type": "service_account"},
        github_token="gh_test_token",
        github_repo="owner/test-repo"
    )
    assert agent_instance.miro_integration.api_key == "miro_test_key"
    assert agent_instance.google_docs_integration.credentials == {"type": "service_account"}
    assert agent_instance.github_integration.token == "gh_test_token"
    assert agent_instance.github_integration.repo == "owner/test-repo"


def test_parse_requirements(agent, sample_inputs):
    """Test Step 1 requirement parsing helper."""
    parsed = agent._parse_requirements(sample_inputs)
    assert "functional_requirements" in parsed
    assert "non_functional_requirements" in parsed
    assert len(parsed["functional_requirements"]) > 0
    assert parsed["non_functional_requirements"]["scalability"]


def test_evaluate_ai_models(agent, sample_inputs):
    """Test Step 2 AI model evaluation helper."""
    parsed = agent._parse_requirements(sample_inputs)
    models = agent._evaluate_ai_models(parsed)
    assert len(models) == 3
    model_names = [m["model_name"] for m in models]
    assert any("Claude 3.5 Sonnet" in m for m in model_names)
    assert any("GPT-4o" in m for m in model_names)
    assert any("Llama-3" in m for m in model_names)


def test_design_aws_architecture(agent, sample_inputs):
    """Test Step 3 AWS architecture design helper."""
    parsed = agent._parse_requirements(sample_inputs)
    models = agent._evaluate_ai_models(parsed)
    arch = agent._design_aws_architecture(parsed, models)

    assert "tier_1_edge_networking" in arch
    assert "tier_2_api_compute" in arch
    assert "tier_3_ai_orchestration" in arch
    assert "tier_4_data_caching_queues" in arch
    assert "tier_5_storage_database" in arch
    assert "tier_6_security_observability" in arch


def test_develop_security_protocols(agent):
    """Test Step 4 security protocols helper."""
    protocols = agent._develop_security_protocols()
    assert "encryption_strategy" in protocols
    assert "access_control" in protocols
    assert "data_retention_and_privacy" in protocols
    assert "AES-256" in protocols["encryption_strategy"]["data_at_rest"]
    assert "TLS 1.3" in protocols["encryption_strategy"]["data_in_transit"]


def test_outline_compliance_plan(agent):
    """Test Step 5 compliance plan helper."""
    protocols = agent._develop_security_protocols()
    plan = agent._outline_compliance_plan(["GDPR", "SOC 2 Type II"], protocols)
    assert "gdpr_compliance" in plan
    assert "soc2_compliance" in plan
    assert "implementation_roadmap" in plan
    assert len(plan["implementation_roadmap"]) == 4


def test_create_miro_diagram(agent, sample_inputs):
    """Test Step 6 Miro diagram creation helper."""
    parsed = agent._parse_requirements(sample_inputs)
    models = agent._evaluate_ai_models(parsed)
    arch = agent._design_aws_architecture(parsed, models)
    protocols = agent._develop_security_protocols()

    url = agent._create_miro_diagram(arch, models, protocols)
    assert url
    parsed_url = urlparse(url)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "miro.com"


def test_generate_compliance_doc(agent):
    """Test Step 7 Google Docs compliance plan generation helper."""
    protocols = agent._develop_security_protocols()
    plan = agent._outline_compliance_plan(["GDPR", "SOC 2 Type II"], protocols)

    url = agent._generate_compliance_doc(plan, protocols)
    assert url
    parsed_url = urlparse(url)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "docs.google.com"


def test_full_agent_execution(agent, sample_inputs):
    """Test full 8-step end-to-end execution of PersonaScriptArchitectureAgent."""
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, ArchitectureOutputs)
    assert outputs.status == "success"
    assert outputs.miro_diagram_url
    assert outputs.security_plan_doc_url
    assert outputs.github_issue_url
    assert len(outputs.selected_ai_models) == 3
    assert len(outputs.system_architecture_summary) == 6
    assert "gdpr_compliance" in outputs.security_compliance_summary

    # Validate URLs
    assert urlparse(outputs.miro_diagram_url).netloc == "miro.com"
    assert urlparse(outputs.security_plan_doc_url).netloc == "docs.google.com"
    assert urlparse(outputs.github_issue_url).netloc == "github.com"

    # Validate execution log step tracking
    assert len(agent.execution_log) == 16  # 8 steps * 2 (started & completed)
    steps_logged = set(log["step"] for log in agent.execution_log)
    assert steps_logged == set(range(1, 9))


def test_agent_execution_handles_exceptions_gracefully(agent):
    """Test exception handling during agent execution when invalid input is provided."""
    outputs = agent.execute(None)

    assert outputs.status == "error"
    assert outputs.error_message is not None
    assert outputs.miro_diagram_url == ""
    assert outputs.security_plan_doc_url == ""
    assert outputs.github_issue_url == ""
