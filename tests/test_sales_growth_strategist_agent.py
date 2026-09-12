"""
Unit tests for SalesGrowthStrategistAgent and related Salesforce, Gong, and ZoomInfo integrations.
"""

import pytest
from urllib.parse import urlparse

from src.agents.sales_growth_strategist_agent import (
    SalesGrowthStrategistAgent,
    AgentInputs,
    AgentOutputs
)
from src.integrations.salesforce_integration import SalesforceIntegration
from src.integrations.gong_integration import GongIntegration
from src.integrations.zoominfo_integration import ZoomInfoIntegration


@pytest.fixture
def agent():
    """Create a default SalesGrowthStrategistAgent instance."""
    return SalesGrowthStrategistAgent()


@pytest.fixture
def sample_inputs():
    """Create sample AgentInputs."""
    return AgentInputs(
        salesforce_api_key="sf_key_123",
        salesforce_instance_url="https://test.salesforce.com",
        gong_access_key="gong_key_456",
        gong_access_key_secret="gong_secret_789",
        zoominfo_username="user@personascript.com",
        zoominfo_client_id="zi_client_000",
        icp_and_value_prop="B2B SaaS Content Automation for Mid-Market Enterprises",
        current_team_structure={"Account Executives": 3, "Sales Development Representatives (SDRs)": 2},
        target_mrr_growth_percent=60.0
    )


def test_salesforce_integration_mock_and_params():
    """Test SalesforceIntegration initialization and metric retrieval."""
    sf = SalesforceIntegration()
    metrics = sf.get_sales_performance_metrics()
    assert "mrr" in metrics
    assert "lead_to_opportunity_rate" in metrics
    assert "average_sales_cycle_days" in metrics
    assert metrics["mrr"] > 0

    sf_custom = SalesforceIntegration(api_key="key", instance_url="https://custom.salesforce.com")
    assert sf_custom.api_key == "key"
    assert sf_custom.instance_url == "https://custom.salesforce.com"


def test_gong_integration_mock_and_params():
    """Test GongIntegration initialization and call analytics retrieval."""
    gong = GongIntegration()
    analytics = gong.get_call_transcripts_and_analytics()
    assert "total_calls_analyzed" in analytics
    assert "average_talk_ratio" in analytics
    assert "top_objections" in analytics
    assert len(analytics["top_objections"]) > 0

    gong_custom = GongIntegration(access_key="k", access_key_secret="s")
    assert gong_custom.access_key == "k"
    assert gong_custom.access_key_secret == "s"


def test_zoominfo_integration_mock_and_params():
    """Test ZoomInfoIntegration initialization and market intelligence retrieval."""
    zi = ZoomInfoIntegration()
    intel = zi.get_prospect_and_market_intelligence()
    assert "ideal_customer_profile" in intel
    assert "target_buyer_titles" in intel
    assert "buying_intent_signals" in intel
    assert intel["addressable_market_accounts_count"] > 0

    zi_custom = ZoomInfoIntegration(username="usr", client_id="cid")
    assert zi_custom.username == "usr"
    assert zi_custom.client_id == "cid"


def test_agent_initialization():
    """Test SalesGrowthStrategistAgent initialization with default and custom values."""
    agent_default = SalesGrowthStrategistAgent()
    assert agent_default.salesforce is not None
    assert agent_default.gong is not None
    assert agent_default.zoominfo is not None
    assert agent_default.github is not None
    assert len(agent_default.execution_log) == 0

    agent_custom = SalesGrowthStrategistAgent(
        salesforce_api_key="sf_k",
        salesforce_instance_url="https://sf.com",
        gong_access_key="gk",
        gong_access_key_secret="gs",
        zoominfo_username="zi_u",
        zoominfo_client_id="zi_c",
        github_token="gh_t",
        github_repo="owner/repo"
    )
    assert agent_custom.salesforce.api_key == "sf_k"
    assert agent_custom.gong.access_key == "gk"
    assert agent_custom.zoominfo.username == "zi_u"
    assert agent_custom.github.token == "gh_t"


def test_agent_data_analysis(agent, sample_inputs):
    """Test data analysis logic step."""
    sf_metrics = agent.salesforce.get_sales_performance_metrics()
    gong_analytics = agent.gong.get_call_transcripts_and_analytics()
    zoominfo_intel = agent.zoominfo.get_prospect_and_market_intelligence()

    analysis = agent._analyze_sales_data(sample_inputs, sf_metrics, gong_analytics, zoominfo_intel)
    assert "identified_bottlenecks" in analysis
    assert "rep_talk_percent" in analysis
    assert "top_objections" in analysis
    assert analysis["opps_per_ae"] > 0


def test_agent_playbook_and_expansion_plan_generation(agent, sample_inputs):
    """Test playbook refinement and expansion plan drafting."""
    sf_metrics = agent.salesforce.get_sales_performance_metrics()
    gong_analytics = agent.gong.get_call_transcripts_and_analytics()
    zoominfo_intel = agent.zoominfo.get_prospect_and_market_intelligence()
    analysis = agent._analyze_sales_data(sample_inputs, sf_metrics, gong_analytics, zoominfo_intel)

    playbook = agent._refine_sales_playbook(sample_inputs, analysis)
    assert "Refined Sales Playbook" in playbook
    assert "Objection Handling" in playbook

    expansion_plan = agent._develop_expansion_plan(sample_inputs, analysis)
    assert "Sales Team Expansion Plan" in expansion_plan
    assert "30-60-90 Day Onboarding Guidelines" in expansion_plan

    tech_recs = agent._formulate_tech_recommendations(sample_inputs, analysis)
    assert "Salesforce CRM Optimization" in tech_recs
    assert "Gong.io Conversational Intelligence" in tech_recs
    assert "ZoomInfo Market Intelligence" in tech_recs

    revenue_report = agent._compile_revenue_impact_report(sample_inputs, sf_metrics, analysis)
    assert "Projected Impact Report" in revenue_report
    assert "Target MRR Growth Rate" in revenue_report


def test_full_agent_execution(agent, sample_inputs):
    """Test complete 7-step execution workflow end-to-end."""
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, AgentOutputs)
    assert outputs.status == "success"
    assert outputs.refined_sales_playbook
    assert outputs.sales_team_expansion_plan
    assert outputs.tech_stack_recommendations
    assert outputs.revenue_impact_report
    assert outputs.github_issue_url

    # Check GitHub URL format
    parsed_gh = urlparse(outputs.github_issue_url)
    assert parsed_gh.scheme == "https"
    assert parsed_gh.netloc == "github.com"

    # Verify 7 execution steps in log
    steps = [log["step"] for log in outputs.execution_log]
    assert set(steps) == set(range(1, 8))


def test_agent_execution_with_none_inputs(agent):
    """Test execution with default None inputs."""
    outputs = agent.execute(None)
    assert outputs.status == "success"
    assert outputs.github_issue_url
    assert len(outputs.execution_log) > 0


def test_agent_execution_error_handling(agent):
    """Test that agent catches exceptions during execution gracefully."""
    # Pass an invalid input type to provoke an exception
    outputs = agent.execute("invalid_inputs_type")
    assert outputs.status == "error"
    assert outputs.error_message is not None
