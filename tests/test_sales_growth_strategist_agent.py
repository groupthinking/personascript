"""
Unit tests for SalesGrowthStrategistAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.sales_growth_strategist_agent import (
    SalesGrowthStrategistAgent,
    SalesAgentInputs,
    SalesAgentOutputs,
)


@pytest.fixture
def sample_sales_inputs():
    """Create sample sales inputs for testing."""
    return SalesAgentInputs(
        salesforce_credentials={"username": "sf_user", "password": "sf_password"},
        gong_credentials={"api_key": "gong_key"},
        zoominfo_credentials={"api_key": "zi_key"},
        existing_playbook="Original playbook content",
        current_team_structure={"reps_count": 2, "roles": ["Account Executive"]},
        icp_and_value_prop="High-volume content personalization for marketing leaders",
    )


@pytest.fixture
def strategist_agent():
    """Create an agent instance for testing."""
    return SalesGrowthStrategistAgent()


def test_agent_initialization():
    """Test that agent initializes correctly with nested integrations."""
    agent = SalesGrowthStrategistAgent()
    assert agent is not None
    assert agent.salesforce_integration is not None
    assert agent.gong_integration is not None
    assert agent.zoominfo_integration is not None
    assert agent.google_docs_integration is not None
    assert agent.github_integration is not None


def test_agent_with_custom_credentials():
    """Test initializing with explicit credentials."""
    agent = SalesGrowthStrategistAgent(
        salesforce_credentials={"username": "custom_sf"},
        gong_credentials={"api_key": "custom_gong"},
        zoominfo_credentials={"api_key": "custom_zi"},
        google_docs_credentials={"type": "service_account"},
        github_token="custom_gh",
        github_repo="owner/repo",
    )
    assert agent.salesforce_integration.username == "custom_sf"
    assert agent.gong_integration.api_key == "custom_gong"
    assert agent.zoominfo_integration.api_key == "custom_zi"
    assert agent.github_integration.token == "custom_gh"
    assert agent.github_integration.repo == "owner/repo"


def test_collect_and_aggregate_data(strategist_agent, sample_sales_inputs):
    """Test collecting data from the integrations."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    assert "salesforce" in data
    assert "gong" in data
    assert "zoominfo" in data

    assert data["salesforce"]["current_mrr"] == 45000.0
    assert "conversational_metrics" in data["gong"]
    assert "ideal_customer_profile_icp" in data["zoominfo"]


def test_analyze_data(strategist_agent, sample_sales_inputs):
    """Test that data analysis correctly flags bottlenecks and capacity gaps."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)

    assert "bottlenecks" in analysis
    assert "playbook_gaps" in analysis
    assert "capacity_gaps" in analysis
    assert "metrics_analyzed" in analysis

    # Representative talk ratio is 63% in mock data, which is > 50%, so it should be flagged
    assert any("Talk-to-Listen Ratio" in b for b in analysis["bottlenecks"])

    # Pricing success rate is 32% in mock data, which is < 50%, so it should be flagged
    assert any("Pricing Objections" in g for g in analysis["playbook_gaps"])

    # No specialized SDR role in input team structure, so it should be flagged
    assert any("SDR/BDR" in c for c in analysis["capacity_gaps"])


def test_refine_playbook(strategist_agent, sample_sales_inputs):
    """Test playbook refinement generation."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)
    playbook = strategist_agent._refine_playbook(analysis, sample_sales_inputs)

    assert playbook
    assert "Refined Sales Playbook" in playbook
    assert "MEDDPICC" in playbook
    assert "Objection A: 'Pricing / Budget Constraints'" in playbook
    assert "Objection B: 'AI Security and Data Privacy'" in playbook


def test_develop_expansion_plan(strategist_agent, sample_sales_inputs):
    """Test sales team expansion plan development."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)
    plan = strategist_agent._develop_expansion_plan(analysis, sample_sales_inputs)

    assert plan
    assert "Sales Team Expansion Plan" in plan
    assert "SDR" in plan
    assert "Account Executive" in plan
    assert "30-60-90 Day Onboarding Guidelines" in plan


def test_formulate_tech_recommendations(strategist_agent, sample_sales_inputs):
    """Test formulating CRM and conversational intelligence tech recommendations."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)
    recs = strategist_agent._formulate_tech_recommendations(analysis)

    assert recs
    assert "Technology Optimization Recommendations" in recs
    assert "Salesforce" in recs
    assert "Gong.io" in recs
    assert "ZoomInfo" in recs


def test_generate_impact_report(strategist_agent, sample_sales_inputs):
    """Test MRR growth and sales efficiency projection generation."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)
    plan = strategist_agent._develop_expansion_plan(analysis, sample_sales_inputs)
    report = strategist_agent._generate_impact_report(analysis, plan)

    assert report
    assert "Projected Strategy Impact on MRR & Sales Efficiency" in report
    assert "Current Baseline MRR" in report
    assert "Projected State" in report


def test_create_google_doc_report(strategist_agent):
    """Test that the Google Doc strategy report URL is correctly structured."""
    url = strategist_agent._create_google_doc_report(
        "Playbook content", "Expansion plan", "Tech recs", "Impact report"
    )
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("docs.google.com")


def test_create_github_issue(strategist_agent, sample_sales_inputs):
    """Test that the GitHub issue creation URL is correctly structured."""
    data = strategist_agent._collect_and_aggregate_data(sample_sales_inputs)
    analysis = strategist_agent._analyze_data(data, sample_sales_inputs)
    plan = strategist_agent._develop_expansion_plan(analysis, sample_sales_inputs)
    report = strategist_agent._generate_impact_report(analysis, plan)

    url = strategist_agent._create_github_issue(
        "https://docs.google.com/document/d/test-doc/edit",
        sample_sales_inputs,
        analysis,
        report,
    )
    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")
    assert "issues" in parsed.path.split("/")


def test_full_execution(strategist_agent, sample_sales_inputs):
    """Test end-to-end execute method of SalesGrowthStrategistAgent."""
    outputs = strategist_agent.execute(sample_sales_inputs)

    assert isinstance(outputs, SalesAgentOutputs)
    assert outputs.refined_playbook
    assert outputs.expansion_plan
    assert outputs.tech_recommendations
    assert outputs.impact_report

    # Check that URLs are properly formatted
    google_doc_parsed = urlparse(outputs.google_docs_url)
    assert google_doc_parsed.scheme == "https"
    assert google_doc_parsed.netloc.endswith("docs.google.com")

    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc.endswith("github.com")
    assert "issues" in github_parsed.path.split("/")
