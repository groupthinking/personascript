"""
Unit tests for CICDPipelineArchitectAgent.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.agents.cicd_pipeline_architect_agent import (
    CICDPipelineArchitectAgent,
    CICDPipelineInputs,
    CICDPipelineOutputs
)


def test_cicd_pipeline_architect_agent_init():
    agent = CICDPipelineArchitectAgent(
        github_token="fake-token",
        github_repo="owner/repo"
    )
    assert agent.github_token == "fake-token"
    assert agent.github_repo == "owner/repo"


@patch("src.agents.cicd_pipeline_architect_agent.GitHubIntegration")
def test_cicd_pipeline_architect_agent_execute_success(mock_github_cls):
    mock_github_instance = MagicMock()
    mock_github_instance.create_issue.return_value = "https://github.com/owner/repo/issues/101"
    mock_github_cls.return_value = mock_github_instance

    agent = CICDPipelineArchitectAgent(
        github_token="fake-token",
        github_repo="owner/repo"
    )

    inputs = CICDPipelineInputs(
        business_context="Custom B2B context",
        task_to_automate="Custom automation task",
        target_platform="GitHub Actions"
    )

    outputs = agent.execute(inputs)

    assert outputs.status == "success"
    assert outputs.github_issue_url == "https://github.com/owner/repo/issues/101"
    assert "Frontend CI/CD Pipeline" in outputs.frontend_pipeline_yaml
    assert "Backend CI/CD Pipeline" in outputs.backend_pipeline_yaml
    assert "AI & ML Services CI/CD Pipeline" in outputs.ai_pipeline_yaml

    mock_github_instance.create_issue.assert_called_once()
    call_kwargs = mock_github_instance.create_issue.call_args[1]
    assert "CI/CD Pipeline Blueprint" in call_kwargs["title"]
    assert "Custom B2B context" in call_kwargs["body"]
    assert "Frontend CI/CD Workflow" in call_kwargs["body"]
    assert "Backend CI/CD Workflow" in call_kwargs["body"]
    assert "AI & ML Services CI/CD Workflow" in call_kwargs["body"]


@patch("src.agents.cicd_pipeline_architect_agent.GitHubIntegration")
def test_cicd_pipeline_architect_agent_execute_default_inputs(mock_github_cls):
    mock_github_instance = MagicMock()
    mock_github_instance.create_issue.return_value = "https://github.com/owner/repo/issues/102"
    mock_github_cls.return_value = mock_github_instance

    agent = CICDPipelineArchitectAgent()
    outputs = agent.execute()

    assert outputs.status == "success"
    assert outputs.github_issue_url == "https://github.com/owner/repo/issues/102"
    assert outputs.frontend_pipeline_yaml != ""
    assert outputs.backend_pipeline_yaml != ""
    assert outputs.ai_pipeline_yaml != ""


@patch("src.agents.cicd_pipeline_architect_agent.GitHubIntegration")
def test_cicd_pipeline_architect_agent_execute_error_handling(mock_github_cls):
    mock_github_instance = MagicMock()
    mock_github_instance.create_issue.side_effect = Exception("GitHub API Error")
    mock_github_cls.return_value = mock_github_instance

    agent = CICDPipelineArchitectAgent()
    outputs = agent.execute()

    assert outputs.status == "error"
    assert outputs.github_issue_url == ""
    assert outputs.error_message == "GitHub API Error"
