"""
Unit and integration tests for PersonaScriptIntegrationAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.persona_script_integration_agent import (
    PersonaScriptIntegrationAgent,
    ContentSchema,
    HubSpotObjectDefinition,
    ContentfulContentModelDefinition,
    IntegrationAgentInputs
)


@pytest.fixture
def sample_integration_inputs():
    """Create sample inputs for the Integration Agent."""
    content_payload = {
        "title": "Unlocking Sales Funnel Velocity",
        "body": "This is a detailed article body about B2B SaaS marketing tactics.",
        "summary": "Speed up lead conversion with PersonaScript.",
        "author": "Jordan Lead",
        "publish_date": "2025-10-15"
    }

    content_schema = ContentSchema(
        content_type="blog_post",
        fields={
            "title": "string",
            "body": "string",
            "summary": "string",
            "author": "string",
            "publish_date": "string"
        }
    )

    hubspot_object_def = HubSpotObjectDefinition(
        object_type="blog_post",
        properties=["name", "htmlTitle", "postBody", "postSummary", "blogAuthorId", "publishDate"]
    )

    contentful_content_model_def = ContentfulContentModelDefinition(
        content_type_id="blogPost",
        fields=["title", "body", "summary", "author", "publishDate"]
    )

    return IntegrationAgentInputs(
        content_payload=content_payload,
        content_schema=content_schema,
        hubspot_object_def=hubspot_object_def,
        contentful_content_model_def=contentful_content_model_def
    )


@pytest.fixture
def agent():
    """Create a default agent instance for testing."""
    return PersonaScriptIntegrationAgent()


def test_agent_initialization(agent):
    """Test that agent initializes correctly with all sub-integrations."""
    assert agent is not None
    assert agent.hubspot is not None
    assert agent.contentful is not None
    assert agent.github is not None


def test_agent_initialization_with_credentials():
    """Test initialization with explicit credentials."""
    agent_creds = PersonaScriptIntegrationAgent(
        hubspot_api_key="hs_api_key",
        hubspot_access_token="hs_token",
        contentful_space_id="cf_space",
        contentful_access_token="cf_token",
        contentful_environment_id="prod",
        github_token="gh_token",
        github_repo="owner/repo"
    )
    assert agent_creds.hubspot.api_key == "hs_api_key"
    assert agent_creds.hubspot.access_token == "hs_token"
    assert agent_creds.contentful.space_id == "cf_space"
    assert agent_creds.contentful.access_token == "cf_token"
    assert agent_creds.contentful.environment_id == "prod"
    assert agent_creds.github.token == "gh_token"
    assert agent_creds.github.repo == "owner/repo"


def test_input_validation_empty_payload(agent, sample_integration_inputs):
    """Test that validating inputs with empty payload raises ValueError."""
    sample_integration_inputs.content_payload = {}
    with pytest.raises(ValueError, match="content_payload cannot be empty"):
        agent._validate_inputs(sample_integration_inputs)


def test_input_validation_empty_schema(agent, sample_integration_inputs):
    """Test that validating inputs with empty schema raises ValueError."""
    sample_integration_inputs.content_schema = None
    with pytest.raises(ValueError, match="content_schema cannot be empty"):
        agent._validate_inputs(sample_integration_inputs)


def test_map_to_hubspot_semantic_mappings(agent, sample_integration_inputs):
    """Test that generic source fields map correctly to specific HubSpot properties."""
    mapped = agent.map_to_hubspot(
        sample_integration_inputs.content_payload,
        sample_integration_inputs.content_schema,
        sample_integration_inputs.hubspot_object_def
    )

    # Assert correct semantic property mappings
    assert mapped["name"] == "Unlocking Sales Funnel Velocity"
    assert mapped["htmlTitle"] == "Unlocking Sales Funnel Velocity"
    assert mapped["postBody"] == "This is a detailed article body about B2B SaaS marketing tactics."
    assert mapped["postSummary"] == "Speed up lead conversion with PersonaScript."
    assert mapped["blogAuthorId"] == "Jordan Lead"
    assert mapped["publishDate"] == "2025-10-15"


def test_map_to_contentful_semantic_mappings(agent, sample_integration_inputs):
    """Test that generic source fields map correctly to Contentful content model fields."""
    mapped = agent.map_to_contentful(
        sample_integration_inputs.content_payload,
        sample_integration_inputs.content_schema,
        sample_integration_inputs.contentful_content_model_def
    )

    # Assert correct semantic field mappings
    assert mapped["title"] == "Unlocking Sales Funnel Velocity"
    assert mapped["body"] == "This is a detailed article body about B2B SaaS marketing tactics."
    assert mapped["summary"] == "Speed up lead conversion with PersonaScript."
    assert mapped["author"] == "Jordan Lead"
    assert mapped["publishDate"] == "2025-10-15"


def test_full_workflow_execution(agent, sample_integration_inputs):
    """Test end-to-end execute method of the integration agent."""
    outputs = agent.execute(sample_integration_inputs)

    # Verify top level output indicators
    assert outputs.success is True
    assert outputs.hubspot_deployment_status["status"] == "success"
    assert outputs.contentful_deployment_status["status"] == "success"
    assert outputs.github_issue_url
    assert outputs.documentation_markdown

    # Verify GitHub issue URL structure
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")

    # Verify Contentful localized payloads in the deployment status details
    contentful_details = outputs.contentful_deployment_status
    assert contentful_details["published"] is True
    assert contentful_details["mapped_payload"]["title"] == "Unlocking Sales Funnel Velocity"
    assert contentful_details["data"]["fields"]["title"] == {"en-US": "Unlocking Sales Funnel Velocity"}

    # Verify Documentation contents
    doc = outputs.documentation_markdown
    assert "# PersonaScript API Integration Documentation" in doc
    assert "HubSpot CMS/CRM Mapping" in doc
    assert "Contentful Headless CMS Mapping" in doc
    assert "Troubleshooting" in doc
