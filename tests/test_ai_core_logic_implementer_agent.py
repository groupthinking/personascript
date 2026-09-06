"""
Unit tests for AICoreLogicImplementerAgent.
"""

import os
import pytest
from urllib.parse import urlparse
from src.agents.ai_core_logic_implementer_agent import (
    AICoreLogicImplementerAgent,
    AICoreLogicInputs,
    AICoreLogicOutputs
)


@pytest.fixture
def sample_specs():
    """Create sample input specifications for testing."""
    return {
        "content_generation": {
            "formats": ["Case studies", "Landing pages"],
            "funnel_stages": ["Awareness", "Consideration"],
            "scalability": "High throughput design"
        },
        "tone_requirements": ["Friendly", "Empathetic"],
        "forbidden_elements": ["Spam words", "Competitor ABC"]
    }


@pytest.fixture
def sample_inputs(sample_specs):
    """Create sample inputs for testing."""
    return AICoreLogicInputs(
        task_specifications=sample_specs,
        brand_guidelines="Tone: Empathetic, friendly. Style: Active voice, clear terminology.",
        style_guides="No jargon. Max sentence length: 25 words.",
        openai_api_key="sk-test-openai",
        anthropic_api_key="sk-test-anthropic",
        pinecone_api_key="pc-test-pinecone",
        weaviate_api_key="wv-test-weaviate"
    )


def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = AICoreLogicImplementerAgent()
    assert agent is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with GitHub credentials."""
    agent = AICoreLogicImplementerAgent(
        github_token="gh_token",
        github_repo="owner/repo"
    )
    assert agent.github_integration.token == "gh_token"
    assert agent.github_integration.repo == "owner/repo"


def test_analyze_specifications(sample_inputs):
    """Test task specifications analysis."""
    agent = AICoreLogicImplementerAgent()
    requirements = agent._analyze_specifications(sample_inputs)

    assert "content_generation" in requirements
    assert "brand_guideline_enforcement" in requirements
    assert "personalization" in requirements

    # Assert that format overrides were respected
    assert "Case studies" in requirements["content_generation"]["formats"]
    assert "Friendly" in requirements["brand_guideline_enforcement"]["tone_requirements"]
    assert "Spam words" in requirements["brand_guideline_enforcement"]["forbidden_elements"]


def test_design_rag_architecture(sample_inputs):
    """Test RAG architecture design."""
    agent = AICoreLogicImplementerAgent()
    requirements = agent._analyze_specifications(sample_inputs)
    rag_design = agent._design_rag_architecture(requirements)

    assert "ingestion_pipeline" in rag_design
    assert "embedding_layer" in rag_design
    assert "retrieval_strategy" in rag_design
    assert "inference_engine" in rag_design

    assert rag_design["embedding_layer"]["dimension"] == 1536
    assert rag_design["retrieval_strategy"]["top_k"] == 5


def test_define_nlp_pipeline(sample_inputs):
    """Test NLP pipeline definition."""
    agent = AICoreLogicImplementerAgent()
    nlp_pipeline = agent._define_nlp_pipeline(sample_inputs)

    assert "pre_processing" in nlp_pipeline
    assert "analysis_and_scoring" in nlp_pipeline
    assert "post_processing_feedback_loop" in nlp_pipeline

    assert "tone_analyzer" in nlp_pipeline["analysis_and_scoring"]
    assert "style_checker" in nlp_pipeline["analysis_and_scoring"]
    assert "brand_adherence_guardrails" in nlp_pipeline["analysis_and_scoring"]


def test_outline_integration_strategy(sample_inputs):
    """Test LLM and vector database integration strategy."""
    agent = AICoreLogicImplementerAgent()
    strategy = agent._outline_integration_strategy(sample_inputs)

    assert "llm_providers" in strategy
    assert "vector_databases" in strategy

    assert strategy["llm_providers"]["openai"]["key_configured"] is True
    assert strategy["vector_databases"]["pinecone"]["key_configured"] is True
    assert strategy["vector_databases"]["weaviate"]["key_configured"] is True


def test_specify_env_setup():
    """Test development environment specification."""
    agent = AICoreLogicImplementerAgent()
    env = agent._specify_env_setup()

    assert "python_version" in env
    assert "core_frameworks" in env
    assert "key_packages" in env


def test_execute_and_generate_blueprint(sample_inputs):
    """Test full execute flow, ensuring file creation and GitHub integration."""
    agent = AICoreLogicImplementerAgent()

    # Ensure file does not exist before running
    blueprint_path = "AI_CORE_LOGIC_BLUEPRINT.md"
    if os.path.exists(blueprint_path):
        os.remove(blueprint_path)

    outputs = agent.execute(sample_inputs)

    assert outputs.blueprint_path == blueprint_path
    assert os.path.exists(blueprint_path)

    # Verify file content
    with open(blueprint_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "# PersonaScript: AI Core Logic Technical Blueprint" in content
    assert "Case studies" in content
    assert "Friendly" in content
    assert "Spam words" in content
    assert "text-embedding-3-small" in content
    assert "openai-python" in content

    # Verify GitHub issue URL
    assert outputs.github_issue_url
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "github.com"

    # Cleanup
    if os.path.exists(blueprint_path):
        os.remove(blueprint_path)


def test_create_issue_real_http_fallback(sample_inputs, monkeypatch):
    """Test GitHub Integration with configured credentials triggering mock fallback on status error."""
    agent = AICoreLogicImplementerAgent(
        github_token="invalid_test_token_causes_401",
        github_repo="groupthinking/personascript"
    )

    # When execute is run, it will try to make a POST call to github, fail with 401,
    # log error, and fall back to returning a mock issue URL.
    outputs = agent.execute(sample_inputs)

    assert outputs.github_issue_url
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "github.com"
    assert "groupthinking/personascript" in parsed.path

    # Cleanup
    blueprint_path = "AI_CORE_LOGIC_BLUEPRINT.md"
    if os.path.exists(blueprint_path):
        os.remove(blueprint_path)
