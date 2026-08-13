"""
Unit tests for TargetedOutreachAgent.
"""

import os
import json
import pytest
from urllib.parse import urlparse
from src.agents.targeted_outreach_agent import (
    TargetedOutreachAgent,
    TargetedOutreachInputs,
    LeadInfo,
    TargetedOutreachOutputs
)


@pytest.fixture
def sample_inputs():
    """Create sample inputs for the outreach agent."""
    return TargetedOutreachInputs(
        icp_industries=["B2B SaaS", "Artificial Intelligence"],
        icp_company_sizes=["50-200", "201-500"],
        icp_job_titles=["VP of Marketing", "Head of Growth", "CMO"],
        ad_budget=5000.0,
        ad_objective="LEAD_GENERATION",
        ad_copy="Accelerate your B2B SaaS marketing scaling today with PersonaScript!",
        ad_asset_url="https://personascript.com/assets/campaign-banner.png",
        message_template="Hi {first_name}, noticed you are the {title} at {company_name}. Let's chat B2B content scaling."
    )


@pytest.fixture
def agent():
    """Create an outreach agent instance."""
    return TargetedOutreachAgent()


def test_agent_initialization():
    """Test initialization with default parameters."""
    agent = TargetedOutreachAgent()
    assert agent.apollo_integration is not None
    assert agent.linkedin_integration is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test initialization with credentials."""
    agent = TargetedOutreachAgent(
        apollo_api_key="apollo_key",
        linkedin_client_id="client_id",
        linkedin_client_secret="client_secret",
        linkedin_account_id="account_id",
        github_token="gh_token",
        github_repo="owner/repo"
    )
    assert agent.apollo_integration.api_key == "apollo_key"
    assert agent.linkedin_integration.client_id == "client_id"
    assert agent.linkedin_integration.client_secret == "client_secret"
    assert agent.linkedin_integration.account_id == "account_id"
    assert agent.github_integration.token == "gh_token"
    assert agent.github_integration.repo == "owner/repo"


def test_parse_icp_details(agent, sample_inputs):
    """Test step 1 parsing logic."""
    icp = agent._parse_icp_details(sample_inputs)
    assert icp["industries"] == ["B2B SaaS", "Artificial Intelligence"]
    assert icp["company_sizes"] == ["50-200", "201-500"]
    assert icp["job_titles"] == ["VP of Marketing", "Head of Growth", "CMO"]
    assert icp["budget"] == 5000.0
    assert icp["objective"] == "LEAD_GENERATION"


def test_apollo_lead_search_and_extraction(agent, sample_inputs):
    """Test step 2 and 3 lead generation & formatting."""
    leads = agent.apollo_integration.search_leads(
        industries=sample_inputs.icp_industries,
        company_sizes=sample_inputs.icp_company_sizes,
        job_titles=sample_inputs.icp_job_titles,
        limit=10
    )
    assert len(leads) > 0
    assert len(leads) <= 10
    assert leads[0]["first_name"]
    assert "@" in leads[0]["email"]


def test_message_personalization(agent, sample_inputs):
    """Test step 4 template personalization."""
    leads = [
        LeadInfo(
            first_name="Alice",
            last_name="Johnson",
            name="Alice Johnson",
            title="VP of Marketing",
            company_name="SaaSify",
            company_size="50-200",
            industry="B2B SaaS",
            email="alice@saasify.com",
            linkedin_url="https://linkedin.com/in/alice",
            location="San Francisco"
        )
    ]
    agent._personalize_messages(leads, sample_inputs.message_template)
    assert "Alice" in leads[0].personalized_message
    assert "VP of Marketing" in leads[0].personalized_message
    assert "SaaSify" in leads[0].personalized_message


def test_linkedin_campaign_flow(agent, sample_inputs):
    """Test steps 5, 6, 7 and 8 LinkedIn ads endpoints."""
    campaign_id = agent.linkedin_integration.create_campaign(
        name="Test Campaign",
        objective=sample_inputs.ad_objective,
        budget=sample_inputs.ad_budget,
        audience_criteria={"industries": sample_inputs.icp_industries}
    )
    assert campaign_id.startswith("urn:li:adCampaigns:")

    creative_id = agent.linkedin_integration.upload_creative(
        campaign_id=campaign_id,
        copy=sample_inputs.ad_copy,
        asset_url=sample_inputs.ad_asset_url
    )
    assert creative_id.startswith("urn:li:adCreatives:")

    launched = agent.linkedin_integration.launch_campaign(campaign_id)
    assert launched is True

    performance = agent.linkedin_integration.get_campaign_performance(campaign_id)
    assert performance["campaign_id"] == campaign_id
    assert performance["impressions"] > 0
    assert performance["clicks"] >= 0

    dashboard_url = agent.linkedin_integration.get_dashboard_url(campaign_id)
    parsed = urlparse(dashboard_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("linkedin.com")


def test_compile_summary_report(agent, sample_inputs):
    """Test step 9 markdown summary report builder."""
    leads = [
        LeadInfo(
            first_name="Alice", last_name="Johnson", name="Alice Johnson",
            title="VP of Marketing", company_name="SaaSify", company_size="50-200",
            industry="B2B SaaS", email="alice@saasify.com", linkedin_url="https://linkedin.com/in/alice",
            location="San Francisco", personalized_message="Hello Alice"
        )
    ]
    metrics = {
        "impressions": 1000,
        "clicks": 50,
        "ctr": 0.05,
        "spend": 100.0,
        "cpc": 2.0
    }
    report = agent._compile_summary_report(
        leads=leads,
        metrics=metrics,
        campaign_id="urn:li:adCampaigns:123",
        dashboard_url="https://linkedin.com/dash",
        inputs=sample_inputs
    )
    assert "# PersonaScript Targeted Outreach Campaign" in report
    assert "SaaSify" in report
    assert "Alice Johnson" in report
    assert "1,000" in report


def test_full_execution(agent, sample_inputs):
    """Test complete end-to-end execute method of Outreach Agent."""
    # Ensure previous leads file doesn't exist
    lead_file = "targeted_outreach_leads.json"
    if os.path.exists(lead_file):
        os.remove(lead_file)

    outputs = agent.execute(sample_inputs)

    assert os.path.exists(lead_file)
    with open(lead_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert len(saved_data) > 0
    assert "personalized_message" in saved_data[0]

    assert outputs.lead_list_file_path == lead_file
    assert outputs.linkedin_campaign_id
    assert outputs.linkedin_dashboard_url
    assert outputs.performance_metrics["impressions"] > 0
    assert outputs.github_issue_url
    assert len(outputs.leads) > 0

    # Clean up test output file
    if os.path.exists(lead_file):
        os.remove(lead_file)
