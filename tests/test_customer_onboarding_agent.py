"""
Unit tests for CustomerOnboardingAndSupportAgent and its integrations.
"""

import pytest
from urllib.parse import urlparse
from src.agents.customer_onboarding_agent import (
    CustomerOnboardingAndSupportAgent,
    AgentInputs,
    OnboardingSequenceSpec,
    InAppSupportSpec,
    KnowledgeBaseArticleSpec,
    BrandGuidelines
)
from src.integrations.intercom_integration import IntercomIntegration
from src.integrations.zendesk_integration import ZendeskIntegration
from src.integrations.loom_integration import LoomIntegration


@pytest.fixture
def sample_inputs():
    """Create sample inputs for onboarding and support agent."""
    onboarding_specs = [
        OnboardingSequenceSpec(
            title="Welcome & Setup Sequence",
            target_audience="New B2B SaaS Signups",
            steps=[
                {
                    "step_number": 1,
                    "step_id": "step_1",
                    "title": "Welcome to PersonaScript",
                    "content": "Welcome! Let's set up your brand guidelines.",
                    "type": "in_app_message",
                    "trigger": "on_signup"
                },
                {
                    "step_number": 2,
                    "step_id": "step_2",
                    "title": "Create Your First Persona",
                    "content": "Follow this video to configure your first buyer persona.",
                    "type": "product_tour",
                    "trigger": "after_step_1"
                }
            ]
        )
    ]

    support_spec = InAppSupportSpec(
        routing_rules=[
            {"condition": "topic == 'billing'", "action": "route_to_team", "target": "Billing Team"},
            {"condition": "topic == 'technical'", "action": "route_to_team", "target": "Tech Support"}
        ],
        automated_responses=[
            {"trigger_keyword": "pricing", "response": "Check out our pricing page at /pricing."},
            {"trigger_keyword": "reset password", "response": "Click 'Forgot Password' on login."}
        ],
        team_assignments=[
            {"team_name": "Tier 1 Support", "members": ["agent1@example.com", "agent2@example.com"]}
        ]
    )

    kb_article_specs = [
        KnowledgeBaseArticleSpec(
            category_name="Getting Started",
            section_name="Account Setup",
            article_title="How to Configure Brand Guidelines",
            article_body="<p>Learn how to upload your PDF guidelines or define custom brand rules in PersonaScript.</p>",
            video_outline={
                "title": "Video Tutorial: Configure Brand Guidelines",
                "description": "Step-by-step video guide for setting up brand guidelines.",
                "duration_seconds": 180
            }
        ),
        KnowledgeBaseArticleSpec(
            category_name="Integrations",
            section_name="CMS Connections",
            article_title="Connecting HubSpot & Contentful",
            article_body="<p>Follow these instructions to connect your CMS integrations for automatic publishing.</p>"
        )
    ]

    brand_guidelines = BrandGuidelines(
        brand_name="PersonaScript",
        primary_color="#4F46E5",
        tone_of_voice="Professional, helpful, and empowering",
        logo_url="https://personascript.com/logo.png"
    )

    return AgentInputs(
        onboarding_specs=onboarding_specs,
        support_spec=support_spec,
        kb_article_specs=kb_article_specs,
        brand_guidelines=brand_guidelines
    )


def test_intercom_integration():
    """Test IntercomIntegration methods."""
    intercom = IntercomIntegration(api_key="test_key", app_id="test_app_123")

    # Test sequence creation
    seq_res = intercom.create_onboarding_sequence(
        title="Test Sequence",
        steps=[{"step_number": 1, "title": "Step 1"}]
    )
    assert seq_res["sequence_id"].startswith("seq_")
    assert seq_res["title"] == "Test Sequence"
    assert "test_app_123" in seq_res["url"]

    # Test in-app chat config
    chat_res = intercom.configure_in_app_chat(
        routing_rules=[{"rule": "rule1"}],
        automated_responses=[{"auto": "res1"}],
        team_assignments=[{"team": "tier1"}]
    )
    assert chat_res["config_id"].startswith("chat_cfg_")
    assert chat_res["status"] == "enabled"

    # Test embed video
    embed_res = intercom.embed_video_in_sequence(
        sequence_id=seq_res["sequence_id"],
        step_id="step_1",
        video_url="https://loom.com/embed/123",
        video_title="Intro Video"
    )
    assert embed_res["embed_status"] == "embedded"

    # Test zendesk integration config
    int_res = intercom.configure_zendesk_integration("personascript")
    assert int_res["status"] == "connected"


