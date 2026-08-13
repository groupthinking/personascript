"""
Unit tests for PersonaScriptMVPDevelopmentRoadmapAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.mvp_roadmap_agent import (
    PersonaScriptMVPDevelopmentRoadmapAgent,
    RoadmapAgentInputs,
    RoadmapAgentOutputs,
    MVPDevelopmentRoadmap,
    MVPEpic,
    MVPFeature,
    UserStory
)


@pytest.fixture
def sample_inputs():
    """Create sample inputs for the roadmap agent."""
    return RoadmapAgentInputs(
        company_name="PersonaScript",
        value_proposition="Empowers growth-stage B2B SaaS marketing teams...",
        timeframe="3-6 months",
        target_platform="Linear",
        internal_docs_paths=[]
    )


def test_agent_initialization():
    """Test that the agent initializes with custom and default parameters."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    assert agent is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with explicit credentials."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent(
        openai_api_key="test_key",
        github_token="test_token",
        github_repo="owner/repo"
    )
    assert agent.openai_api_key == "test_key"
    assert agent.client is not None
    assert agent.github_integration.token == "test_token"
    assert agent.github_integration.repo == "owner/repo"


def test_parse_business_context(sample_inputs):
    """Test context parsing step."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    context = agent._parse_business_context(sample_inputs)
    assert context["company_name"] == "PersonaScript"
    assert context["timeframe"] == "3-6 months"
    assert "value_proposition" in context


def test_access_internal_documentation():
    """Test accessing internal documentation."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    insights = agent._access_internal_documentation([])
    assert len(insights) > 0
    assert any("README.md" in item["source_file"] for item in insights)


def test_synthesize_strategic_themes(sample_inputs):
    """Test synthesizing strategic themes (deterministic fallback)."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    context = agent._parse_business_context(sample_inputs)
    themes = agent._synthesize_strategic_themes(context, [])
    assert len(themes) >= 4
    assert any("Brand Alignment" in t for t in themes)


def test_generate_and_prioritize_features(sample_inputs):
    """Test generating and prioritizing features."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    context = agent._parse_business_context(sample_inputs)
    themes = agent._synthesize_strategic_themes(context, [])
    features = agent._generate_and_prioritize_features(themes, context)
    assert len(features) > 0
    assert any(f["id"] == "FEAT-1" for f in features)
    assert all("priority" in f for f in features)


def test_draft_mvp_roadmap(sample_inputs):
    """Test drafting detailed Linear-structured MVP roadmap."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    context = agent._parse_business_context(sample_inputs)
    themes = agent._synthesize_strategic_themes(context, [])
    features = agent._generate_and_prioritize_features(themes, context)
    roadmap = agent._draft_mvp_roadmap(features, sample_inputs.timeframe)

    assert isinstance(roadmap, MVPDevelopmentRoadmap)
    assert len(roadmap.epics) > 0

    # Check Epics, Features, and User Stories
    for epic in roadmap.epics:
        assert isinstance(epic, MVPEpic)
        assert epic.id.startswith("EPIC-")
        assert epic.target_timeline
        for feat in epic.features:
            assert isinstance(feat, MVPFeature)
            assert feat.id.startswith("FEAT-")
            for story in feat.user_stories:
                assert isinstance(story, UserStory)
                assert story.id.startswith("PS-")
                assert story.estimate


def test_construct_issue_body(sample_inputs):
    """Test composing detailed issue markdown body."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    context = agent._parse_business_context(sample_inputs)
    themes = agent._synthesize_strategic_themes(context, [])
    features = agent._generate_and_prioritize_features(themes, context)
    roadmap = agent._draft_mvp_roadmap(features, sample_inputs.timeframe)

    body = agent._construct_issue_body(sample_inputs, themes, roadmap)
    assert "PersonaScript MVP Development Roadmap" in body
    assert "Strategic Themes" in body
    assert "Detailed MVP Roadmap" in body
    assert "EPIC-1" in body
    assert "FEAT-101" in body
    assert "PS-101" in body


def test_full_execution(sample_inputs):
    """Test the complete execute flow of the agent."""
    agent = PersonaScriptMVPDevelopmentRoadmapAgent()
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, RoadmapAgentOutputs)
    assert isinstance(outputs.roadmap, MVPDevelopmentRoadmap)
    assert outputs.github_issue_url
    assert outputs.issue_body
    assert len(outputs.key_themes) > 0

    # Check scheme of issue URL
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")
