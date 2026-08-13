"""
Unit tests for PersonaScriptInternalToolSetupAgent and associated integrations.
"""

import pytest
from urllib.parse import urlparse
from src.integrations.linear_integration import LinearIntegration
from src.integrations.slack_integration import SlackIntegration
from src.integrations.notion_integration import NotionIntegration
from src.agents.internal_tool_setup_agent import (
    PersonaScriptInternalToolSetupAgent,
    ProjectSetupRequest,
    AgentInputs,
    AgentOutputs
)


class TestLinearIntegration:
    """Tests for LinearIntegration."""

    def test_create_team(self):
        integration = LinearIntegration()
        team = integration.create_team("Marketing Launch Team", ["alice@example.com", "bob@example.com"])

        assert team["id"].startswith("team-")
        assert team["name"] == "Marketing Launch Team"
        assert team["key"] == "MLT"
        assert "alice@example.com" in team["members"]
        assert "marketing-launch-team" not in team["key"]
        assert "https://linear.app/personascript/team/mlt" == team["url"]

    def test_create_team_short_name(self):
        integration = LinearIntegration()
        team = integration.create_team("AI", ["alice@example.com"])
        assert team["key"] == "AIX"

    def test_create_project(self):
        integration = LinearIntegration()
        project = integration.create_project("team-123", "MLT", "Beta Release", ["alice@example.com"])

        assert project["id"].startswith("proj-")
        assert project["name"] == "Beta Release"
        assert project["url"] == "https://linear.app/personascript/team/mlt/project/beta-release"

    def test_create_sprints(self):
        integration = LinearIntegration()
        sprints = integration.create_sprints("proj-123", sprint_duration_weeks=2, count=3)

        assert len(sprints) == 3
        assert sprints[0]["name"] == "Sprint 1"
        assert sprints[0]["duration_weeks"] == 2
        assert sprints[1]["name"] == "Sprint 2"
        assert sprints[2]["name"] == "Sprint 3"


class TestSlackIntegration:
    """Tests for SlackIntegration."""

    def test_sluggify(self):
        integration = SlackIntegration()
        assert integration.sluggify("Project Alpha!") == "project-alpha"
        assert integration.sluggify("Super_Duper   Space") == "super-duper-space"
        assert integration.sluggify("---Hello World---") == "hello-world"

    def test_create_channel(self):
        integration = SlackIntegration()
        channel = integration.create_channel("#dev-chat", ["alice", "bob"])

        assert channel["id"].startswith("C")
        assert channel["name"] == "#dev-chat"
        assert channel["invited_members"] == ["alice", "bob"]
        assert "https://personascript.slack.com/archives/" in channel["url"]

    def test_create_project_channels(self):
        integration = SlackIntegration()
        channels = integration.create_project_channels("Project Alpha", ["alice", "bob"])

        assert "general" in channels
        assert "dev" in channels
        assert "marketing" in channels

        assert channels["general"]["name"] == "#general-project-alpha"
        assert channels["dev"]["name"] == "#project-alpha-dev"
        assert channels["marketing"]["name"] == "#project-alpha-marketing"


class TestNotionIntegration:
    """Tests for NotionIntegration."""

    def test_create_page(self):
        integration = NotionIntegration()
        page = integration.create_page("Test Document", permissions={"role": "admin"})

        assert page["id"]
        assert page["title"] == "Test Document"
        assert page["permissions"] == {"role": "admin"}
        assert "Test-Document" in page["url"]

    def test_create_project_workspace(self):
        integration = NotionIntegration()
        workspace = integration.create_project_workspace("Project Delta")

        assert "home" in workspace
        assert "docs" in workspace
        assert "meetings" in workspace

        assert workspace["home"]["title"] == "Project Delta - Home"
        assert workspace["docs"]["title"] == "Project Delta - Documentation"
        assert workspace["meetings"]["title"] == "Project Delta - Meetings"

        assert workspace["docs"]["parent_id"] == workspace["home"]["id"]
        assert workspace["meetings"]["parent_id"] == workspace["home"]["id"]


class TestPersonaScriptInternalToolSetupAgent:
    """Tests for PersonaScriptInternalToolSetupAgent."""

    def test_agent_initialization(self):
        agent = PersonaScriptInternalToolSetupAgent(
            linear_api_key="lin_123",
            slack_api_token="xoxb-123",
            notion_api_key="secret_123",
            github_token="gh_123",
            github_repo="test/repo"
        )
        assert agent.linear_api_key == "lin_123"
        assert agent.slack_api_token == "xoxb-123"
        assert agent.notion_api_key == "secret_123"
        assert agent.github_token == "gh_123"
        assert agent.github_repo == "test/repo"

    def test_parse_setup_request_valid(self):
        agent = PersonaScriptInternalToolSetupAgent()
        req = ProjectSetupRequest(
            project_name="Project Gamma",
            team_members=["alice", "bob"],
            sprint_duration_weeks=3,
            specific_configs={"foo": "bar"}
        )
        parsed = agent._parse_setup_request(req)

        assert parsed["project_name"] == "Project Gamma"
        assert parsed["team_members"] == ["alice", "bob"]
        assert parsed["sprint_duration_weeks"] == 3
        assert parsed["specific_configs"] == {"foo": "bar"}

    def test_parse_setup_request_empty_name(self):
        agent = PersonaScriptInternalToolSetupAgent()
        req = ProjectSetupRequest(
            project_name="   ",
            team_members=["alice"]
        )
        with pytest.raises(ValueError, match="Project name must not be empty"):
            agent._parse_setup_request(req)

    def test_execute_flow(self):
        agent = PersonaScriptInternalToolSetupAgent(
            github_repo="groupthinking/personascript"
        )
        req = ProjectSetupRequest(
            project_name="Mars Colonization",
            team_members=["elon", "grimes"],
            sprint_duration_weeks=2
        )
        inputs = AgentInputs(
            setup_request=req,
            linear_api_key="lin_key",
            slack_api_token="slack_token",
            notion_api_key="notion_key",
            github_token="gh_token"
        )

        outputs = agent.execute(inputs)

        assert outputs.linear_team_id
        assert outputs.linear_project_id
        assert "linear.app" in outputs.linear_project_url

        assert "general" in outputs.slack_channel_urls
        assert "dev" in outputs.slack_channel_urls
        assert "marketing" in outputs.slack_channel_urls

        assert "home" in outputs.notion_page_urls
        assert "docs" in outputs.notion_page_urls
        assert "meetings" in outputs.notion_page_urls

        # Verify Github Issue URL is a mock URL with correct format
        assert "github.com/groupthinking/personascript/issues/" in outputs.github_issue_url

        # Verify summary details
        assert "Mars Colonization" in outputs.summary
        assert "elon, grimes" in outputs.summary
        assert "Sprint 1" in outputs.summary
