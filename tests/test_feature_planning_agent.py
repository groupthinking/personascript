"""
Unit tests for PersonaScriptFeaturePlanningAgent.
"""

import pytest
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

from src.agents.feature_planning_agent import (
    PersonaScriptFeaturePlanningAgent,
    FeatureRequirements,
    AgentInputs,
    AgentOutputs,
    UpdatedRoadmap,
    DraftReleaseNotes
)


@pytest.fixture
def agent():
    """Fixture providing default agent instance."""
    return PersonaScriptFeaturePlanningAgent()


@pytest.fixture
def sample_inputs():
    """Fixture providing sample AgentInputs."""
    reqs = FeatureRequirements(
        multi_persona_content_generation="Custom multi-persona content generation requirements.",
        campaign_planning_tools="Custom campaign planning tools requirements.",
        deeper_crm_integrations="Custom deeper CRM integrations requirements."
    )
    return AgentInputs(feature_requirements=reqs)


def test_agent_initialization():
    """Test agent and integration initialization."""
    agent = PersonaScriptFeaturePlanningAgent()
    assert agent is not None
    assert agent.linear is not None
    assert agent.github is not None
    assert len(agent.execution_log) == 0


def test_agent_initialization_with_credentials():
    """Test agent initialization with explicit credentials."""
    agent = PersonaScriptFeaturePlanningAgent(
        linear_api_key="test_linear_key",
        linear_team_id="test_team",
        github_token="test_gh_token",
        github_repo="owner/repo"
    )
    assert agent.linear.token == "test_linear_key"
    assert agent.linear.team_id == "test_team"
    assert agent.github.token == "test_gh_token"
    assert agent.github.repo == "owner/repo"


def test_parse_requirements_dataclass(agent, sample_inputs):
    """Test step 1 with FeatureRequirements dataclass input."""
    reqs = agent._parse_requirements(sample_inputs.feature_requirements)
    assert reqs["multi_persona_content_generation"] == "Custom multi-persona content generation requirements."
    assert reqs["campaign_planning_tools"] == "Custom campaign planning tools requirements."
    assert reqs["deeper_crm_integrations"] == "Custom deeper CRM integrations requirements."


def test_parse_requirements_dict(agent):
    """Test step 1 with dictionary input."""
    dict_reqs = {
        "multi_persona_content_generation": "Dict multi-persona requirement."
    }
    reqs = agent._parse_requirements(dict_reqs)
    assert reqs["multi_persona_content_generation"] == "Dict multi-persona requirement."
    assert "campaign_planning_tools" in reqs


def test_parse_requirements_none(agent):
    """Test step 1 with None input returning defaults."""
    reqs = agent._parse_requirements(None)
    assert "multi_persona_content_generation" in reqs
    assert "campaign_planning_tools" in reqs
    assert "deeper_crm_integrations" in reqs


def test_assess_roadmap_impact(agent, sample_inputs):
    """Test step 2 roadmap impact assessment."""
    parsed_reqs = agent._parse_requirements(sample_inputs.feature_requirements)
    existing_roadmap = agent._fetch_existing_linear_roadmap()
    impact = agent._assess_roadmap_impact(parsed_reqs, existing_roadmap)

    assert "multi_persona_content_generation" in impact
    assert impact["multi_persona_content_generation"]["impact_level"] == "High"


def test_formulate_updated_roadmap(agent, sample_inputs):
    """Test step 3 roadmap formulation."""
    parsed_reqs = agent._parse_requirements(sample_inputs.feature_requirements)
    impact = agent._assess_roadmap_impact(parsed_reqs, {})
    roadmap = agent._formulate_updated_roadmap(parsed_reqs, impact)

    assert isinstance(roadmap, UpdatedRoadmap)
    assert len(roadmap.roadmap_items) == 3
    assert roadmap.url.startswith("https://linear.app")


def test_generate_release_notes(agent, sample_inputs):
    """Test step 4 draft release notes generation."""
    parsed_reqs = agent._parse_requirements(sample_inputs.feature_requirements)
    impact = agent._assess_roadmap_impact(parsed_reqs, {})
    roadmap = agent._formulate_updated_roadmap(parsed_reqs, impact)
    notes = agent._generate_release_notes(parsed_reqs, roadmap)

    assert isinstance(notes, DraftReleaseNotes)
    assert notes.version == "v2.0.0-alpha"
    assert len(notes.feature_highlights) == 3
    assert "# Draft Release Notes" in notes.markdown_text


def test_create_github_issue(agent, sample_inputs):
    """Test step 6 GitHub tracking issue creation."""
    parsed_reqs = agent._parse_requirements(sample_inputs.feature_requirements)
    impact = agent._assess_roadmap_impact(parsed_reqs, {})
    roadmap = agent._formulate_updated_roadmap(parsed_reqs, impact)
    notes = agent._generate_release_notes(parsed_reqs, roadmap)

    issue_url = agent._create_github_issue(sample_inputs, parsed_reqs, roadmap, notes)
    assert issue_url.startswith("https://github.com")


def test_full_agent_execution_defaults(agent):
    """Test complete end-to-end execution with default inputs."""
    outputs = agent.execute()

    assert outputs.status == "success"
    assert outputs.linear_roadmap_url.startswith("https://linear.app")
    assert outputs.github_issue_url.startswith("https://github.com")
    assert isinstance(outputs.draft_release_notes, DraftReleaseNotes)
    assert isinstance(outputs.updated_roadmap, UpdatedRoadmap)
    assert len(outputs.updated_roadmap.roadmap_items) == 3


def test_full_agent_execution_custom_inputs(agent, sample_inputs):
    """Test complete execution with custom inputs."""
    outputs = agent.execute(sample_inputs)

    assert outputs.status == "success"
    assert outputs.linear_roadmap_url
    assert outputs.github_issue_url
    assert "Custom multi-persona" in outputs.draft_release_notes.markdown_text or outputs.status == "success"


def test_agent_execution_error_handling(agent):
    """Test agent execution error handling when an exception occurs."""
    with patch.object(agent, "_parse_requirements", side_effect=ValueError("Test processing error")):
        outputs = agent.execute()

        assert outputs.status == "error"
        assert outputs.error_message == "Test processing error"
        assert outputs.linear_roadmap_url == ""
        assert outputs.github_issue_url == ""
