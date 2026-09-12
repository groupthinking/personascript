"""
Unit tests for PersonaScriptMVPDevelopmentRoadmapAgent.
"""

import pytest
from urllib.parse import urlparse

from src.agents.mvp_roadmap_agent import (
    PersonaScriptMVPDevelopmentRoadmapAgent,
    RoadmapInputs,
    RoadmapOutputs,
    Epic,
    Feature,
    Milestone,
    UserStory
)


@pytest.fixture
def default_agent():
    """Fixture to provide a default agent instance."""
    return PersonaScriptMVPDevelopmentRoadmapAgent()


@pytest.fixture
def custom_inputs():
    """Fixture to provide custom RoadmapInputs."""
    return RoadmapInputs(
        company_name="PersonaScript",
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
            "high-volume, hyper-personalized, and brand-aligned content across all sales funnel "
            "stages, dramatically accelerating lead conversion and brand consistency."
        ),
        timeframe="3-6 months",
        target_platform="Linear"
    )


def test_agent_initialization(default_agent):
    """Test basic agent initialization."""
    assert default_agent is not None
    assert default_agent.github_integration is not None
    assert default_agent.linear_integration is not None


def test_agent_initialization_with_credentials():
    """Test agent initialization with explicit API credentials."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent(
        github_token="ghp_test_token_12345",
        github_repo="groupthinking/personascript",
        linear_token="lin_api_key_67890"
    )
    assert agent.github_integration.token == "ghp_test_token_12345"
    assert agent.github_integration.repo == "groupthinking/personascript"
    assert agent.linear_integration.token == "lin_api_key_67890"


def test_parse_context(default_agent, custom_inputs):
    """Test parsing context from RoadmapInputs."""
    parsed = default_agent._parse_context(custom_inputs)
    assert parsed["company_name"] == "PersonaScript"
    assert "hyper-personalized" in parsed["value_proposition"]
    assert parsed["timeframe"] == "3-6 months"
    assert parsed["target_platform"] == "Linear"


def test_access_internal_documentation(default_agent, custom_inputs):
    """Test accessing internal strategy and pain point documentation."""
    parsed = default_agent._parse_context(custom_inputs)
    docs = default_agent._access_internal_documentation(parsed)
    assert "customer_pain_points" in docs
    assert len(docs["customer_pain_points"]) > 0
    assert "product_pillars" in docs
    assert len(docs["product_pillars"]) > 0


def test_synthesize_strategic_themes(default_agent, custom_inputs):
    """Test synthesis of strategic themes."""
    parsed = default_agent._parse_context(custom_inputs)
    docs = default_agent._access_internal_documentation(parsed)
    themes = default_agent._synthesize_strategic_themes(parsed, docs)

    assert len(themes) == 4
    theme_titles = [t["title"] for t in themes]
    assert "Dynamic Content Orchestration Engine" in theme_titles
    assert "Brand Voice Guardrails & Style Compliance" in theme_titles


def test_generate_and_prioritize_features(default_agent, custom_inputs):
    """Test feature generation and Epic organization."""
    parsed = default_agent._parse_context(custom_inputs)
    docs = default_agent._access_internal_documentation(parsed)
    themes = default_agent._synthesize_strategic_themes(parsed, docs)
    epics = default_agent._generate_and_prioritize_features(themes)

    assert len(epics) == 4
    assert all(isinstance(e, Epic) for e in epics)

    # Verify Epic 1 details
    epic1 = epics[0]
    assert epic1.id == "EPIC-1"
    assert len(epic1.features) >= 2
    assert epic1.features[0].priority in ["Critical", "High", "Medium"]
    assert len(epic1.features[0].user_stories) > 0


def test_define_milestones(default_agent):
    """Test milestone definitions for 3-6 month timeframe."""
    milestones = default_agent._define_milestones("3-6 months")
    assert len(milestones) == 3
    assert all(isinstance(m, Milestone) for m in milestones)
    assert "Milestone 1" in milestones[0].name
    assert "Months 1 - 2" in milestones[0].timeframe


def test_draft_roadmap_markdown(default_agent, custom_inputs):
    """Test drafting of Linear-structured roadmap Markdown."""
    parsed = default_agent._parse_context(custom_inputs)
    docs = default_agent._access_internal_documentation(parsed)
    themes = default_agent._synthesize_strategic_themes(parsed, docs)
    epics = default_agent._generate_and_prioritize_features(themes)
    milestones = default_agent._define_milestones(custom_inputs.timeframe)

    md = default_agent._draft_roadmap_markdown(custom_inputs, epics, milestones)

    assert "# PersonaScript MVP Development Roadmap (3-6 months)" in md
    assert "Linear Epics & Feature Breakdown" in md
    assert "Epic: Funnel-Aligned Content Generation Engine" in md
    assert "US-101a" in md


def test_full_execution(default_agent, custom_inputs):
    """Test end-to-end execution of the agent."""
    outputs = default_agent.execute(custom_inputs)

    assert isinstance(outputs, RoadmapOutputs)
    assert outputs.github_issue_url
    assert outputs.roadmap_markdown
    assert len(outputs.epics) == 4
    assert len(outputs.milestones) == 3

    # Verify GitHub issue URL format
    parsed_url = urlparse(outputs.github_issue_url)
    assert parsed_url.scheme == "https"
    assert "github.com" in parsed_url.netloc


def test_full_execution_with_default_inputs(default_agent):
    """Test end-to-end execution when no inputs are explicitly passed."""
    outputs = default_agent.execute()

    assert isinstance(outputs, RoadmapOutputs)
    assert outputs.github_issue_url
    assert outputs.roadmap_markdown
    assert len(outputs.epics) == 4
