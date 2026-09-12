"""
Unit tests for FigmaIntegration.
"""

import pytest
from src.integrations.figma_integration import FigmaIntegration


@pytest.fixture
def figma_integration():
    """Fixture providing a default FigmaIntegration instance."""
    return FigmaIntegration()


def test_figma_integration_initialization(figma_integration):
    """Test initial configuration and fallback mode."""
    assert figma_integration is not None
    assert figma_integration.file_key == "personaScriptMVPFileKey123"
    assert figma_integration.base_url == "https://api.figma.com/v1"


def test_is_configured():
    """Test is_configured method with and without API token."""
    unconfigured = FigmaIntegration()

    configured = FigmaIntegration(api_token="test_figma_token_123")
    assert configured.is_configured() is True


def test_create_or_update_design_system(figma_integration):
    """Test creating or updating Figma design system."""
    brand_guidelines = {
        "brand_name": "PersonaScript",
        "colors": {"primary": "#4F46E5", "secondary": "#7C3AED"},
        "typography": {"primary_font": "Inter"}
    }
    result = figma_integration.create_or_update_design_system(brand_guidelines)

    assert result["title"] == "PersonaScript Design System"
    assert "file_key" in result
    assert result["url"].startswith("https://www.figma.com/file/")
    assert len(result["components"]) > 0
    assert "Primary Blue" in result["styles"]["color_styles"]


def test_create_wireframes(figma_integration):
    """Test translating user stories into wireframes."""
    user_stories = [
        {"id": "US-101", "title": "Configure Campaign Target Persona"},
        {"id": "US-102", "title": "Set Funnel Output Formats"}
    ]
    wireframes = figma_integration.create_wireframes("create a campaign", user_stories)

    assert wireframes["workflow_name"] == "create a campaign"
    assert wireframes["slug"] == "create-a-campaign"
    assert wireframes["total_frames"] == 2
    assert wireframes["frames"][0]["user_story_id"] == "US-101"


def test_create_high_fidelity_mockups(figma_integration):
    """Test generating high-fidelity UI mockups in Figma."""
    wireframes = {
        "workflow_name": "ingest brand guidelines",
        "frames": [
            {"id": "wf-1", "name": "Upload Document"},
            {"id": "wf-2", "name": "Style Audit Config"}
        ]
    }
    design_system = {
        "file_key": "ds-12345",
        "styles": {"color_styles": ["Primary Blue", "Neutral Gray"]}
    }

    mockups = figma_integration.create_high_fidelity_mockups("ingest brand guidelines", wireframes, design_system)

    assert mockups["workflow_name"] == "ingest brand guidelines"
    assert mockups["url"].startswith("https://www.figma.com/file/")
    assert len(mockups["screens"]) == 2
    assert mockups["screens"][0]["brand_alignment"] == "100%"


def test_create_interactive_prototype(figma_integration):
    """Test creating interactive prototype navigation flows."""
    mockups = {
        "screens": [{"screen_id": "screen-1"}, {"screen_id": "screen-2"}]
    }
    proto = figma_integration.create_interactive_prototype("create a campaign", mockups)

    assert proto["workflow_name"] == "create a campaign"
    assert proto["url"].startswith("https://www.figma.com/proto/")
    assert proto["screens_connected"] == 2
    assert len(proto["interactions"]) > 0


def test_consolidate_master_prototype(figma_integration):
    """Test consolidating workflow prototypes into a master interactive prototype."""
    workflow_prototypes = [
        {"workflow_name": "create a campaign", "url": "https://www.figma.com/proto/1/wf1"},
        {"workflow_name": "ingest brand guidelines", "url": "https://www.figma.com/proto/2/wf2"}
    ]
    master = figma_integration.consolidate_master_prototype(workflow_prototypes)

    assert master["title"] == "PersonaScript MVP Interactive Master Prototype"
    assert master["total_prototypes"] == 2
    assert master["master_url"].startswith("https://www.figma.com/proto/")
    assert "create a campaign" in master["workflows_included"]
    assert "ingest brand guidelines" in master["workflows_included"]


def test_get_design_system_url(figma_integration):
    """Test getting public shareable URL for design system."""
    design_system = {"url": "https://www.figma.com/file/ds-999/personascript-design-system"}
    url = figma_integration.get_design_system_url(design_system)

    assert url == "https://www.figma.com/file/ds-999/personascript-design-system"
