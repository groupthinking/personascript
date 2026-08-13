"""
Unit tests for FigmaPrototypeDesignerAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents import (
    FigmaPrototypeDesignerAgent,
    FigmaPrototypeDesignerInputs,
    FigmaPrototypeDesignerOutputs
)


@pytest.fixture
def sample_inputs():
    """Create sample input data for testing."""
    return FigmaPrototypeDesignerInputs(
        workflows=["create a campaign", "ingest brand guidelines"],
        user_stories={
            "create a campaign": [
                "As a marketer, I want to define target parameters to build standard layouts.",
                "As a designer, I want standard grids so I don't have to manually realign objects."
            ],
            "ingest brand guidelines": [
                "As a brand owner, I want to drag and drop assets to automatically sync colors."
            ]
        },
        brand_guidelines={
            "colors": {
                "primary": "#0D1B2A",
                "secondary": "#E0E1DD",
                "accent": "#415A77",
                "background": "#FFFFFF"
            },
            "typography": {
                "h1": "Roboto-Bold-36",
                "h2": "Roboto-Medium-24",
                "body": "Roboto-Regular-16",
                "caption": "Roboto-Light-12"
            },
            "logo": "PersonaScript Logo Standard V2",
            "voice_and_tone": "Warm, inspiring, professional B2B SaaS voice"
        }
    )


@pytest.fixture
def agent():
    """Create an agent instance for testing."""
    return FigmaPrototypeDesignerAgent()


def test_agent_initialization(agent):
    """Test that agent initializes correctly."""
    assert agent is not None
    assert agent.figma_integration is not None
    assert agent.github_integration is not None


def test_analyze_brand_guidelines(agent, sample_inputs):
    """Test extracting colors, typography, and logo from guidelines."""
    analyzed_styles = agent._analyze_brand_guidelines(sample_inputs.brand_guidelines)

    assert analyzed_styles["primary_color"] == "#0D1B2A"
    assert analyzed_styles["secondary_color"] == "#E0E1DD"
    assert analyzed_styles["accent_color"] == "#415A77"
    assert analyzed_styles["background_color"] == "#FFFFFF"
    assert analyzed_styles["typography_scale"]["h1"] == "Roboto-Bold-36"
    assert analyzed_styles["typography_scale"]["body"] == "Roboto-Regular-16"
    assert analyzed_styles["logo_asset"] == "PersonaScript Logo Standard V2"
    assert analyzed_styles["voice_and_tone"] == "Warm, inspiring, professional B2B SaaS voice"


def test_generate_wireframes(agent, sample_inputs):
    """Test generating standard wireframes from user stories."""
    wireframes = agent._generate_wireframes(sample_inputs.workflows, sample_inputs.user_stories)

    assert "create a campaign" in wireframes
    assert "ingest brand guidelines" in wireframes

    campaign_wf = wireframes["create a campaign"]
    assert campaign_wf["layout"] == "Grid-12, Sidebar-Navigation"
    assert len(campaign_wf["screens"]) == 2
    assert campaign_wf["screens"][0]["screen_name"] == "Create a campaign - Start Screen"
    assert "Header" in campaign_wf["screens"][0]["components"]


def test_full_execution(agent, sample_inputs):
    """Test full FigmaPrototypeDesignerAgent workflow execution."""
    outputs = agent.execute(sample_inputs)

    assert outputs.prototype_url
    assert outputs.design_system_url
    assert outputs.github_issue_url

    # Check URLs using proper URL parsing
    proto_parsed = urlparse(outputs.prototype_url)
    assert proto_parsed.scheme == "https"
    assert proto_parsed.netloc.endswith("figma.com")
    assert "/proto/" in proto_parsed.path

    ds_parsed = urlparse(outputs.design_system_url)
    assert ds_parsed.scheme == "https"
    assert ds_parsed.netloc.endswith("figma.com")
    assert "/file/" in ds_parsed.path

    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc.endswith("github.com")
    assert "issues" in github_parsed.path

    # Validate structure collections are non-empty
    assert len(outputs.analyzed_styles) > 0
    assert len(outputs.wireframes) == 2
    assert len(outputs.high_fidelity_mockups) == 2
    assert len(outputs.interactions) == 2

    # Ensure color mapping is propagated down
    assert outputs.high_fidelity_mockups["create a campaign"]["styles_applied"]["primary_bg"] == "#0D1B2A"
    assert outputs.high_fidelity_mockups["create a campaign"]["styles_applied"]["brand_accent"] == "#E0E1DD"
