"""Tests for UsabilityTestAgent."""

import pytest
from urllib.parse import urlparse
from src.agents.usability_test_agent import (
    UsabilityTestAgent,
    AgentInputs,
    AgentOutputs,
    FrictionPoint,
    DesignIteration,
    UsabilityTestReport
)


@pytest.fixture
def sample_inputs():
    """Fixture providing realistic inputs for UsabilityTestAgent."""
    prototypes = [
        "https://www.figma.com/proto/mock1/PersonaScript-Brief-Builder",
        "https://www.figma.com/proto/mock2/PersonaScript-Persona-Config"
    ]
    target_user_profiles = {
        "title": "Director of Demand Generation / Content Lead",
        "company_size": "50-500 employees",
        "industry": "B2B SaaS"
    }
    test_script = [
        "Task 1: Complete Onboarding & Select Target Buyer Persona",
        "Task 2: Configure Tone and Generate Marketing Brief",
        "Task 3: Export Brief to HubSpot and Review Score"
    ]
    potential_users = [
        {"name": f"User {i+1}", "email": f"user{i+1}@saas.com", "role": "Marketing Leader"}
        for i in range(10)
    ]

    return AgentInputs(
        prototypes=prototypes,
        target_user_profiles=target_user_profiles,
        test_script=test_script,
        potential_users=potential_users
    )


class TestUsabilityTestAgent:
    """Tests for UsabilityTestAgent implementation."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = UsabilityTestAgent()
        assert agent is not None
        assert agent.maze is not None
        assert agent.zoom is not None
        assert agent.github is not None

    def test_execute_workflow(self, sample_inputs):
        """Test complete 7-step execution workflow."""
        agent = UsabilityTestAgent()
        outputs = agent.execute(sample_inputs)

        assert isinstance(outputs, AgentOutputs)
        assert outputs.status == "success"
        assert outputs.error_message is None

        # Verify report outputs
        report = outputs.usability_test_report
        assert isinstance(report, UsabilityTestReport)
        assert report.participant_count == 10
        assert "maze.co" in report.maze_test_link

        # Verify friction points and design iterations
        assert len(outputs.identified_friction_points) > 0
        assert len(outputs.proposed_design_iterations) > 0
        assert isinstance(outputs.identified_friction_points[0], FrictionPoint)
        assert isinstance(outputs.proposed_design_iterations[0], DesignIteration)

        # Verify GitHub issue URL
        assert outputs.github_issue_url
        parsed_url = urlparse(outputs.github_issue_url)
        assert parsed_url.scheme == "https"
        assert parsed_url.netloc.endswith("github.com")

        # Check execution log
        steps_logged = {entry["step"] for entry in agent.execution_log}
        assert steps_logged == {1, 2, 3, 4, 5, 6, 7}
        completed_entries = [e for e in agent.execution_log if e["status"] == "completed"]
        assert len(completed_entries) == 7

    def test_friction_point_analysis_and_iteration_mapping(self, sample_inputs):
        """Test that friction points properly generate design iterations."""
        agent = UsabilityTestAgent()
        outputs = agent.execute(sample_inputs)

        friction_ids = {fp.id for fp in outputs.identified_friction_points}
        iteration_mapped_ids = {di.friction_point_id for di in outputs.proposed_design_iterations}

        # Each friction point should have a corresponding design iteration
        assert friction_ids.issubset(iteration_mapped_ids)

    def test_error_handling(self, sample_inputs):
        """Test error handling during workflow execution."""
        agent = UsabilityTestAgent()
        # Cause exception by passing invalid object to maze.configure_test via mock
        agent.maze.configure_test = lambda *args, **kwargs: 1 / 0

        outputs = agent.execute(sample_inputs)
        assert outputs.status == "error"
        assert outputs.error_message is not None
        assert "division by zero" in outputs.error_message
