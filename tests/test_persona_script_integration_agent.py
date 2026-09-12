"""Tests for PersonaScriptIntegrationAgent."""

import pytest
from src.agents.persona_script_integration_agent import (
    PersonaScriptIntegrationAgent,
    PersonaScriptContent,
    HubSpotObjectDefinition,
    ContentfulContentModel,
    AgentInputs,
    AgentOutputs
)


def test_agent_initialization():
    agent = PersonaScriptIntegrationAgent()
    assert agent is not None


def test_agent_full_execution_workflow():
    agent = PersonaScriptIntegrationAgent()

    blog_item = PersonaScriptContent(
        id="item-001",
        content_type="blog_post",
        title="AI-Powered Marketing Automation",
        body="<p>PersonaScript simplifies SaaS marketing copy generation...</p>",
        summary="A summary of AI-powered marketing automation",
        author="Growth Marketer",
        slug="ai-powered-marketing-automation"
    )

    email_item = PersonaScriptContent(
        id="item-002",
        content_type="email",
        title="Welcome Email Campaign",
        body="Hello {{first_name}}, welcome to PersonaScript!",
        summary="Welcome to PersonaScript"
    )

    inputs = AgentInputs(content_items=[blog_item, email_item])
    outputs: AgentOutputs = agent.execute(inputs)

    assert outputs.status == "success"
    assert "Successfully developed, executed, and verified" in outputs.confirmation_message
    assert len(outputs.published_hubspot_items) == 2
    assert len(outputs.published_contentful_items) == 2
    assert len(outputs.integration_test_results) >= 4
    assert outputs.github_issue_url != ""
    assert "# PersonaScript Integration Documentation" in outputs.documentation_markdown


def test_agent_custom_object_definitions():
    agent = PersonaScriptIntegrationAgent()

    custom_item = PersonaScriptContent(
        id="custom-001",
        content_type="landing_page",
        title="PersonaScript Demo Landing Page",
        body="<h1>Get Started Today</h1>",
        slug="persona-script-demo"
    )

    custom_hs_defs = {
        "landing_page": HubSpotObjectDefinition(
            object_type="landing_page",
            property_mappings={"title": "htmlTitle", "body": "pageBody", "slug": "slug"},
            required_properties=["htmlTitle", "pageBody"]
        )
    }

    custom_ct_models = {
        "landing_page": ContentfulContentModel(
            content_type_id="landingPage",
            field_mappings={"title": "headline", "body": "heroContent", "slug": "pageSlug"},
            required_fields=["headline", "heroContent"]
        )
    }

    inputs = AgentInputs(
        content_items=[custom_item],
        hubspot_object_definitions=custom_hs_defs,
        contentful_content_models=custom_ct_models
    )

    outputs = agent.execute(inputs)
    assert outputs.status == "success"
    assert len(outputs.published_hubspot_items) == 1
    assert outputs.published_hubspot_items[0]["target_object_type"] == "landing_page"
    assert outputs.published_contentful_items[0]["content_type_id"] == "landingPage"
