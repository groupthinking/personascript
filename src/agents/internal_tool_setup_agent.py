"""
PersonaScriptInternalToolSetupAgent

Automates the initial setup of internal project management, communication,
and documentation tools (Linear, Slack, Notion) for PersonaScript projects,
publishing a comprehensive summary tracking issue to GitHub.
"""

import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.linear_integration import LinearIntegration
from ..integrations.slack_integration import SlackIntegration
from ..integrations.notion_integration import NotionIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ProjectSetupRequest:
    """Request data for configuring project tools."""

    project_name: str
    team_members: List[str]
    initial_sprint_duration_weeks: int = 2
    linear_token: Optional[str] = None
    slack_token: Optional[str] = None
    notion_token: Optional[str] = None
    github_token: Optional[str] = None
    github_repo: Optional[str] = None


# Alias for AgentInputs
AgentInputs = ProjectSetupRequest


@dataclass
class AgentOutputs:
    """Output data from PersonaScriptInternalToolSetupAgent."""

    linear_project_url: str
    linear_team_url: str
    slack_channel_urls: Dict[str, str]
    notion_page_urls: Dict[str, str]
    github_issue_url: str
    summary: str
    status: str = "success"
    error_message: Optional[str] = None


class PersonaScriptInternalToolSetupAgent:
    """
    Agent responsible for automating the setup of internal tools (Linear, Slack, Notion)
    for PersonaScript projects and documenting the result via GitHub.
    """

    def __init__(
        self,
        linear_token: Optional[str] = None,
        slack_token: Optional[str] = None,
        notion_token: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize agent with optional default API keys or environment fallbacks.
        """
        self.linear_token = linear_token or os.environ.get("LINEAR_API_KEY")
        self.slack_token = slack_token or os.environ.get("SLACK_BOT_TOKEN")
        self.notion_token = notion_token or os.environ.get("NOTION_API_KEY")
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.github_repo = github_repo or os.environ.get("GITHUB_REPO", "groupthinking/personascript")

        logger.info("PersonaScriptInternalToolSetupAgent initialized")

    def execute(self, inputs: ProjectSetupRequest) -> AgentOutputs:
        """
        Execute the 6-step internal tool setup execution plan.

        Args:
            inputs: ProjectSetupRequest containing setup parameters.

        Returns:
            AgentOutputs containing direct URLs to all configured resources and GitHub issue.
        """
        logger.info(f"Starting internal tool setup for project: '{inputs.project_name}'")

        try:
            # Step 1: Receive and parse the 'Project Setup Request'
            parsed_request = self._parse_request(inputs)

            # Resolve API tokens (inputs override default tokens)
            linear_tok = inputs.linear_token or self.linear_token
            slack_tok = inputs.slack_token or self.slack_token
            notion_tok = inputs.notion_token or self.notion_token
            github_tok = inputs.github_token or self.github_token
            github_rp = inputs.github_repo or self.github_repo

            # Initialize integrations
            linear_integ = LinearIntegration(token=linear_tok)
            slack_integ = SlackIntegration(token=slack_tok)
            notion_integ = NotionIntegration(token=notion_tok)
            github_integ = GitHubIntegration(token=github_tok, repo=github_rp)

            # Step 2: Configure Linear
            linear_res = self._configure_linear(linear_integ, parsed_request)

            # Step 3: Configure Slack
            slack_urls = self._configure_slack(slack_integ, parsed_request)

            # Step 4: Configure Notion
            notion_urls = self._configure_notion(notion_integ, parsed_request)

            # Step 5: Compile comprehensive summary
            summary = self._compile_summary(
                parsed_request=parsed_request,
                linear_res=linear_res,
                slack_urls=slack_urls,
                notion_urls=notion_urls
            )

            # Step 6: Create GitHub issue summarizing the setup
            github_issue_url = self._create_github_issue(
                github_integ=github_integ,
                parsed_request=parsed_request,
                linear_res=linear_res,
                slack_urls=slack_urls,
                notion_urls=notion_urls,
                summary=summary
            )

            logger.info(f"Internal tool setup for '{inputs.project_name}' completed successfully.")
            return AgentOutputs(
                linear_project_url=linear_res["project_url"],
                linear_team_url=linear_res["team_url"],
                slack_channel_urls=slack_urls,
                notion_page_urls=notion_urls,
                github_issue_url=github_issue_url,
                summary=summary,
                status="success"
            )

        except Exception as e:
            logger.error(f"Error during internal tool setup: {e}", exc_info=True)
            return AgentOutputs(
                linear_project_url="",
                linear_team_url="",
                slack_channel_urls={},
                notion_page_urls={},
                github_issue_url="",
                summary=f"Setup failed: {str(e)}",
                status="error",
                error_message=str(e)
            )

    def _parse_request(self, inputs: ProjectSetupRequest) -> Dict[str, Any]:
        """
        Step 1: Parse and validate the Project Setup Request.
        """
        logger.info("Step 1: Parsing Project Setup Request")
        project_name = inputs.project_name.strip()
        team_members = [m.strip() for m in inputs.team_members if m.strip()]
        duration = inputs.initial_sprint_duration_weeks if inputs.initial_sprint_duration_weeks > 0 else 2

        return {
            "project_name": project_name,
            "team_members": team_members,
            "initial_sprint_duration_weeks": duration
        }

    def _configure_linear(self, linear_integ: LinearIntegration, parsed_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Configure Linear (Team, Project, Sprints, Member Assignments).
        """
        logger.info("Step 2: Configuring Linear")
        project_name = parsed_request["project_name"]
        team_members = parsed_request["team_members"]
        sprint_duration = parsed_request["initial_sprint_duration_weeks"]

        return linear_integ.setup_project(
            project_name=project_name,
            team_members=team_members,
            initial_sprint_duration_weeks=sprint_duration
        )

    def _configure_slack(self, slack_integ: SlackIntegration, parsed_request: Dict[str, Any]) -> Dict[str, str]:
        """
        Step 3: Configure Slack channels and invite team members.
        """
        logger.info("Step 3: Configuring Slack channels")
        project_name = parsed_request["project_name"]
        team_members = parsed_request["team_members"]

        return slack_integ.setup_project_channels(
            project_name=project_name,
            team_members=team_members
        )

    def _configure_notion(self, notion_integ: NotionIntegration, parsed_request: Dict[str, Any]) -> Dict[str, str]:
        """
        Step 4: Configure Notion top-level pages and permissions.
        """
        logger.info("Step 4: Configuring Notion workspace pages")
        project_name = parsed_request["project_name"]

        return notion_integ.setup_workspace_pages(
            project_name=project_name
        )

    def _compile_summary(
        self,
        parsed_request: Dict[str, Any],
        linear_res: Dict[str, Any],
        slack_urls: Dict[str, str],
        notion_urls: Dict[str, str]
    ) -> str:
        """
        Step 5: Compile a comprehensive summary of all configured tools.
        """
        logger.info("Step 5: Compiling summary of configured tools")
        project_name = parsed_request["project_name"]
        team_members = ", ".join(parsed_request["team_members"])
        sprint_duration = parsed_request["initial_sprint_duration_weeks"]

        slack_links = "\n".join([f"- **{ch}**: [{url}]({url})" for ch, url in slack_urls.items()])
        notion_links = "\n".join([f"- **{page}**: [{url}]({url})" for page, url in notion_urls.items()])

        summary_lines = [
            f"### Internal Tool Setup Summary for {project_name}",
            f"- **Team Members Configured**: {team_members}",
            f"- **Initial Sprint Duration**: {sprint_duration} weeks",
            "",
            "#### 🎯 Linear Project Management",
            f"- **Team**: [{linear_res['team']['name']}]({linear_res['team_url']}) (Key: `{linear_res['team']['key']}`, ID: `{linear_res['team']['id']}`)",
            f"- **Project**: [{linear_res['project']['name']}]({linear_res['project_url']}) (ID: `{linear_res['project']['id']}`)",
            f"- **Initial Sprint**: {linear_res['sprint']['name']} (ID: `{linear_res['sprint']['id']}`)",
            "",
            "#### 💬 Slack Communication Channels",
            slack_links,
            "",
            "#### 📄 Notion Documentation Workspace",
            notion_links
        ]

        return "\n".join(summary_lines)

    def _create_github_issue(
        self,
        github_integ: GitHubIntegration,
        parsed_request: Dict[str, Any],
        linear_res: Dict[str, Any],
        slack_urls: Dict[str, str],
        notion_urls: Dict[str, str],
        summary: str
    ) -> str:
        """
        Step 6: Create a new GitHub issue in designated repository detailing the completed setup.
        """
        logger.info("Step 6: Publishing GitHub summary issue")
        project_name = parsed_request["project_name"]
        title = f"Internal Tool Setup for {project_name} Completed"

        team_members_str = ", ".join(parsed_request["team_members"])
        slack_outputs_str = ", ".join([f"`{ch}`" for ch in slack_urls.keys()])
        notion_outputs_str = ", ".join([f"`{p}`" for p in notion_urls.keys()])

        body = f"""# {title}

## Goal
Automate the initial setup of internal project management, communication, and documentation tools (Linear, Slack, Notion) for PersonaScript.

## Inputs
- **Project Name**: `{project_name}`
- **Team Members**: `{team_members_str}`
- **Initial Sprint Duration**: `{parsed_request['initial_sprint_duration_weeks']} weeks`

## Outputs
- **Linear Team/Project**: [{linear_res['project']['name']}]({linear_res['project_url']})
- **Slack Channels Created**: {slack_outputs_str}
- **Notion Pages Configured**: {notion_outputs_str}

## Execution Plan Executed
1. 🧠 **Receive and Parse Request**: Parsed project request parameters for `{project_name}` and team members.
2. 🎯 **Configure Linear**: Created Linear Team (`{linear_res['team']['name']}`), Project (`{linear_res['project']['name']}`), and initial `{parsed_request['initial_sprint_duration_weeks']}-week` Sprint cycle.
3. 💬 **Configure Slack**: Created predefined Slack channels ({slack_outputs_str}) and invited assigned team members.
4. 📄 **Configure Notion**: Created top-level workspace pages ({notion_outputs_str}) with initial permissions.
5. 📊 **Compile Summary**: Formatted links, IDs, and access details across all configured platforms.
6. 🚀 **Publish GitHub Issue**: Published this comprehensive issue for setup tracking and team visibility.

---

## Tool Configuration Summary & Direct Links
{summary}
"""

        issue_url = github_integ.create_issue(
            title=title,
            body=body,
            labels=["internal-setup", "tooling", "completed"]
        )

        logger.info(f"Published GitHub summary issue: {issue_url}")
        return issue_url
