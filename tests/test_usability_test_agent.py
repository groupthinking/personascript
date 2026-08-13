"""
Unit tests for UsabilityTestAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.usability_test_agent import (
    UsabilityTestAgent,
    UsabilityTestInputs,
    UsabilityTestOutputs
)


@pytest.fixture
def sample_usability_inputs():
    """Create sample input data for testing UsabilityTestAgent."""
    potential_users = [
        {"name": f"Tester {i}", "email": f"tester{i}@b2bsaas.com", "role": "Marketing Director"}
        for i in range(1, 11)  # 10 potential users
    ]
    return UsabilityTestInputs(
        prototypes=["https://www.figma.com/proto/test1", "https://www.invisionapp.com/proto/test2"],
        target_user_profiles={
            "role": "Marketing Director / VP of Marketing",
            "experience": "5-10 years",
            "industry": "B2B SaaS"
        },
        test_script={
            "scenarios": ["Scenario 1: Generate a brand-aligned email campaign", "Scenario 2: Set up a new persona"],
            "questions": ["How easy was it to generate content?", "Were there any parts where you felt stuck?"]
        },
        potential_users=potential_users
    )


@pytest.fixture
def agent():
    """Create an agent instance for testing."""
    return UsabilityTestAgent()


def test_agent_initialization():
    """Test that agent initializes correctly with all required integrations."""
    agent = UsabilityTestAgent()
    assert agent is not None
    assert agent.maze_integration is not None
    assert agent.zoom_integration is not None
    assert agent.google_docs_integration is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with explicit credentials."""
    agent = UsabilityTestAgent(
        maze_api_key="maze_key",
        zoom_credentials={"api_key": "zoom_key"},
        google_docs_credentials={"type": "service_account"},
        github_token="github_token",
        github_repo="owner/repo"
    )
    assert agent.maze_integration.api_key == "maze_key"
    assert agent.zoom_integration.credentials == {"api_key": "zoom_key"}
    assert agent.google_docs_integration.credentials is not None
    assert agent.github_integration.token == "github_token"
    assert agent.github_integration.repo == "owner/repo"


def test_maze_configuration(agent, sample_usability_inputs):
    """Test Maze test configuration step."""
    test_link = agent.maze_integration.configure_usability_test(
        prototypes=sample_usability_inputs.prototypes,
        test_script=sample_usability_inputs.test_script
    )
    assert test_link
    parsed = urlparse(test_link)
    assert parsed.scheme == "https"
    assert parsed.netloc == "t.maze.co"


def test_zoom_sessions_scheduling(agent, sample_usability_inputs):
    """Test scheduling sessions via Zoom."""
    test_link = "https://t.maze.co/123456"
    sessions = agent.zoom_integration.schedule_sessions(
        potential_users=sample_usability_inputs.potential_users,
        test_link=test_link
    )

    assert len(sessions) == 10
    assert all(s["status"] == "scheduled" for s in sessions)
    assert all("meeting_url" in s for s in sessions)
    assert all(s["maze_test_link"] == test_link for s in sessions)


def test_friction_points_and_iterations_analysis(agent):
    """Test data aggregation, friction points identification and design proposal generation."""
    maze_data = {
        "total_testers": 10,
        "misclick_rate": 0.18,          # >10%
        "direct_success_rate": 0.75,    # <90%
        "bounce_rate": 0.05
    }
    zoom_feedback = [
        {"session_id": "1", "observations": ["User struggled to locate the main CTA on the landing page initially."]},
        {"session_id": "2", "observations": ["Confused by the 'advanced settings' section of the template creation flow."]}
    ]

    aggregated = agent._aggregate_data(maze_data, zoom_feedback)
    assert aggregated["total_sessions"] == 2
    assert len(aggregated["observations"]) == 2

    friction_points = agent._identify_friction_points(aggregated)
    assert len(friction_points) == 4

    fp_issues = [fp["issue"] for fp in friction_points]
    assert "High Misclick Rate" in fp_issues
    assert "Suboptimal Task Direct Success Rate" in fp_issues
    assert "CTA Prominence and Layout Location Confusion" in fp_issues
    assert "Advanced Settings Flow Cognitive Overload" in fp_issues

    proposals = agent._propose_design_iterations(friction_points)
    assert len(proposals) == 4

    priorities = [p["priority"] for p in proposals]
    assert "Critical" in priorities
    assert "High" in priorities
    assert "Medium" in priorities


def test_create_usability_report_doc(agent, sample_usability_inputs):
    """Test the document generation for Usability Test Report."""
    maze_data = {
        "total_testers": 10,
        "misclick_rate": 0.15,
        "direct_success_rate": 0.80,
        "bounce_rate": 0.10,
        "average_time_spent_seconds": 120.0
    }
    friction_points = [
        {"id": "FP-1", "issue": "High Misclick Rate", "description": "Too high", "source": "Maze"}
    ]
    proposed_iterations = [
        {"friction_point_id": "FP-1", "proposed_change": "Enlarge button target", "priority": "High", "impact": "Better"}
    ]

    doc_url = agent._create_usability_report_doc(
        inputs=sample_usability_inputs,
        maze_data=maze_data,
        friction_points=friction_points,
        proposed_iterations=proposed_iterations
    )

    assert doc_url
    parsed = urlparse(doc_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "docs.google.com"


def test_create_github_issue(agent, sample_usability_inputs):
    """Test GitHub issue content generation for usability testing runs."""
    maze_data = {
        "total_testers": 10,
        "misclick_rate": 0.12,
        "direct_success_rate": 0.85,
        "bounce_rate": 0.10,
        "average_time_spent_seconds": 110.0
    }
    report_url = "https://docs.google.com/document/d/mock-report/edit"
    friction_points = [
        {"id": "FP-1", "issue": "High Misclick Rate", "description": "Too high", "source": "Maze"}
    ]
    proposed_iterations = [
        {"friction_point_id": "FP-1", "proposed_change": "Enlarge target", "priority": "High", "impact": "Better"}
    ]

    github_url = agent._create_github_issue(
        inputs=sample_usability_inputs,
        maze_data=maze_data,
        report_url=report_url,
        friction_points=friction_points,
        proposed_iterations=proposed_iterations
    )

    assert github_url
    parsed = urlparse(github_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "github.com"
    assert "issues" in parsed.path


def test_full_agent_execution(agent, sample_usability_inputs):
    """Test full execute workflow of UsabilityTestAgent."""
    outputs = agent.execute(sample_usability_inputs)

    assert isinstance(outputs, UsabilityTestOutputs)
    assert outputs.usability_test_report_url
    assert len(outputs.identified_friction_points) > 0
    assert len(outputs.proposed_design_iterations) > 0
    assert outputs.github_issue_url

    # URL parsed validation
    parsed_report = urlparse(outputs.usability_test_report_url)
    assert parsed_report.scheme == "https"
    assert parsed_report.netloc == "docs.google.com"

    parsed_issue = urlparse(outputs.github_issue_url)
    assert parsed_issue.scheme == "https"
    assert parsed_issue.netloc == "github.com"
