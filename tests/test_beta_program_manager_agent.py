"""
Unit tests for BetaProgramManagerAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.beta_program_manager_agent import (
    BetaProgramManagerAgent,
    AlphaCustomer,
    StressTestPlan,
    BetaAgentInputs,
    FeedbackSession,
    LinearIssue,
    BetaProgramReport,
    BetaAgentOutputs
)


@pytest.fixture
def sample_customers():
    """Create a list of sample alpha customers."""
    return [
        AlphaCustomer(name="Sarah Connor", email="sarah@acme.com", company="Acme Corp"),
        AlphaCustomer(name="Alex Murphy", email="alex@globex.com", company="Globex"),
        AlphaCustomer(name="John Doe", email="john@umbrella.com", company="Umbrella")
    ]


@pytest.fixture
def sample_plan():
    """Create a sample stress-test plan."""
    return StressTestPlan(
        title="High Load Content Scaling Staging Phase",
        test_scenarios=[
            "Scenario 1: Generate 150+ custom B2B articles simultaneously under high volume request queue.",
            "Scenario 2: Apply custom vocabulary files up to 50MB and check system consistency."
        ],
        target_metrics={
            "max_concurrency": 200,
            "error_rate_threshold": 0.01,
            "avg_latency_ms": 1200
        },
        duration_days=14
    )


@pytest.fixture
def agent():
    """Initialize agent under test."""
    return BetaProgramManagerAgent()


def test_agent_initialization(agent):
    """Test that agent initializes correctly."""
    assert agent is not None
    assert agent.intercom is not None
    assert agent.linear is not None
    assert agent.zoom is not None
    assert agent.github is not None


def test_step_1_retrieve_inputs(agent, sample_customers, sample_plan):
    """Test retrieve inputs validation."""
    inputs = BetaAgentInputs(alpha_customers=sample_customers, stress_test_plan=sample_plan)
    customers, plan = agent._step_1_retrieve_inputs(inputs)

    assert len(customers) == 3
    assert plan.title == "High Load Content Scaling Staging Phase"

    # Test error handling
    with pytest.raises(ValueError, match="Alpha customers list cannot be empty"):
        agent._step_1_retrieve_inputs(BetaAgentInputs(alpha_customers=[], stress_test_plan=sample_plan))

    with pytest.raises(ValueError, match="Stress-test plan cannot be empty"):
        agent._step_1_retrieve_inputs(BetaAgentInputs(alpha_customers=sample_customers, stress_test_plan=None))

    invalid_plan = StressTestPlan(title="Invalid", test_scenarios=[], target_metrics={})
    with pytest.raises(ValueError, match="Stress-test plan must contain at least one scenario"):
        agent._step_1_retrieve_inputs(BetaAgentInputs(alpha_customers=sample_customers, stress_test_plan=invalid_plan))


def test_step_2_send_invites(agent, sample_customers, sample_plan):
    """Test Intercom user creation and personalized message invitation sending."""
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)

    assert len(onboarded) == 3
    for customer in onboarded:
        assert customer.onboarded is True
        assert customer.intercom_id.startswith("int_usr_")


def test_step_3_monitor_and_log_issues(agent, sample_customers, sample_plan):
    """Test feedback monitoring from Intercom and logging into Linear."""
    # First onboard customers to generate intercom IDs
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)
    bugs, features = agent._step_3_monitor_and_log_issues(onboarded)

    # Acme Corp (Sarah) -> Timeout (bug) and workflow (feature)
    # Globex (Alex) -> Crash (bug) and dark mode (feature)
    # Umbrella (John) -> General positive feedback (no tickets)

    assert len(bugs) == 2
    assert any(b.customer == "Acme Corp" and "Timeout" in b.title for b in bugs)
    assert any(b.customer == "Globex" and "Crash" in b.title or "Vocabulary" in b.title for b in bugs)

    assert len(features) == 2
    assert any(f.customer == "Acme Corp" and "workflow" in f.description.lower() for f in features)
    assert any(f.customer == "Globex" and "dark mode" in f.description.lower() for f in features)


def test_step_4_schedule_zoom_meetings(agent, sample_customers, sample_plan):
    """Test Zoom meeting scheduling based on customer engagement pattern."""
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)
    bugs, features = agent._step_3_monitor_and_log_issues(onboarded)
    sessions = agent._step_4_schedule_zoom_meetings(onboarded, bugs, features)

    assert len(sessions) == 3
    # Check session topics based on feedback
    assert any("Support" in s.notes[0] or "Support" in s.zoom_url or "Support" in s.session_id or s.customer_name == "Sarah Connor" for s in sessions)


def test_step_5_analyze_data(agent, sample_customers, sample_plan):
    """Test NLP theme extraction and success metrics calculation."""
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)
    bugs, features = agent._step_3_monitor_and_log_issues(onboarded)
    sessions = agent._step_4_schedule_zoom_meetings(onboarded, bugs, features)

    themes, metrics = agent._step_5_analyze_data(onboarded, bugs, features, sessions)

    assert len(themes) > 0
    assert "active_percentage" in metrics
    assert metrics["active_participants"] == 3
    assert metrics["total_bugs"] == 2
    assert metrics["total_features"] == 2
    assert metrics["total_zoom_sessions"] == 3


def test_step_6_compile_report(agent, sample_customers, sample_plan):
    """Test compiling comprehensive report in Markdown format."""
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)
    bugs, features = agent._step_3_monitor_and_log_issues(onboarded)
    sessions = agent._step_4_schedule_zoom_meetings(onboarded, bugs, features)
    themes, metrics = agent._step_5_analyze_data(onboarded, bugs, features, sessions)

    report = agent._step_6_compile_report(sample_plan, onboarded, bugs, features, sessions, themes, metrics)

    assert isinstance(report, BetaProgramReport)
    assert sample_plan.title in report.title
    assert "Acme Corp" in report.raw_markdown
    assert "Globex" in report.raw_markdown
    assert "Umbrella" in report.raw_markdown
    assert "identified bugs" in report.raw_markdown.lower()
    assert "proposed feature enhancements" in report.raw_markdown.lower()


def test_step_7_create_github_issue(agent, sample_customers, sample_plan):
    """Test creating a GitHub issue with compiled report content."""
    inputs = BetaAgentInputs(alpha_customers=sample_customers, stress_test_plan=sample_plan)
    onboarded = agent._step_2_send_invites(sample_customers, sample_plan)
    bugs, features = agent._step_3_monitor_and_log_issues(onboarded)
    sessions = agent._step_4_schedule_zoom_meetings(onboarded, bugs, features)
    themes, metrics = agent._step_5_analyze_data(onboarded, bugs, features, sessions)
    report = agent._step_6_compile_report(sample_plan, onboarded, bugs, features, sessions, themes, metrics)

    url = agent._step_7_create_github_issue(inputs, report)

    assert url
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc.endswith("github.com")


def test_full_execution(agent, sample_customers, sample_plan):
    """Test full agent execute method and return structures."""
    inputs = BetaAgentInputs(alpha_customers=sample_customers, stress_test_plan=sample_plan)
    outputs = agent.execute(inputs)

    assert isinstance(outputs, BetaAgentOutputs)
    assert outputs.report is not None
    assert outputs.github_issue_url.startswith("https://github.com/")
    assert len(outputs.report.bugs_identified) == 2
    assert len(outputs.report.feature_requests) == 2
