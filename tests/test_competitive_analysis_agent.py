"""
Unit tests for PersonaScriptCompetitiveAnalysisAgent
"""

import pytest
from unittest.mock import Mock, patch
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
    return CompanyProfile(
        name="PersonaScript",
        value_proposition="Empowers B2B SaaS marketing teams to generate personalized, brand-aligned content at scale.",
        core_features=[
            "Dynamic Content Generation",
            "Brand Guideline Adherence Engine",
            "User Profile Personalization"
        ],
        target_audience="Growth-stage B2B SaaS marketing leaders and demand generation directors",
        current_positioning="AI content orchestration platform for B2B SaaS"
    )


@pytest.fixture
def sample_inputs(sample_company_profile):
    return AgentInputs(company_profile=sample_company_profile)


@pytest.fixture
def agent():
    return PersonaScriptCompetitiveAnalysisAgent()


def test_agent_initialization():
    agent = PersonaScriptCompetitiveAnalysisAgent(
        notion_token="test-notion-token",
        github_token="test-github-token",
        github_repo="owner/repo"
    )
    assert agent.notion_integration.token == "test-notion-token"
    assert agent.github_integration.token == "test-github-token"
    assert agent.github_integration.repo == "owner/repo"


def test_full_execution_success(agent, sample_inputs):
    outputs = agent.execute(sample_inputs)

    assert outputs.status == "success"
    assert outputs.notion_matrix_url
    assert outputs.github_issue_url
    assert outputs.unique_value_proposition

    # Verify Notion URL format
    notion_parsed = urlparse(outputs.notion_matrix_url)
    assert notion_parsed.scheme == "https"
    assert notion_parsed.netloc == "notion.so"

    # Verify Competitor Matrix
    matrix = outputs.competitor_matrix
    assert isinstance(matrix, CompetitorMatrix)
    assert len(matrix.competitors) >= 4
    assert len(matrix.market_gaps) >= 2
    assert len(matrix.personascript_differentiators) >= 3

    # Check that competitor names are present
    competitor_names = [c.name for c in matrix.competitors]
    assert "Jasper AI" in competitor_names
    assert "Copy.ai" in competitor_names
    assert "Writer.com" in competitor_names
    assert "HubSpot Content Assistant" in competitor_names

    # Check UVP content
    assert "PersonaScript" in outputs.unique_value_proposition
    assert "B2B SaaS" in outputs.unique_value_proposition


def test_competitor_details_extraction(agent):
    competitors = agent._identify_competitors()
    profiles = agent._extract_competitor_details(competitors)

    assert len(profiles) == len(competitors)
    for p in profiles:
        assert isinstance(p, CompetitorProfile)
        assert len(p.core_features) > 0
        assert p.pricing_model
        assert p.target_audience
        assert len(p.strengths) > 0
        assert len(p.weaknesses_and_pain_points) > 0


def test_uvp_formulation(agent, sample_company_profile):
    differentiators = ["Psychographic Persona Trigger Injection", "Automated Brand Guideline Adherence"]
    uvp = agent._formulate_uvp(sample_company_profile, differentiators)

    assert isinstance(uvp, str)
    assert len(uvp) > 50
    assert "growth-stage b2b saas" in uvp.lower()


def test_execution_handles_exceptions(agent, sample_inputs):
    with patch.object(agent, '_identify_competitors', side_effect=RuntimeError("Data fetch failed")):
        outputs = agent.execute(sample_inputs)

        assert outputs.status == "error"
        assert outputs.error_message == "Data fetch failed"
        assert outputs.notion_matrix_url == ""
        assert outputs.github_issue_url == ""
        assert outputs.unique_value_proposition == ""