def test_zendesk_integration():
    """Test ZendeskIntegration methods."""
    zendesk = ZendeskIntegration(subdomain="testsub", email="user@example.com", api_token="token")

    # Test category creation
    cat_res = zendesk.create_category("Getting Started", "Desc")
    assert isinstance(cat_res["category_id"], int)
    assert cat_res["name"] == "Getting Started"

    # Test section creation
    sec_res = zendesk.create_section(cat_res["category_id"], "Account Setup", "Desc")
    assert isinstance(sec_res["section_id"], int)
    assert sec_res["category_id"] == cat_res["category_id"]

    # Test article creation
    art_res = zendesk.create_article(sec_res["section_id"], "Title 1", "<p>Body</p>")
    assert isinstance(art_res["article_id"], int)
    assert art_res["title"] == "Title 1"

    # Test embed video
    embed_res = zendesk.embed_video_in_article(art_res["article_id"], "https://loom.com/embed/123", "Video Title")
    assert embed_res["embed_status"] == "embedded"

    # Test intercom integration config
    int_res = zendesk.configure_intercom_integration("intercom_app")
    assert int_res["status"] == "active"


def test_loom_integration():
    """Test LoomIntegration methods."""
    loom = LoomIntegration(api_key="loom_key")
    video_res = loom.create_video_tutorial("Tutorial 1", "Description 1", duration_seconds=150)
    assert video_res["video_id"].startswith("loom_")
    assert video_res["title"] == "Tutorial 1"
    assert "loom.com/share/" in video_res["share_url"]
    assert "loom.com/embed/" in video_res["embed_url"]
    assert "<iframe" in video_res["embed_html"]


def test_customer_onboarding_agent_execution(sample_inputs):
    """Test complete 9-step execution workflow of CustomerOnboardingAndSupportAgent."""
    agent = CustomerOnboardingAndSupportAgent()
    outputs = agent.execute(sample_inputs)

    assert outputs.status == "success"
    assert outputs.error_message is None

    # Check onboarding sequence outputs
    assert len(outputs.onboarding_sequences) == 1
    seq = outputs.onboarding_sequences[0]
    assert seq.title == "Welcome & Setup Sequence"
    assert seq.sequence_id.startswith("seq_")

    # Check support chat outputs
    assert outputs.support_chat_config is not None
    assert outputs.support_chat_config.status == "enabled"
    assert len(outputs.support_chat_config.routing_rules) == 2

    # Check KB articles outputs
    assert len(outputs.knowledge_base_articles) == 2
    art1 = outputs.knowledge_base_articles[0]
    assert art1.title == "How to Configure Brand Guidelines"
    assert art1.embedded_video_url is not None
    assert "loom.com/embed/" in art1.embedded_video_url

    # Check Loom videos outputs
    assert len(outputs.loom_videos) == 1
    vid = outputs.loom_videos[0]
    assert vid.title == "Video Tutorial: Configure Brand Guidelines"

    # Check integration config
    assert outputs.integration_config is not None
    assert outputs.integration_config.status == "active"

    # Check implementation report
    assert outputs.implementation_report is not None
    assert outputs.implementation_report.onboarding_sequences_count == 1
    assert outputs.implementation_report.kb_articles_count == 2
    assert outputs.implementation_report.loom_videos_count == 1

    # Check GitHub issue URL format
    parsed_url = urlparse(outputs.github_issue_url)
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "github.com"
    assert "issues" in parsed_url.path


def test_customer_onboarding_agent_handles_error(sample_inputs, monkeypatch):
    """Test error handling in CustomerOnboardingAndSupportAgent execution."""
    agent = CustomerOnboardingAndSupportAgent()

    # Force an exception inside _parse_specifications
    def mock_fail(*args, **kwargs):
        raise ValueError("Simulated parsing error")

    monkeypatch.setattr(agent, "_parse_specifications", mock_fail)

    outputs = agent.execute(sample_inputs)
    assert outputs.status == "error"
    assert "Simulated parsing error" in outputs.error_message
