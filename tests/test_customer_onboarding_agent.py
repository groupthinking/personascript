"""
Unit tests for CustomerOnboardingAndSupportAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.customer_onboarding_agent import (
    CustomerOnboardingAndSupportAgent,
    OnboardingAgentInputs,
    OnboardingAgentOutputs
)


@pytest.fixture
def sample_onboarding_inputs():
    """Create sample onboarding and support setup input data for testing."""
    return OnboardingAgentInputs(
        onboarding_spec=[
            {
                "title": "PersonaScript Welcome Flow",
                "audience": "growth_b2b_saas_leads",
                "steps": [
                    {
                        "title": "Welcome & Brand Workspace Setup",
                        "description": "Welcome to PersonaScript! Let's configure your workspace.",
                        "requires_video": True,
                        "type": "video_tour"
                    },
                    {
                        "title": "First Persona Creation",
                        "description": "Step-by-step tour on how to generate your first hyper-personalized persona.",
                        "requires_video": False,
                        "type": "product_tour"
                    }
                ]
            }
        ],
        chat_support_requirements={
            "routing_rule": "route_to_marketing_enablement",
            "automated_responses": [
                {
                    "trigger": "first_time_user",
                    "response": "Hi there! Welcome to PersonaScript! How can we help you scale your B2B SaaS content today?"
                }
            ],
            "team_assignments": [
                {"agent_name": "Sarah (Support Lead)", "role": "Onboarding Specialist"}
            ]
        },
        knowledge_base_outlines={
            "categories": [
                {
                    "name": "Getting Started",
                    "sections": [
                        {
                            "name": "Workspace Configuration",
                            "articles": [
                                {
                                    "title": "How to Configure Brand Guidelines",
                                    "requires_video": True
                                },
                                {
                                    "title": "Inviting Team Members",
                                    "requires_video": False
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        brand_guidelines={
            "brand_name": "PersonaScript",
            "theme_color": "#4F46E5",
            "logo_url": "https://personascript.com/logo.png"
        }
    )


@pytest.fixture
def onboarding_agent():
    """Create an instance of the agent."""
    return CustomerOnboardingAndSupportAgent()


def test_agent_initialization():
    """Test that customer onboarding agent initializes correctly."""
    agent = CustomerOnboardingAndSupportAgent()
    assert agent is not None
    assert agent.intercom is not None
    assert agent.zendesk is not None
    assert agent.loom is not None
    assert agent.github is not None


def test_agent_with_credentials():
    """Test agent initialization with custom credentials."""
    agent = CustomerOnboardingAndSupportAgent(
        intercom_api_key="intercom_abc",
        zendesk_subdomain="custom_sub",
        zendesk_api_token="zendesk_abc",
        loom_api_key="loom_abc",
        github_token="github_abc",
        github_repo="owner/repo"
    )
    assert agent.intercom.api_key == "intercom_abc"
    assert agent.zendesk.subdomain == "custom_sub"
    assert agent.zendesk.api_token == "zendesk_abc"
    assert agent.loom.api_key == "loom_abc"
    assert agent.github.token == "github_abc"
    assert agent.github.repo == "owner/repo"


def test_parse_and_comprehend_specs(onboarding_agent, sample_onboarding_inputs):
    """Test step 1 context parsing of specifications."""
    parsed = onboarding_agent._parse_and_comprehend_specs(sample_onboarding_inputs)
    assert parsed["brand_name"] == "PersonaScript"
    assert parsed["theme_color"] == "#4F46E5"
    assert parsed["sequences_count"] == 1
    assert parsed["kb_categories_count"] == 1


def test_extract_video_outlines(onboarding_agent, sample_onboarding_inputs):
    """Test extracting video outlines based on specifications requiring video."""
    outlines = onboarding_agent._extract_video_outlines(sample_onboarding_inputs)
    assert len(outlines) == 2
    assert outlines[0]["title"] == "How to: Welcome & Brand Workspace Setup"
    assert outlines[1]["title"] == "KB Tutorial: How to Configure Brand Guidelines"


def test_compile_detailed_report(onboarding_agent, sample_onboarding_inputs):
    """Test report compilation formatting and content."""
    intercom_seq = onboarding_agent.intercom.configure_onboarding_sequences(sample_onboarding_inputs.onboarding_spec)
    intercom_chat = onboarding_agent.intercom.integrate_chat_support(sample_onboarding_inputs.chat_support_requirements)
    zendesk_kb = onboarding_agent.zendesk.populate_knowledge_base(sample_onboarding_inputs.knowledge_base_outlines)

    outlines = onboarding_agent._extract_video_outlines(sample_onboarding_inputs)
    loom_videos = onboarding_agent.loom.generate_multiple_tutorials(outlines)

    integration_status = onboarding_agent.intercom.configure_zendesk_integration("personascript")

    report = onboarding_agent._compile_detailed_report(
        sample_onboarding_inputs,
        intercom_seq,
        intercom_chat,
        zendesk_kb,
        loom_videos,
        integration_status
    )

    assert "PersonaScript Onboarding and Support System Implementation Report" in report
    assert "Intercom Onboarding Sequences" in report
    assert "Intercom In-App Chat Support" in report
    assert "Zendesk Knowledge Base" in report
    assert "Loom Video Tutorials" in report
    assert "How to Configure Brand Guidelines" in report


def test_full_execution(onboarding_agent, sample_onboarding_inputs):
    """Test full onboarding support setup workflow execution."""
    outputs = onboarding_agent.execute(sample_onboarding_inputs)

    # Verify outputs are properly formed
    assert isinstance(outputs, OnboardingAgentOutputs)
    assert outputs.intercom_sequences["status"] == "success"
    assert outputs.intercom_chat_support["status"] == "success"
    assert outputs.zendesk_knowledge_base["status"] == "success"
    assert len(outputs.loom_videos) == 2
    assert outputs.github_issue_url
    assert outputs.execution_summary_report

    # Verify URLs
    parsed_git_url = urlparse(outputs.github_issue_url)
    assert parsed_git_url.scheme == "https"
    assert parsed_git_url.netloc.endswith("github.com")

    # Verify report is populated in GitHub issue body
    assert "Implementation Report" in outputs.execution_summary_report
    assert "Loom Video Tutorials" in outputs.execution_summary_report
