"""
Unit tests for PersonaScriptCompetitiveAnalysisAgent.
"""

import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse
from src.agents.competitive_analysis_agent import (
    PersonaScriptCompetitiveAnalysisAgent,
    CompanyProfile,
    CompetitorProfile,
    CompetitorMatrix,
    AgentInputs,
    AgentOutputs
)


@pytest.fixture
def sample_company_profile():
    """Create sample company profile for PersonaScript."""
    return CompanyProfile(
        name="PersonaScript",
        value_proposition="Empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume content.",
        core_features=["AI content generation", "Brand alignment", "Persona targeting"],
        target_audience="B2B SaaS marketers",
        current_positioning="Hyper-personalized content automation based on user research."
    )


@pytest.fixture
def sample_inputs(sample_company_profile):
    """Create sample inputs for testing."""
    return AgentInputs(
        personascript_profile=sample_company_profile,
        ahrefs_api_key="test_ahrefs",
        crunchbase_api_key="test_crunchbase",
        capterra_api_key="test_capterra",
        notion_api_key="test_notion",
        notion_database_id="test_db",
        github_token="test_github",
        github_repo="owner/repo"
    )


@pytest.fixture
def agent():
    """Create an agent instance for testing."""
    return PersonaScriptCompetitiveAnalysisAgent()


def test_agent_initialization():
    """Test that agent initializes with default mock values."""
    agent = PersonaScriptCompetitiveAnalysisAgent()
    assert agent is not None
    assert agent.notion_integration is not None
    assert agent.github_integration is not None
    assert len(agent.competitors) == 0


def test_agent_with_credentials():
    """Test agent initialization with custom credentials."""
    agent = PersonaScriptCompetitiveAnalysisAgent(
        notion_api_key="test_notion_key",
        notion_database_id="test_notion_db",
        github_token="test_github_token",
        github_repo="test/repo"
    )
    assert agent.notion_integration.api_key == "test_notion_key"
    assert agent.notion_integration.database_id == "test_notion_db"
    assert agent.github_integration.token == "test_github_token"
    assert agent.github_integration.repo == "test/repo"


def test_identify_competitors(agent, sample_inputs):
    """Test step 1 of the agent workflow: identifying competitors."""
    competitors = agent._identify_competitors(sample_inputs)
    assert len(competitors) > 0
    assert "Jasper AI" in competitors
    assert "Copy.ai" in competitors


def test_extract_competitor_details(agent, sample_inputs):
    """Test step 2 of the agent workflow: extracting competitor details."""
    competitors = agent._identify_competitors(sample_inputs)
    details = agent._extract_competitor_details(competitors, sample_inputs)

    assert len(details) == len(competitors)
    for detail in details:
        assert isinstance(detail, CompetitorProfile)
        assert detail.name in competitors
        assert len(detail.core_features) > 0
        assert detail.pricing_model
        assert detail.target_audience
        assert len(detail.reported_strengths) > 0
        assert len(detail.common_pain_points) > 0


def test_analyze_matrix_gaps(agent, sample_company_profile):
    """Test step 4: gap analysis."""
    # Build a simple matrix
    comp_profile = CompetitorProfile(
        name="Jasper AI",
        core_features=["Features"],
        pricing_model="Pricing",
        target_audience="Audience",
        reported_strengths=["Strengths"],
        common_pain_points=["Pain Points"]
    )
    matrix = CompetitorMatrix(
        title="Test Matrix",
        competitors=[comp_profile],
        dimensions_compared=["Pricing"]
    )

    analysis = agent._analyze_matrix_gaps(matrix, sample_company_profile)
    assert "gaps_identified" in analysis
    assert "persona_script_differentiators" in analysis
    assert len(analysis["gaps_identified"]) > 0
    assert len(analysis["persona_script_differentiators"]) > 0


def test_formulate_uvp(agent, sample_company_profile):
    """Test step 5: UVP formulation."""
    analysis = {
        "gaps_identified": ["Gap 1"],
        "persona_script_differentiators": ["Diff 1"]
    }
    uvp = agent._formulate_uvp(analysis, sample_company_profile)
    assert uvp
    assert "PersonaScript" in uvp
    assert "B2B SaaS" in uvp


def test_compose_issue_body(agent, sample_inputs):
    """Test issue body formatting."""
    comp_profile = CompetitorProfile(
        name="Jasper AI",
        core_features=["Features"],
        pricing_model="Pricing",
        target_audience="Audience",
        reported_strengths=["Strengths"],
        common_pain_points=["Pain Points"]
    )
    matrix = CompetitorMatrix(
        title="Test Matrix",
        competitors=[comp_profile],
        dimensions_compared=["Pricing"]
    )
    analysis = {
        "gaps_identified": ["Gap 1"],
        "persona_script_differentiators": ["Diff 1"]
    }
    body = agent._compose_issue_body(
        competitor_matrix_url="https://notion.so/test",
        uvp="Test UVP",
        matrix=matrix,
        analysis_results=analysis,
        inputs=sample_inputs
    )

    assert body
    assert "PersonaScript Competitive Analysis & UVP Draft" in body
    assert "Jasper AI" in body
    assert "Test UVP" in body
    assert "Notion Competitor Matrix" in body


@patch("src.integrations.notion_integration.requests.post")
def test_full_execution(mock_post, sample_company_profile):
    """Test full agent execution pipeline with mocked requests to Notion API."""
    # Set up mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_post.return_value = mock_resp

    agent_with_creds = PersonaScriptCompetitiveAnalysisAgent(
        notion_api_key="test_notion_key",
        notion_database_id="test_notion_db",
        github_token="test_github_token",
        github_repo="owner/repo"
    )

    inputs_with_creds = AgentInputs(
        personascript_profile=sample_company_profile,
        ahrefs_api_key="test_ahrefs",
        crunchbase_api_key="test_crunchbase",
        capterra_api_key="test_capterra",
        notion_api_key="test_notion_key",
        notion_database_id="test_notion_db",
        github_token="test_github_token",
        github_repo="owner/repo"
    )

    outputs = agent_with_creds.execute(inputs_with_creds)

    assert isinstance(outputs, AgentOutputs)
    assert outputs.competitor_matrix_url == "https://notion.so/test_notion_db"
    assert outputs.unique_value_proposition
    assert outputs.github_issue_url
    assert isinstance(outputs.competitor_matrix, CompetitorMatrix)

    # Assert that mock_post was called for each competitor (there are 4 competitors)
    assert mock_post.call_count == 4

    # Check that URLs are properly formatted
    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc.endswith("github.com")
    assert "issues" in github_parsed.path.split("/")

    # Check that competitors were retrieved and saved
    assert len(agent_with_creds.competitors) > 0
    assert len(outputs.competitor_matrix.competitors) == len(agent_with_creds.competitors)


@patch("src.integrations.notion_integration.requests.post")
def test_notion_integration_failure_fallback(mock_post, agent):
    """Test that Notion integration falls back to mock URL gracefully on API error."""
    mock_post.side_effect = Exception("API connection error")

    notion_int = agent.notion_integration
    notion_int.api_key = "test_key"
    notion_int.database_id = "test_db"

    url = notion_int.create_competitor_matrix({
        "title": "Failure Test",
        "competitors": [{"name": "Jasper AI", "features": ["Templates"]}]
    })

    assert "mock-notion-" in url
