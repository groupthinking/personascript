"""
Unit tests for PersonaScriptFeaturePlanningAgent and Linear integration.
"""

import pytest
from urllib.parse import urlparse
from src.integrations.linear_integration import LinearIntegration
from src.agents.feature_planning_agent import (
    PersonaScriptFeaturePlanningAgent,
    FeatureRequirement,
    FeaturePlanningInputs,
    FeaturePlanningOutputs
)


@pytest.fixture
def sample_feature_requirements():
    """Create sample advanced features for testing."""
    return [
        FeatureRequirement(
            name="Multi-Persona Content Generation",
            description="Generate personalized B2B marketing collateral tailored to multiple target personas simultaneously.",
            key_details=[
                "Simultaneous generation of copy for up to 5 distinct B2B roles",
                "Built-in tone and voice matching per persona",
                "Direct export to marketing templates"
            ]
        ),
        FeatureRequirement(
            name="Campaign Planning Tools",
            description="A comprehensive toolkit to map and schedule multi-stage, multi-touch campaigns.",
            key_details=[
                "Visual workflow canvas mapping awareness to decision stages",
                "Automated scheduling and calendar integration",
                "Pre-built SaaS campaign templates"
            ]
        ),
        FeatureRequirement(
            name="Deeper CRM Integrations",
            description="Synchronize content interaction logs and track closed-loop conversion metrics.",
            key_details=[
                "Bi-directional sync with HubSpot and Salesforce",
                "Conversion attribution tracking for custom landing pages",
                "Lead score integration based on content consumed"
            ]
        )
    ]


@pytest.fixture
def sample_inputs(sample_feature_requirements):
    """Create sample input data for testing."""
    return FeaturePlanningInputs(
        advanced_features=sample_feature_requirements,
        existing_roadmap_id="roadmap-123",
        linear_api_key="mock_linear_key",
        github_token="mock_github_token",
        github_repo="groupthinking/personascript"
    )


def test_linear_integration_initialization():
    """Test LinearIntegration class initialization."""
    integration = LinearIntegration()
    assert integration is not None
    assert integration.api_key is None

    integration_with_key = LinearIntegration(api_key="test_key")
    assert integration_with_key.api_key == "test_key"


def test_linear_integration_get_roadmap():
    """Test LinearIntegration get_roadmap method."""
    integration = LinearIntegration()
    roadmap = integration.get_roadmap("roadmap-abc")

    assert roadmap is not None
    assert roadmap["id"] == "roadmap-abc"
    assert "projects" in roadmap
    assert len(roadmap["projects"]) > 0


def test_linear_integration_update_roadmap():
    """Test LinearIntegration update_roadmap method."""
    integration = LinearIntegration()
    updates = {
        "title": "PersonaScript Advanced Features Product Roadmap",
        "projects": []
    }
    url = integration.update_roadmap("roadmap-abc", updates)
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("linear.app")


def test_linear_integration_create_roadmap():
    """Test LinearIntegration create_roadmap method."""
    integration = LinearIntegration()
    url = integration.create_roadmap(
        title="Custom New Roadmap",
        description="A brand new roadmap",
        projects=[]
    )
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("linear.app")
    assert "custom-new-roadmap" in parsed.path


def test_agent_initialization():
    """Test that agent initializes correctly with defaults and parameters."""
    agent = PersonaScriptFeaturePlanningAgent()
    assert agent is not None
    assert agent.linear_integration is not None
    assert agent.github_integration is not None


def test_parse_requirements(sample_feature_requirements):
    """Test requirement parsing and attribute extraction."""
    agent = PersonaScriptFeaturePlanningAgent()
    parsed = agent._parse_requirements(sample_feature_requirements)

    assert len(parsed) == 3
    assert parsed[0]["name"] == "Multi-Persona Content Generation"
    assert parsed[0]["complexity"] == "Medium"
    assert parsed[0]["dependencies"] == ["User Persona Profiles"]

    # Campaign Planning complexity and dependencies
    assert parsed[1]["complexity"] == "Medium-High"
    assert parsed[1]["dependencies"] == ["User Persona Profiles", "Content Journey Maps"]

    # CRM Integrations complexity and dependencies
    assert parsed[2]["complexity"] == "High"
    assert parsed[2]["dependencies"] == ["Campaign Planning Tools", "Multi-Persona Content Generation"]


def test_generate_release_notes(sample_feature_requirements):
    """Test markdown draft release notes generation."""
    agent = PersonaScriptFeaturePlanningAgent()
    parsed = agent._parse_requirements(sample_feature_requirements)
    release_notes = agent._generate_release_notes(parsed)

    assert release_notes is not None
    assert "# PersonaScript Draft Release Notes" in release_notes
    assert "Multi-Persona Content Generation" in release_notes
    assert "Campaign Planning Tools" in release_notes
    assert "Deeper CRM Integrations" in release_notes
    assert "Bi-directional sync with HubSpot and Salesforce" in release_notes


def test_full_agent_execution(sample_inputs):
    """Test complete end-to-end execution of the agent."""
    agent = PersonaScriptFeaturePlanningAgent()
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, FeaturePlanningOutputs)
    assert outputs.roadmap_url
    assert outputs.draft_release_notes
    assert outputs.github_issue_url

    # Validate URLs
    parsed_roadmap = urlparse(outputs.roadmap_url)
    assert parsed_roadmap.scheme == "https"
    assert parsed_roadmap.netloc.endswith("linear.app")

    parsed_github = urlparse(outputs.github_issue_url)
    assert parsed_github.scheme == "https"
    assert parsed_github.netloc.endswith("github.com")


def test_github_issue_content_format(sample_inputs):
    """Test that the generated GitHub issue matches the requested format precisely."""
    # We will mock GITHUB_TOKEN and REPO so GitHubIntegration generates a mock URL
    agent = PersonaScriptFeaturePlanningAgent(
        github_token="dummy",
        github_repo="groupthinking/personascript"
    )

    # Spy or intercept the create_issue call to inspect body
    original_create_issue = agent.github_integration.create_issue
    captured_body = []

    def mock_create_issue(title, body, labels=None, assignees=None):
        captured_body.append(body)
        return original_create_issue(title, body, labels, assignees)

    agent.github_integration.create_issue = mock_create_issue

    agent.execute(sample_inputs)

    assert len(captured_body) == 1
    body = captured_body[0]

    # Verify the structure as required:
    # 'Goal: [Agent's Goal]', 'Inputs: [List of Inputs]', 'Outputs: [List of Outputs with URLs where applicable]', 'Execution Plan: [Summary of steps 1-5]'
    assert "Goal: To plan and document advanced feature development for PersonaScript, resulting in an updated product roadmap and draft release notes." in body
    assert "Inputs:" in body
    assert "Outputs:" in body
    assert "Execution Plan:" in body

    # Check that details of inputs/outputs are list items
    assert "- Advanced Feature Requirements" in body
    assert "- URL to Updated Product Roadmap in Linear" in body
    assert "1. **Parse & Understand Requirements**:" in body
    assert "3. **Formulate Updated Roadmap**:" in body
    assert "5. **Consolidate Deliverables**:" in body
