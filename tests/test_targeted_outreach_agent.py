"""
Unit tests for TargetedOutreachAgent, ApolloIntegration, and LinkedInIntegration.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.integrations.apollo_integration import ApolloIntegration
from src.integrations.linkedin_integration import LinkedInIntegration
from src.agents.targeted_outreach_agent import (
    TargetedOutreachAgent,
    ICPDetails,
    CampaignConfig,
    AdCreative,
    Lead,
    PersonalizedMessage,
    AdPerformanceMetrics,
    AgentInputs,
    AgentOutputs
)


@pytest.fixture
def sample_icp():
    return ICPDetails(
        industry="B2B SaaS",
        company_size_range="50-200",
        target_job_titles=["VP of Demand Generation", "Head of Growth Marketing"],
        target_locations=["United States"]
    )


@pytest.fixture
def sample_campaign():
    return CampaignConfig(
        campaign_name="Test Ad Campaign",
        daily_budget=200.0,
        objective="LEAD_GENERATION",
        ad_format="SPONSORED_UPDATES"
    )


@pytest.fixture
def sample_creatives():
    return [
        AdCreative(
            headline="Scale your SaaS leads with AI",
            ad_copy="Transform your content velocity with PersonaScript.",
            media_url="https://personascript.com/banner.png",
            destination_url="https://personascript.com/demo"
        )
    ]


@pytest.fixture
def sample_inputs(sample_icp, sample_campaign, sample_creatives):
    return AgentInputs(
        icp_details=sample_icp,
        campaign_config=sample_campaign,
        ad_creatives=sample_creatives,
        target_lead_count=10
    )


def test_apollo_integration_simulated():
    apollo = ApolloIntegration()
    leads = apollo.search_people(titles=["VP Marketing"], industry="B2B SaaS", count=10)
    assert len(leads) == 10
    assert leads[0]["name"]
    assert leads[0]["email"]
    assert "@" in leads[0]["email"]


def test_apollo_integration_with_api_key():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "people": [
                {
                    "id": "123",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "title": "CMO",
                    "email": "jane@tech.io",
                    "linkedin_url": "https://linkedin.com/in/janedoe",
                    "organization": {"name": "TechCorp"}
                }
            ]
        }

        apollo = ApolloIntegration(api_key="mock_key")
        leads = apollo.search_people(count=1)
        assert len(leads) == 1
        assert leads[0]["name"] == "Jane Doe"
        assert leads[0]["email"] == "jane@tech.io"


def test_linkedin_integration_simulated():
    linkedin = LinkedInIntegration()

    # Create campaign
    c_res = linkedin.create_campaign("Test", "LEAD_GEN", 150.0, {})
    assert "campaign_id" in c_res
    assert c_res["status"] == "DRAFT"

    # Upload creative
    cr_res = linkedin.upload_ad_creative(c_res["campaign_id"], "Head", "Copy")
    assert cr_res["status"] == "APPROVED"

    # Launch campaign
    l_res = linkedin.launch_campaign(c_res["campaign_id"])
    assert l_res["status"] == "ACTIVE"

    # Metrics
    m_res = linkedin.get_campaign_performance(c_res["campaign_id"])
    assert m_res["impressions"] > 0
    assert m_res["clicks"] > 0
    assert m_res["spend"] > 0


def test_targeted_outreach_agent_full_workflow(sample_inputs):
    agent = TargetedOutreachAgent()
    outputs = agent.execute(sample_inputs)

    assert outputs.status == "success"
    assert len(outputs.qualified_leads) == 10
    assert len(outputs.personalized_messages) == 10
    assert outputs.campaign_id
    assert outputs.campaign_dashboard_url
    assert outputs.ad_performance.impressions > 0
    assert outputs.ad_performance.spend > 0
    assert "github.com" in outputs.github_issue_url
    assert len(agent.execution_log) == 20


def test_targeted_outreach_agent_error_handling(sample_inputs):
    agent = TargetedOutreachAgent()
    with patch.object(agent.apollo, "search_people", side_effect=RuntimeError("Apollo API crash")):
        outputs = agent.execute(sample_inputs)
        assert outputs.status == "error"
        assert "Apollo API crash" in outputs.error_message
