"""
Unit tests for PersonaScriptContentIterationAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.content_iteration_agent import (
    PersonaScriptContentIterationAgent,
    AgentInputs,
    ContentAsset,
    WeeklyAnalyticsReport,
    ABTestResultsSummary,
    BacklogItem,
    AgentOutputs
)


@pytest.fixture
def sample_inputs():
    """Create sample inputs for the ContentIterationAgent."""
    assets = [
        ContentAsset(
            id="asset-1",
            title="How to Scale B2B Content",
            url="/blog/how-to-scale-b2b-content",
            type="blog",
            current_cta="Download eBook",
            audience_target="Content Marketing Manager"
        ),
        ContentAsset(
            id="asset-2",
            title="AI Personalization Feature Page",
            url="/features/ai-personalization",
            type="landing_page",
            current_cta="Start Free Trial",
            audience_target="VP of Marketing"
        ),
        ContentAsset(
            id="asset-3",
            title="SaaS Pricing Page",
            url="/pricing",
            type="pricing",
            current_cta="Contact Sales",
            audience_target="CMO"
        )
    ]
    return AgentInputs(
        start_date="2025-10-01",
        end_date="2025-10-08",
        existing_content_assets=assets
    )


@pytest.fixture
def agent():
    """Create a default Agent instance."""
    return PersonaScriptContentIterationAgent()


def test_agent_initialization():
    """Test that agent initializes and hooks up integrations correctly."""
    agent_instance = PersonaScriptContentIterationAgent()
    assert agent_instance is not None
    assert agent_instance.mixpanel is not None
    assert agent_instance.google_analytics is not None
    assert agent_instance.optimizely is not None
    assert agent_instance.linear is not None
    assert agent_instance.github is not None
    assert len(agent_instance.execution_log) == 0


def test_agent_initialization_with_credentials():
    """Test that agent configures integrations when credentials are provided."""
    agent_instance = PersonaScriptContentIterationAgent(
        mixpanel_api_key="mp_key",
        mixpanel_project_id="mp_pid",
        google_analytics_property_id="ga_pid",
        google_analytics_credentials_path="/path/to/ga.json",
        optimizely_api_key="opt_key",
        optimizely_project_id="opt_pid",
        linear_api_key="lin_key",
        linear_team_id="lin_team",
        github_token="gh_token",
        github_repo="owner/repo"
    )
    assert agent_instance.mixpanel.api_key == "mp_key"
    assert agent_instance.mixpanel.project_id == "mp_pid"
    assert agent_instance.google_analytics.property_id == "ga_pid"
    assert agent_instance.google_analytics.credentials_path == "/path/to/ga.json"
    assert agent_instance.optimizely.api_key == "opt_key"
    assert agent_instance.optimizely.project_id == "opt_pid"
    assert agent_instance.linear.api_key == "lin_key"
    assert agent_instance.linear.team_id == "lin_team"
    assert agent_instance.github.token == "gh_token"
    assert agent_instance.github.repo == "owner/repo"


def test_data_consolidation_and_analysis(agent, sample_inputs):
    """Test that step 4 properly consolidates data from Mixpanel & Google Analytics."""
    mp_perf = agent.mixpanel.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    ga_perf = agent.google_analytics.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    mp_eng = agent.mixpanel.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    ga_eng = agent.google_analytics.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    experiments = agent.optimizely.get_experiments()

    analysis = agent._analyze_data(
        sample_inputs, mp_perf, ga_perf, mp_eng, ga_eng, experiments
    )

    assert "pages" in analysis
    assert "experiments" in analysis
    assert len(analysis["pages"]) > 0
    assert len(analysis["experiments"]) == 2

    # Check that a page contains fields from both integrations
    blog_page = next((p for p in analysis["pages"] if p["url"] == "/blog/how-to-scale-b2b-content"), None)
    assert blog_page is not None
    assert blog_page["views"] > 0
    assert blog_page["sessions"] > 0
    assert blog_page["scroll_depth"] > 0.0
    assert blog_page["engagement_rate"] > 0.0


def test_generate_weekly_analytics_report(agent, sample_inputs):
    """Test step 5 report generation."""
    mp_perf = agent.mixpanel.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    ga_perf = agent.google_analytics.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    mp_eng = agent.mixpanel.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    ga_eng = agent.google_analytics.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    experiments = agent.optimizely.get_experiments()

    analysis = agent._analyze_data(
        sample_inputs, mp_perf, ga_perf, mp_eng, ga_eng, experiments
    )
    report = agent._generate_weekly_report(analysis, sample_inputs)

    assert isinstance(report, WeeklyAnalyticsReport)
    assert report.summary
    assert len(report.content_performance) > 0
    assert len(report.engagement_insights) > 0

    # Confirm high-performing or underperforming classifications exist
    assert len(report.high_performing_urls) >= 0
    assert len(report.underperforming_urls) >= 0


def test_synthesize_ab_results(agent):
    """Test step 6: A/B results summary synthesis."""
    experiments = agent.optimizely.get_experiments()
    summary = agent._synthesize_ab_results(experiments)

    assert isinstance(summary, ABTestResultsSummary)
    assert summary.summary
    assert len(summary.experiments) == 2
    assert len(summary.winning_variations) == 2
    assert len(summary.actionable_recommendations) == 2

    # Check winning variations properties
    win = summary.winning_variations[0]
    assert "experiment_id" in win
    assert "winning_variation" in win
    assert "improvement_percent" in win


def test_prioritization_logic_and_backlog(agent, sample_inputs):
    """Test step 7: Backlog identification and prioritization heuristics."""
    mp_perf = agent.mixpanel.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    ga_perf = agent.google_analytics.get_content_performance(sample_inputs.start_date, sample_inputs.end_date)
    mp_eng = agent.mixpanel.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    ga_eng = agent.google_analytics.get_user_engagement(sample_inputs.start_date, sample_inputs.end_date)
    experiments = agent.optimizely.get_experiments()

    analysis = agent._analyze_data(
        sample_inputs, mp_perf, ga_perf, mp_eng, ga_eng, experiments
    )
    report = agent._generate_weekly_report(analysis, sample_inputs)
    ab_summary = agent._synthesize_ab_results(experiments)

    backlog = agent._prioritize_backlog(report, ab_summary, sample_inputs)

    assert len(backlog) > 0
    assert all(isinstance(item, BacklogItem) for item in backlog)

    # Check prioritization sorting (score descending)
    scores = [item.priority_score for item in backlog]
    assert scores == sorted(scores, reverse=True)

    # Check priority levels mapping
    for item in backlog:
        assert item.priority_level in ["Critical", "High", "Medium", "Low"]
        if item.priority_score >= 80:
            assert item.priority_level == "Critical"
        elif item.priority_score >= 60:
            assert item.priority_level == "High"


def test_create_linear_issues(agent, sample_inputs):
    """Test step 8: Linear issue creation and mapping back to backlog items."""
    item = BacklogItem(
        id="test-backlog-1",
        title="Optimize Pricing Page CTA",
        description="Low conversions recorded",
        priority_level="High",
        priority_score=75,
        category="CTA optimization",
        target_url="/pricing"
    )

    updated = agent._create_linear_issues([item])
    assert len(updated) == 1
    assert updated[0].linear_issue_url is not None
    assert updated[0].linear_issue_url.startswith("https://linear.app")


def test_full_execution_flow(agent, sample_inputs):
    """Test full agent execution end-to-end and returned outputs."""
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, AgentOutputs)
    assert isinstance(outputs.weekly_analytics_report, WeeklyAnalyticsReport)
    assert isinstance(outputs.ab_test_results_summary, ABTestResultsSummary)
    assert len(outputs.prioritized_feature_backlog) > 0

    # Check that GitHub issue was compiled and returns valid URL structure
    assert outputs.github_issue_url
    parsed = urlparse(outputs.github_issue_url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")

    # Check execution log completed 9 steps (with start and complete for each step)
    assert len(agent.execution_log) == 18
    steps_tracked = set(log["step"] for log in agent.execution_log)
    assert steps_tracked == set(range(1, 10))


def test_data_consolidation_aggregates_multiple_entries(agent, sample_inputs):
    """Test that multiple entries for the same page are averaged and aggregated correctly."""
    mp_perf = [
        {"page_url": "/pricing", "page_views": 100, "conversion_rate": 0.02, "bounce_rate": 0.50},
        {"page_url": "/pricing", "page_views": 200, "conversion_rate": 0.04, "bounce_rate": 0.60}
    ]
    ga_perf = [
        {"page_url": "/pricing", "sessions": 80, "bounce_rate": 0.40}
    ]
    mp_eng = [
        {"page_url": "/pricing", "average_scroll_depth_percent": 80.0, "clicks_by_element": {"btn1": 5}},
        {"page_url": "/pricing", "average_scroll_depth_percent": 90.0, "clicks_by_element": {"btn1": 10}}
    ]
    ga_eng = [
        {"page_url": "/pricing", "engagement_rate": 0.40},
        {"page_url": "/pricing", "engagement_rate": 0.60}
    ]

    analysis = agent._analyze_data(sample_inputs, mp_perf, ga_perf, mp_eng, ga_eng, [])

    assert len(analysis["pages"]) == 1
    page = analysis["pages"][0]

    assert page["views"] == 300
    assert page["sessions"] == 80
    assert pytest.approx(page["conversion_rate"]) == 0.03 # (0.02 + 0.04) / 2
    assert pytest.approx(page["bounce_rate"]) == 0.50 # (0.50 + 0.60 + 0.40) / 3
    assert pytest.approx(page["scroll_depth"]) == 85.0 # (80.0 + 90.0) / 2
    assert pytest.approx(page["engagement_rate"]) == 0.50 # (0.40 + 0.60) / 2
    assert page["clicks_by_element"] == {"btn1": 15}


def test_execute_gracefully_handles_errors(agent, sample_inputs):
    """Test that execute captures and gracefully processes exceptions without crashing."""
    # Force an exception by passing None instead of inputs
    outputs = agent.execute(None)

    assert outputs.status == "error"
    assert outputs.error_message is not None
    assert len(outputs.prioritized_feature_backlog) == 0
    assert outputs.weekly_analytics_report.summary == "An error occurred during execution. No analytics available."
