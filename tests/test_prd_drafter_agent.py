"""
Unit tests for PersonaScriptPRDDrafterAgent and its integrations.
"""

import pytest
from urllib.parse import urlparse
from src.agents.prd_drafter_agent import (
    PersonaScriptPRDDrafterAgent,
    AgentInputs,
    CoreFunctionality,
    UserStory
)
from src.integrations.notion_integration import NotionIntegration
from src.integrations.linear_integration import LinearIntegration


@pytest.fixture
def sample_inputs():
    """Create sample inputs matching the PRD task."""
    return AgentInputs(
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
            "high-volume, hyper-personalized, and brand-aligned content across all sales funnel "
            "stages, dramatically accelerating lead conversion and brand consistency."
        ),
        feature_concepts=[
            "Dynamic Content Generation",
            "Brand Guideline Adherence Engine",
            "User Profile Personalization"
        ]
    )


@pytest.fixture
def agent():
    """Create a default agent instance for testing."""
    return PersonaScriptPRDDrafterAgent()


def test_agent_initialization():
    """Test that the agent and its integrations initialize correctly."""
    agent = PersonaScriptPRDDrafterAgent()
    assert agent is not None
    assert agent.notion_integration is not None
    assert agent.linear_integration is not None
    assert agent.github_integration is not None
    assert len(agent.core_functionalities) == 0
    assert agent.prd_content == ""


def test_agent_with_credentials():
    """Test agent initialization with custom credentials."""
    agent = PersonaScriptPRDDrafterAgent(
        notion_token="test_notion_token",
        notion_database_id="test_db_id",
        linear_token="test_linear_token",
        github_token="test_github_token",
        github_repo="owner/repo"
    )
    assert agent.notion_integration.token == "test_notion_token"
    assert agent.notion_integration.database_id == "test_db_id"
    assert agent.linear_integration.token == "test_linear_token"
    assert agent.github_integration.token == "test_github_token"
    assert agent.github_integration.repo == "owner/repo"


def test_parse_context(agent, sample_inputs):
    """Test Step 1: Parsing and comprehension of context inputs."""
    parsed = agent._parse_context(sample_inputs)
    assert parsed["value_proposition"] == sample_inputs.value_proposition
    assert len(parsed["feature_concepts"]) == 3
    assert "Dynamic Content Generation" in parsed["feature_concepts"]


def test_define_core_functionalities(agent, sample_inputs):
    """Test Step 2, 3, 4: Define core functionalities, user stories, and acceptance criteria."""
    parsed = agent._parse_context(sample_inputs)
    functionalities = agent._define_core_functionalities(parsed)

    assert len(functionalities) == 3
    assert all(isinstance(f, CoreFunctionality) for f in functionalities)

    # Verify specific feature definitions and stories
    dynamic_gen = next(f for f in functionalities if f.name == "Dynamic Content Generation")
    assert "LLM prompts" in dynamic_gen.description
    assert len(dynamic_gen.user_stories) == 2

    # Check UserStory attributes and acceptance criteria presence
    story_1 = dynamic_gen.user_stories[0]
    assert story_1.id == "US-001"
    assert "B2B SaaS Content Marketer" in story_1.role
    assert len(story_1.acceptance_criteria) > 0


def test_compile_prd(agent, sample_inputs):
    """Test Step 5: Compilation of functional requirements into a V0.9 PRD draft."""
    parsed = agent._parse_context(sample_inputs)
    functionalities = agent._define_core_functionalities(parsed)
    prd = agent._compile_prd(sample_inputs.value_proposition, functionalities)

    assert prd
    assert "PersonaScript MVP Features PRD - V0.9" in prd
    assert "Executive Summary" in prd
    assert "US-001" in prd
    assert "US-005" in prd
    assert "Brand Guideline Adherence Engine" in prd


def test_notion_integration_and_step():
    """Test Notion integration and publishing helper."""
    integration = NotionIntegration()
    url = integration.create_page("Test Title", "Test Content")
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "notion.so"
    assert "mock-notion" in parsed.path


def test_linear_integration_and_step():
    """Test Linear integration and issue creation helper."""
    integration = LinearIntegration()
    url = integration.create_issue("Test Title", "Test Description")
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "linear.app"
    assert "mock-linear" in parsed.path


def test_full_execution(agent, sample_inputs):
    """Test the complete 8-step agent execution."""
    outputs = agent.execute(sample_inputs)

    # Verify outputs are generated
    assert outputs.notion_prd_url
    assert outputs.linear_issue_url
    assert outputs.github_issue_url
    assert outputs.prd_content
    assert len(outputs.core_functionalities) == 3

    # Verify Notion URL format
    notion_parsed = urlparse(outputs.notion_prd_url)
    assert notion_parsed.scheme == "https"
    assert notion_parsed.netloc == "notion.so"

    # Verify Linear URL format
    linear_parsed = urlparse(outputs.linear_issue_url)
    assert linear_parsed.scheme == "https"
    assert linear_parsed.netloc == "linear.app"

    # Verify GitHub URL format
    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc == "github.com"
    assert "issues" in github_parsed.path
