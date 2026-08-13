"""
Unit tests for PersonaScriptFrontendUIAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.frontend_ui_agent import (
    PersonaScriptFrontendUIAgent,
    FrontendUIInputs,
    FrontendUIOutputs
)


@pytest.fixture
def agent():
    """Create a FrontendUIAgent instance for testing."""
    return PersonaScriptFrontendUIAgent()


@pytest.fixture
def default_inputs():
    """Create default inputs for testing."""
    return FrontendUIInputs()


def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = PersonaScriptFrontendUIAgent()
    assert agent is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with custom credentials."""
    agent = PersonaScriptFrontendUIAgent(
        github_token="dummy_token",
        github_repo="owner/repo"
    )
    assert agent.github_integration.token == "dummy_token"
    assert agent.github_integration.repo == "owner/repo"


def test_blueprint_generation(agent, default_inputs):
    """Test generating blueprint content and format."""
    specs = [s.lower() for s in default_inputs.specifications]
    stack = default_inputs.target_stack

    # Generate blueprint markdown
    markdown = agent._generate_blueprint_markdown(specs, stack, default_inputs.additional_notes)

    # Assert inclusion of core tech stack keywords
    assert "Next.js" in markdown or "Next.js (App Router)" in markdown
    assert "TypeScript" in markdown
    assert "Tailwind" in markdown
    assert "Chakra" in markdown

    # Assert inclusion of core workspace specs
    assert "Content Generation" in markdown
    assert "Brief Creation" in markdown
    assert "Content Management" in markdown


def test_github_issue_creation(agent, default_inputs):
    """Test the complete workflow execution including mock GitHub integration."""
    outputs = agent.execute(default_inputs)

    # Check outputs are formatted correctly
    assert isinstance(outputs, FrontendUIOutputs)
    assert "Blueprint:" in outputs.blueprint_title
    assert "# PersonaScript Frontend UI Technical Blueprint" in outputs.blueprint_body

    # Verify GitHub issue URL format
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com") or "example" in parsed.netloc
    assert "issues" in parsed.path
