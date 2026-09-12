"""
Unit tests for PersonaScriptFrontendUIAgent.
"""

import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse

from src.agents.frontend_ui_agent import (
    PersonaScriptFrontendUIAgent,
    AgentInputs,
    AgentOutputs,
    UIBlueprint,
    ComponentBlueprint
)


@pytest.fixture
def agent():
    """Fixture providing a default agent instance."""
    return PersonaScriptFrontendUIAgent()


@pytest.fixture
def sample_inputs():
    """Fixture providing sample inputs for testing."""
    return AgentInputs(
        task_specifications=[
            "content generation",
            "brief creation",
            "content management dashboard"
        ],
        tech_stack={
            "framework": "Next.js",
            "language": "TypeScript",
            "styling": "Tailwind CSS"
        }
    )


def test_agent_initialization():
    """Test that the agent initializes properly."""
    agent = PersonaScriptFrontendUIAgent(github_token="fake_token", github_repo="owner/repo")
    assert agent is not None
    assert agent.github_token == "fake_token"
    assert agent.github_repo == "owner/repo"
    assert agent.github_integration is not None


def test_parse_task_specifications(agent):
    """Test parsing of frontend UI task specifications."""
    specs = ["content generation interface", "brief creation", "content management"]
    parsed = agent._parse_task_specifications(specs)

    assert parsed["content_generation"] is True
    assert parsed["brief_creation"] is True
    assert parsed["content_management"] is True


def test_extract_tech_stack(agent):
    """Test tech stack extraction and normalization."""
    input_stack = {
        "framework": "Next.js",
        "language": "TypeScript",
        "styling": "Chakra UI"
    }
    extracted = agent._extract_tech_stack(input_stack)

    assert extracted["framework"] == "Next.js"
    assert extracted["language"] == "TypeScript"
    assert extracted["styling"] == "Chakra UI"
    assert "state_management" in extracted
    assert "component_library" in extracted


def test_formulate_ui_blueprint(agent, sample_inputs):
    """Test formulation of the structured UI blueprint."""
    parsed_specs = agent._parse_task_specifications(sample_inputs.task_specifications)
    tech_stack = agent._extract_tech_stack(sample_inputs.tech_stack)

    blueprint = agent._formulate_ui_blueprint(parsed_specs, tech_stack)

    assert isinstance(blueprint, UIBlueprint)
    assert len(blueprint.content_generation_components) >= 3
    assert len(blueprint.brief_creation_components) >= 3
    assert len(blueprint.content_management_components) >= 3
    assert len(blueprint.setup_considerations) >= 4

    # Check component blueprint structure
    gen_comp = blueprint.content_generation_components[0]
    assert isinstance(gen_comp, ComponentBlueprint)
    assert gen_comp.name
    assert len(gen_comp.key_features) > 0


def test_formulate_issue_body(agent, sample_inputs):
    """Test markdown formatting of GitHub issue body."""
    parsed_specs = agent._parse_task_specifications(sample_inputs.task_specifications)
    tech_stack = agent._extract_tech_stack(sample_inputs.tech_stack)
    blueprint = agent._formulate_ui_blueprint(parsed_specs, tech_stack)

    body = agent._formulate_issue_body(
        goal="Generate a detailed technical blueprint for frontend UI",
        inputs=sample_inputs,
        blueprint=blueprint
    )

    assert "# PersonaScript Next.js Frontend Application Blueprint" in body
    assert "Content Generation Interface Components" in body
    assert "Brief Creation Interface Components" in body
    assert "Content Management Dashboard Components" in body
    assert "Directory Structure Recommendation" in body


@patch("src.integrations.github_integration.GitHubIntegration.create_issue")
def test_full_execution_workflow(mock_create_issue, agent, sample_inputs):
    """Test full execution workflow of the agent with mock GitHub API response."""
    mock_create_issue.return_value = "https://github.com/groupthinking/personascript/issues/101"

    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, AgentOutputs)
    assert outputs.status == "success"
    assert outputs.github_issue_url == "https://github.com/groupthinking/personascript/issues/101"
    assert outputs.issue_title == "Frontend UI Blueprint: PersonaScript Next.js Application Specifications"
    assert "PersonaScript Next.js Frontend Application Blueprint" in outputs.issue_body

    # Check URL format
    parsed_url = urlparse(outputs.github_issue_url)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "github.com"

    mock_create_issue.assert_called_once()


@patch("src.integrations.github_integration.GitHubIntegration.create_issue")
def test_execution_error_handling(mock_create_issue, agent):
    """Test agent error handling when issue creation raises an exception."""
    mock_create_issue.side_effect = Exception("GitHub API unavailable")

    outputs = agent.execute()

    assert outputs.status == "error"
    assert outputs.error_message == "GitHub API unavailable"
    assert outputs.github_issue_url == ""
