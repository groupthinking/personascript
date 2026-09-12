"""
Unit tests for BetaProgramManagerAgent and its associated integrations (Intercom, Zoom).
"""

import pytest
from unittest.mock import MagicMock

from src.integrations.intercom_integration import IntercomIntegration
from src.integrations.zoom_integration import ZoomIntegration
from src.agents.beta_program_manager_agent import (
    BetaProgramManagerAgent,
    AlphaCustomer,
    StressTestPlan,
    AgentInputs,
    AgentOutputs,
    ComprehensiveBetaReport
)


@pytest.fixture
def sample_alpha_customers():
    return [
        AlphaCustomer(
            id="cust-001",
            company_name="Acme Corp",
            contact_name="Alice Smith",
            contact_email="alice@acme.com",
            tier="Enterprise"
        ),
        AlphaCustomer(
            id="cust-002",
            company_name="TechStart Inc",
            contact_name="Bob Jones",
            contact_email="bob@techstart.io",
            tier="Growth"
        )
    ]


@pytest.fixture
def sample_stress_test_plan():
    return StressTestPlan(
        plan_id="plan-alpha-101",
        title="PersonaScript High-Volume Batch Generation Stress Test",
        target_concurrent_users=50,
        focus_areas=[
            "Concurrency and Rate Limiting",
            "SSO Authentication & Permissions",
            "Custom Persona JSON Export",
            "Brand Guideline Compliance Score Latency"
        ],
        duration_weeks=4,
        success_threshold_uptime_pct=99.5
    )


@pytest.fixture
def agent_inputs(sample_alpha_customers, sample_stress_test_plan):
    return AgentInputs(
        alpha_customers=sample_alpha_customers,
        stress_test_plan=sample_stress_test_plan,
        intercom_access_details={"app_id": "mock_app"},
        linear_access_details={"team": "ALPHA"},
        zoom_access_details={"account": "mock_account"}
    )


def test_intercom_integration_mock():
    """Test IntercomIntegration fallback/mock behavior."""
    intercom = IntercomIntegration()
    inv_res = intercom.send_invitation("test@example.com", "Test User", "https://example.com/onboard")
    assert inv_res["status"] == "sent"
    assert inv_res["recipient_email"] == "test@example.com"

    srv_res = intercom.send_survey("test@example.com", "Survey 1", ["Q1", "Q2"])
    assert srv_res["status"] == "dispatched"
    assert srv_res["question_count"] == 2

    feedback = intercom.fetch_feedback_and_conversations()
    assert len(feedback) > 0
    assert "conversation_id" in feedback[0]


def test_zoom_integration_mock():
    """Test ZoomIntegration fallback/mock behavior."""
    zoom = ZoomIntegration()
    session = zoom.schedule_session(
        topic="Feedback Call",
        start_time="2025-02-10T15:00:00Z",
        duration_minutes=30,
        participants=["user@example.com"],
        session_type="1:1"
    )
    assert session["status"] == "scheduled"
    assert "zoom.us" in session["join_url"]
    assert session["duration_minutes"] == 30


def test_beta_program_manager_agent_init():
    """Test BetaProgramManagerAgent initialization."""
    agent = BetaProgramManagerAgent(
        intercom_token="mock_ic",
        linear_token="mock_lin",
        zoom_token="mock_zm",
        github_token="mock_gh",
        github_repo="owner/repo"
    )
    assert agent.intercom.token == "mock_ic"
    assert agent.linear.token == "mock_lin"
    assert agent.zoom.token == "mock_zm"
    assert agent.github.token == "mock_gh"


def test_beta_program_manager_agent_execution(agent_inputs):
    """Test complete end-to-end execution of BetaProgramManagerAgent."""
    agent = BetaProgramManagerAgent()
    outputs = agent.execute(agent_inputs)

    assert isinstance(outputs, AgentOutputs)
    assert outputs.status == "success"
    assert isinstance(outputs.report, ComprehensiveBetaReport)
    assert len(outputs.report.customer_onboarding_status) == 2
    assert len(outputs.report.logged_bugs_and_features) > 0
    assert len(outputs.report.scheduled_zoom_sessions) == 3  # 2 1:1 sessions + 1 group session
    assert len(outputs.report.key_themes_and_feedback) > 0
    assert outputs.report.success_metrics["alpha_customer_participation_rate"] == 100.0
    assert outputs.github_issue_url != ""
    assert "https://github.com" in outputs.github_issue_url


def test_beta_program_manager_agent_exception_handling(agent_inputs):
    """Test agent fallback when an exception occurs during execution."""
    agent = BetaProgramManagerAgent()
    # Force error by passing invalid alpha_customers type
    invalid_inputs = AgentInputs(
        alpha_customers=None,  # type: ignore
        stress_test_plan=agent_inputs.stress_test_plan
    )

    outputs = agent.execute(invalid_inputs)
    assert outputs.status == "error"
    assert outputs.error_message is not None
    assert "NoneType" in outputs.error_message or "TypeError" in outputs.error_message or "object is not iterable" in outputs.error_message
