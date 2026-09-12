"""
Unit tests for PersonaScriptInternalToolSetupAgent and SlackIntegration.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.integrations.slack_integration import SlackIntegration
from src.integrations.linear_integration import LinearIntegration
from src.integrations.notion_integration import NotionIntegration
from src.integrations.github_integration import GitHubIntegration
from src.agents.internal_tool_setup_agent import (
    PersonaScriptInternalToolSetupAgent,
    ProjectSetupRequest,
    AgentOutputs
)


def test_slack_integration_mock_fallback():
    """Test SlackIntegration when no API tokens are provided."""
    slack = SlackIntegration()
    assert not slack.is_configured()

    # Test channel creation fallback
    channel_info = slack.create_channel("general-test")
    assert channel_info["name"] == "general-test"
    assert "slack.com/app_redirect" in channel_info["url"]

    # Test invite members fallback
    invite_info = slack.invite_members("C12345", ["alice@example.com", "bob@example.com"])
    assert invite_info["channel_id"] == "C12345"
    assert len(invite_info["invited_members"]) == 2

    # Test setup project channels
    ch_urls = slack.setup_project_channels("PersonaScript MVP", ["alice@example.com"])
    assert "#general-personascript-mvp" in ch_urls
    assert "#dev-personascript-mvp" in ch_urls
    assert "#marketing-personascript-mvp" in ch_urls


def test_linear_integration_setup_project():
    """Test LinearIntegration team, project, and sprint setup."""
    linear = LinearIntegration()
    res = linear.setup_project(
        project_name="PersonaScript Core",
        team_members=["alice@example.com"],
        initial_sprint_duration_weeks=3
    )

    assert res["team"]["name"] == "PersonaScript Core Team"
    assert "linear.app/personascript/team" in res["team_url"]
    assert res["project"]["name"] == "PersonaScript Core"
    assert "linear.app/personascript/project" in res["project_url"]
    assert res["sprint"]["duration_weeks"] == 3


def test_notion_integration_setup_workspace_pages():
    """Test NotionIntegration workspace page hierarchy setup."""
    notion = NotionIntegration()
    pages = notion.setup_workspace_pages("PersonaScript Alpha")

    assert "PersonaScript Alpha - Home" in pages
    assert "PersonaScript Alpha - Documentation" in pages
    assert "PersonaScript Alpha - Meetings" in pages
    for url in pages.values():
        assert "notion.so" in url


def test_internal_tool_setup_agent_full_workflow():
    """Test complete execution of PersonaScriptInternalToolSetupAgent."""
    agent = PersonaScriptInternalToolSetupAgent()

    request = ProjectSetupRequest(
        project_name="PersonaScript Engine",
        team_members=["sarah@company.com", "alex@company.com"],
        initial_sprint_duration_weeks=2
    )

    outputs = agent.execute(request)

    assert outputs.status == "success"
    assert outputs.linear_project_url.startswith("https://linear.app/")
    assert outputs.linear_team_url.startswith("https://linear.app/")

    assert len(outputs.slack_channel_urls) >= 3
    assert "#general-personascript-engine" in outputs.slack_channel_urls

    assert len(outputs.notion_page_urls) >= 3
    assert "PersonaScript Engine - Home" in outputs.notion_page_urls

    assert outputs.github_issue_url.startswith("https://github.com/")

    # Check summary content
    assert "PersonaScript Engine" in outputs.summary
    assert "sarah@company.com" in outputs.summary
    assert "2 weeks" in outputs.summary


def test_internal_tool_setup_agent_error_handling():
    """Test error handling in PersonaScriptInternalToolSetupAgent."""
    agent = PersonaScriptInternalToolSetupAgent()

    request = ProjectSetupRequest(
        project_name="Test Fail Project",
        team_members=["test@example.com"]
    )

    # Force error by mocking Linear setup_project to raise an exception
    with patch.object(LinearIntegration, "setup_project", side_effect=Exception("Linear API error")):
        outputs = agent.execute(request)
        assert outputs.status == "error"
        assert "Linear API error" in outputs.error_message
