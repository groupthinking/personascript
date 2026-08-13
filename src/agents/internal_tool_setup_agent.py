"""
PersonaScriptInternalToolSetupAgent - Agent for automating setup of Linear, Slack, Notion, and GitHub.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..integrations.linear_integration import LinearIntegration
from ..integrations.slack_integration import SlackIntegration
from ..integrations.notion_integration import NotionIntegration
from ..integrations.github_integration import GitHubIntegration

logger = logging.getLogger(__name__)


@dataclass
class ProjectSetupRequest:
    """Represents a request to set up internal project tools."""

    project_name: str
    team_members: List[str]
    sprint_duration_weeks: int = 2
    specific_configs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentInputs:
    """Input data for the PersonaScriptInternalToolSetupAgent."""

    setup_request: ProjectSetupRequest
    linear_api_key: Optional[str] = None
    slack_api_token: Optional[str] = None
    notion_api_key: Optional[str] = None
    github_token: Optional[str] = None
    github_repo: Optional[str] = None


@dataclass
class AgentOutputs:
    """Output data from the PersonaScriptInternalToolSetupAgent."""

    linear_team_id: str
    linear_project_id: str
    linear_project_url: str
    slack_channel_urls: Dict[str, str]
    notion_page_urls: Dict[str, str]
    github_issue_url: str
    summary: str


class PersonaScriptInternalToolSetupAgent:
    """
    Main agent class for automating the setup of internal tools for PersonaScript projects.

    This agent follows a 6-step execution plan:
    1. Parse the 'Project Setup Request'
    2. Configure Linear (team, project, sprints, assign members)
    3. Configure Slack (channels, invite members)
    4. Configure Notion (workspace/pages, permissions)
    5. Compile a comprehensive summary of all configured tools
    6. Create a new GitHub issue in the repository summarizing the setup
    """

    def __init__(
        self,
        linear_api_key: Optional[str] = None,
        slack_api_token: Optional[str] = None,
        notion_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        github_repo: Optional[str] = None
    ):
        """
        Initialize the setup agent.
        """
        self.linear_api_key = linear_api_key
        self.slack_api_token = slack_api_token
        self.notion_api_key = notion_api_key
        self.github_token = github_token
        self.github_repo = github_repo or "groupthinking/personascript"

        logger.info("PersonaScriptInternalToolSetupAgent initialized")

    def execute(self, inputs: AgentInputs) -> AgentOutputs:
        """
        Execute the complete setup workflow.

        Args:
            inputs: AgentInputs containing ProjectSetupRequest and credentials.

        Returns:
            AgentOutputs containing URLs and configuration details.
        """
        logger.info("Starting PersonaScriptInternalToolSetupAgent execution")

        # Merge API keys/tokens from inputs or initialization
        linear_key = inputs.linear_api_key or self.linear_api_key
        slack_token = inputs.slack_api_token or self.slack_api_token
        notion_key = inputs.notion_api_key or self.notion_api_key
        gh_token = inputs.github_token or self.github_token
        gh_repo = inputs.github_repo or self.github_repo

        # Initialize integrations
        linear_integration = LinearIntegration(api_key=linear_key)
        slack_integration = SlackIntegration(api_token=slack_token)
        notion_integration = NotionIntegration(api_key=notion_key)
        github_integration = GitHubIntegration(token=gh_token, repo=gh_repo)

        # Step 1: Parse Project Setup Request
        parsed_config = self._parse_setup_request(inputs.setup_request)

        # Step 2: Configure Linear
        linear_results = self._configure_linear(linear_integration, parsed_config)

        # Step 3: Configure Slack
        slack_results = self._configure_slack(slack_integration, parsed_config)

        # Step 4: Configure Notion
        notion_results = self._configure_notion(notion_integration, parsed_config)

        # Step 5: Compile a comprehensive summary
        summary = self._compile_summary(
            parsed_config,
            linear_results,
            slack_results,
            notion_results
        )

        # Step 6: Create GitHub Issue
        github_issue_url = self._create_github_issue(
            github_integration,
            parsed_config,
            inputs,
            linear_results,
            slack_results,
            notion_results,
            summary
        )

        outputs = AgentOutputs(
            linear_team_id=linear_results["team"]["id"],
            linear_project_id=linear_results["project"]["id"],
            linear_project_url=linear_results["project"]["url"],
            slack_channel_urls={k: v["url"] for k, v in slack_results["channels"].items()},
            notion_page_urls={k: v["url"] for k, v in notion_results["pages"].items()},
            github_issue_url=github_issue_url,
            summary=summary
        )

        logger.info("PersonaScriptInternalToolSetupAgent execution completed successfully")
        return outputs

    def _parse_setup_request(self, request: ProjectSetupRequest) -> Dict[str, Any]:
        """
        Step 1: Parse the Project Setup Request to extract project parameters.
        """
        logger.info("Step 1: Parsing setup request")

        project_name = request.project_name.strip()
        if not project_name:
            raise ValueError("Project name must not be empty.")

        team_members = [m.strip() for m in request.team_members if m.strip()]
        sprint_duration = max(1, request.sprint_duration_weeks)

        logger.info(f"Parsed parameters - Name: '{project_name}', Members: {team_members}, Sprint Duration: {sprint_duration} weeks")

        return {
            "project_name": project_name,
            "team_members": team_members,
            "sprint_duration_weeks": sprint_duration,
            "specific_configs": request.specific_configs
        }

    def _configure_linear(self, integration: LinearIntegration, parsed_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Configure Linear (Create Team, Project, and Sprints).
        """
        logger.info("Step 2: Configuring Linear")

        project_name = parsed_config["project_name"]
        team_members = parsed_config["team_members"]
        sprint_duration = parsed_config["sprint_duration_weeks"]

        # Create team
        team_name = f"{project_name} Team"
        team_details = integration.create_team(team_name, team_members)

        # Create project under that team
        project_details = integration.create_project(
            team_id=team_details["id"],
            team_key=team_details["key"],
            project_name=project_name,
            members=team_members
        )

        # Define initial sprints (Create 3 initial sprints)
        sprints = integration.create_sprints(
            project_id=project_details["id"],
            sprint_duration_weeks=sprint_duration,
            count=3
        )

        return {
            "team": team_details,
            "project": project_details,
            "sprints": sprints
        }

    def _configure_slack(self, integration: SlackIntegration, parsed_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Configure Slack (Create channels, invite members).
        """
        logger.info("Step 3: Configuring Slack")

        project_name = parsed_config["project_name"]
        team_members = parsed_config["team_members"]

        # Create standard set of predefined channels and invite team members
        channels = integration.create_project_channels(project_name, team_members)

        return {
            "channels": channels
        }

    def _configure_notion(self, integration: NotionIntegration, parsed_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4: Configure Notion (workspace top-level pages and permissions).
        """
        logger.info("Step 4: Configuring Notion")

        project_name = parsed_config["project_name"]

        # Custom or default permissions
        specific_permissions = parsed_config["specific_configs"].get("notion_permissions")

        pages = integration.create_project_workspace(
            project_name=project_name,
            permissions=specific_permissions
        )

        return {
            "pages": pages
        }

    def _compile_summary(
        self,
        parsed_config: Dict[str, Any],
        linear: Dict[str, Any],
        slack: Dict[str, Any],
        notion: Dict[str, Any]
    ) -> str:
        """
        Step 5: Compile a comprehensive summary of all configured tools.
        """
        logger.info("Step 5: Compiling summary of configured tools")

        project_name = parsed_config["project_name"]
        team_members = parsed_config["team_members"]
        sprint_duration = parsed_config["sprint_duration_weeks"]

        sprint_lines = []
        for s in linear["sprints"]:
            sprint_lines.append(f"  - **{s['name']}**: {s['start_date']} to {s['end_date']} ({s['duration_weeks']} weeks)")
        sprint_text = "\n".join(sprint_lines)

        slack_lines = []
        for key, chan in slack["channels"].items():
            slack_lines.append(f"  - **{chan['name']}**: {chan['url']}")
        slack_text = "\n".join(slack_lines)

        notion_lines = []
        for key, page in notion["pages"].items():
            notion_lines.append(f"  - **{page['title']}**: {page['url']}")
        notion_text = "\n".join(notion_lines)

        member_list = ", ".join(team_members) if team_members else "None"

        summary = f"""### Internal Tool Setup Summary for {project_name}

#### 👥 Project Details
- **Project Name**: {project_name}
- **Assigned Team Members**: {member_list}
- **Sprint Duration**: {sprint_duration} weeks

#### 📐 Linear Configuration
- **Team Created**: {linear['team']['name']} (Key: `{linear['team']['key']}`)
- **Project Created**: {linear['project']['name']} (ID: `{linear['project']['id']}`)
- **Project URL**: {linear['project']['url']}
- **Sprints Configured**:
{sprint_text}

#### 💬 Slack Channels
- **Predefined Channels Created**:
{slack_text}

#### 📄 Notion Workspace & Pages
- **Top-Level Pages Configured**:
{notion_text}
"""
        return summary

    def _create_github_issue(
        self,
        integration: GitHubIntegration,
        parsed_config: Dict[str, Any],
        inputs: AgentInputs,
        linear: Dict[str, Any],
        slack: Dict[str, Any],
        notion: Dict[str, Any],
        summary: str
    ) -> str:
        """
        Step 6: Create GitHub issue summarizing the tool setup.
        """
        logger.info("Step 6: Creating GitHub issue summarizing setup")

        project_name = parsed_config["project_name"]
        issue_title = f"Internal Tool Setup for {project_name} Completed"

        # Construct issue body mapping the requested template/contents
        body = f"""# Internal Tool Setup Completed - {project_name}

## Goal
Automate the initial setup of internal project management, communication, and documentation tools (Linear, Slack, Notion) for PersonaScript.

## Inputs
- **Project Setup Request**:
  - Project Name: `{project_name}`
  - Team Members: {parsed_config['team_members']}
  - Initial Sprint Duration: {parsed_config['sprint_duration_weeks']} weeks
- **API Credentials**:
  - Linear API Key: {'[Configured]' if inputs.linear_api_key else '[Not Configured]'}
  - Slack API Token: {'[Configured]' if inputs.slack_api_token else '[Not Configured]'}
  - Notion API Key: {'[Configured]' if inputs.notion_api_key else '[Not Configured]'}
  - GitHub Token: {'[Configured]' if inputs.github_token else '[Not Configured]'}

## Outputs
- **Linear Project URL**: {linear['project']['url']}
- **Slack Channel URLs**:
{chr(10).join([f"  - {c['name']}: {c['url']}" for c in slack['channels'].values()])}
- **Notion Page URLs**:
{chr(10).join([f"  - {p['title']}: {p['url']}" for p in notion['pages'].values()])}
- **GitHub Issue URL**: [This Issue]

## Execution Plan
1. **Receive and parse the 'Project Setup Request'** to extract project name, team members, and any specific configuration details for Linear, Slack, and Notion. (Tool: Internal Logic/Parser)
2. **Configure Linear**: Create a new team, a new project under that team, and define initial sprints based on the parsed request. Assign relevant team members. (Tool: Linear API)
3. **Configure Slack**: Create a set of predefined channels (e.g., `#general-<project-slug>`, `#<project-slug>-dev`, `#<project-slug>-marketing`) and invite specified team members to these channels. (Tool: Slack API)
4. **Configure Notion**: Create a new workspace or a set of top-level pages (e.g., `'Project Name - Home'`, `'Project Name - Documentation'`, `'Project Name - Meetings'`) and set initial permissions. (Tool: Notion API)
5. **Compile a comprehensive summary** of all configured tools, including direct links to the created Linear project, Slack channels, and Notion pages. Document any relevant IDs or access information. (Tool: Internal Logic/Formatter)
6. **Create a new GitHub issue** in a designated repository. The issue title should clearly state `'Internal Tool Setup for [Project Name] Completed'`. The issue body must contain the goal, inputs, outputs, and the entire execution plan of this agent, along with the summary generated in Step 5. (Tool: GitHub API)

---

## Tool Setup Summary

{summary}
"""

        issue_url = integration.create_issue(
            title=issue_title,
            body=body,
            labels=["tool-setup", "completed"]
        )

        return issue_url
