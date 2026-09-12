"""
Unit tests for FigmaPrototypeDesignerAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.figma_prototype_designer_agent import (
    FigmaPrototypeDesignerAgent,
    UserStoryRequirement,
    MVPWorkflow,
    BrandGuidelines,
    FigmaAgentInputs,
    FigmaAgentOutputs
)


@pytest.fixture
def sample_inputs():
    """Fixture providing sample FigmaAgentInputs matching MVP workflows."""
    workflow_1 = MVPWorkflow(
        name="create a campaign",
        description="Configure target personas, campaign channels, and generate multi-stage content variations.",
        user_stories=[
            UserStoryRequirement(
                id="US-101",
                title="Persona & Goal Selection",
                description="Select target B2B buyer persona and primary conversion goal.",
                acceptance_criteria=["Persona options loaded", "Goal dropdown functional"]
            ),
            UserStoryRequirement(
                id="US-102",
                title="Batch Content Generation Preview",
                description="Preview and generate multi-stage email and social collateral.",
                acceptance_criteria=["Preview renders in under 3s", "Export to ZIP available"]
            )
        ]
    )

    workflow_2 = MVPWorkflow(
        name="ingest brand guidelines",
        description="Upload brand PDFs, extract visual identity tokens, set banned words and tone sliders.",
        user_stories=[
            UserStoryRequirement(
                id="US-201",
                title="Brand PDF & Rules Extractor",
                description="Drag and drop corporate brand guidelines PDF for automated parsing.",
                acceptance_criteria=["PDF uploaded successfully", "Extracted tone keywords highlighted"]
            ),
            UserStoryRequirement(
                id="US-202",
                title="Style & Tone Configurator",
                description="Configure visual tone sliders and restricted terminology lists.",
                acceptance_criteria=["Tone sliders save state", "Banned word list updated"]
            )
        ]
    )

    brand = BrandGuidelines(
        brand_name="PersonaScript",
        colors={
            "primary": "#4F46E5",
            "secondary": "#7C3AED",
            "neutral_dark": "#111827",
            "neutral_light": "#F9FAFB",
            "accent": "#F59E0B"
        },
        typography={
            "primary_font": "Inter",
            "heading_font": "Plus Jakarta Sans",
            "base_size": "16px"
        },
        voice_and_tone="Professional, authoritative, intelligent, empathetic, and innovative."
    )

    return FigmaAgentInputs(
        workflows=[workflow_1, workflow_2],
        brand_guidelines=brand
    )


@pytest.fixture
def agent():
    """Fixture providing a default FigmaPrototypeDesignerAgent instance."""
    return FigmaPrototypeDesignerAgent()


def test_agent_initialization():
    """Test initializing agent with default and custom credentials."""
    default_agent = FigmaPrototypeDesignerAgent()
    assert default_agent.figma is not None
    assert default_agent.github is not None
    assert len(default_agent.execution_log) == 0

    custom_agent = FigmaPrototypeDesignerAgent(
        figma_api_token="test_figma_token",
        figma_file_key="test_file_key",
        github_token="test_git_token",
        github_repo="owner/repo"
    )
    assert custom_agent.figma.api_token == "test_figma_token"
    assert custom_agent.figma.file_key == "test_file_key"
    assert custom_agent.github.token == "test_git_token"
    assert custom_agent.github.repo == "owner/repo"


def test_parse_inputs(agent, sample_inputs):
    """Test Step 1: Input parsing helper."""
    parsed = agent._parse_inputs(sample_inputs)
    assert len(parsed["workflows"]) == 2
    assert parsed["workflows"][0]["name"] == "create a campaign"
    assert len(parsed["workflows"][0]["user_stories"]) == 2
    assert parsed["brand_guidelines"]["brand_name"] == "PersonaScript"


def test_analyze_brand_guidelines(agent, sample_inputs):
    """Test Step 2: Brand guidelines analysis helper."""
    parsed = agent._parse_inputs(sample_inputs)
    analyzed = agent._analyze_brand_guidelines(parsed["brand_guidelines"])

    assert analyzed["brand_name"] == "PersonaScript"
    assert analyzed["colors"]["primary"] == "#4F46E5"
    assert analyzed["typography"]["primary_font"] == "Inter"
    assert len(analyzed["interaction_patterns"]) > 0


def test_full_execution_workflow(agent, sample_inputs):
    """Test full 9-step agent execution workflow."""
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, FigmaAgentOutputs)
    assert outputs.status == "success"
    assert outputs.prototype_url
    assert outputs.design_system_url
    assert outputs.github_issue_url
    assert len(outputs.workflow_mockups) == 2
    assert len(outputs.execution_log) >= 9

    # Verify Figma prototype URL format
    proto_parsed = urlparse(outputs.prototype_url)
    assert proto_parsed.scheme == "https"
    assert proto_parsed.netloc == "www.figma.com"
    assert "proto" in proto_parsed.path

    # Verify Figma design system URL format
    ds_parsed = urlparse(outputs.design_system_url)
    assert ds_parsed.scheme == "https"
    assert ds_parsed.netloc == "www.figma.com"
    assert "file" in ds_parsed.path

    # Verify GitHub issue URL format
    git_parsed = urlparse(outputs.github_issue_url)
    assert git_parsed.scheme == "https"
    assert git_parsed.netloc == "github.com"
    assert "issues" in git_parsed.path


def test_agent_error_handling():
    """Test agent error handling when an exception occurs."""
    bad_agent = FigmaPrototypeDesignerAgent()
    # Pass invalid input type to trigger exception
    outputs = bad_agent.execute(None)

    assert outputs.status == "error"
    assert outputs.error_message is not None
    assert outputs.prototype_url == ""
