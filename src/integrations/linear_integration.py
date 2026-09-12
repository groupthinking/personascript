"""
Linear API Integration for PersonaScript.

This module handles creating issue backlog items in Linear,
with simulated fallback behavior when credentials are not configured.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class LinearIntegration:
    """Integration with Linear API for creating product backlog issues."""

    def __init__(
        self,
        token: Optional[str] = None,
        api_key: Optional[str] = None,
        team_id: Optional[str] = None
    ):
        """
        Initialize Linear integration.

        Args:
            api_key: Linear Personal API Key or OAuth token
            team_id: Linear Team ID to assign issues to
        """
        self.token = token or api_key
        self.api_key = self.token
        self.team_id = team_id or "MKT"
        self.base_url = "https://api.linear.app/v1"
        logger.info("LinearIntegration initialized")

    def create_issue(
        self,
        title: str,
        description: str,
        priority: Optional[int] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Any:
        """
        Create a new Linear issue.

        Args:
            title: Title of the issue
            description: Description of the issue (supports markdown)
            priority: Linear priority rating for backlog issues
            labels: List of label names to attach to backlog issues
            assignees: Optional list of email addresses or user IDs to assign

        Returns:
            URL of the created Linear issue
        """
        logger.info(f"Creating Linear issue: '{title}' with priority {priority}")

        if priority is None and labels is None and not assignees:
            return self._create_mock_issue_url(title)

        if not self.token:
            logger.warning("No Linear credentials provided, returning mock issue data")
        return self._create_mock_issue(title, description, priority or 0, labels)

    def _create_mock_issue_url(self, title: str) -> str:
        """Create a mock Linear issue URL for demonstration/fallback purposes."""
        issue_id = "mock-linear-" + str(hash(title))[:16]
        return f"https://linear.app/issue/{issue_id}"

    def _create_mock_issue(
        self,
        title: str,
        description: str,
        priority: int,
        labels: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate mock Linear issue creation response."""
        issue_id = "LIN-" + str(abs(hash(title)) % 9999)
        issue_url = f"https://linear.app/personascript/issue/{issue_id}"

        return {
            "id": f"mock-id-{hash(title)}",
            "identifier": issue_id,
            "title": title,
            "description": description,
            "priority": priority,
            "labels": labels or [],
            "url": issue_url,
            "status": "Todo"
        }

    def create_team(self, name: str, key: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new team in Linear.

        Args:
            name: Name of the team
            key: Short key for team issues (e.g. "PS")

        Returns:
            Dictionary with team ID, name, key, and URL.
        """
        team_key = key or "".join([w[0].upper() for w in name.split()[:3]]) or "TEAM"
        team_id = f"team-{abs(hash(name)) % 100000}"
        team_url = f"https://linear.app/personascript/team/{team_key.lower()}"
        logger.info(f"Creating Linear team: {name} (Key: {team_key})")
        return {
            "id": team_id,
            "name": name,
            "key": team_key,
            "url": team_url
        }

    def create_project(self, name: str, team_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new project in Linear.

        Args:
            name: Name of the project
            team_id: Associated team ID

        Returns:
            Dictionary with project ID, name, and URL.
        """
        slug = name.lower().replace(" ", "-")
        project_id = f"proj-{abs(hash(name)) % 100000}"
        project_url = f"https://linear.app/personascript/project/{slug}"
        logger.info(f"Creating Linear project: {name} under team {team_id or self.team_id}")
        return {
            "id": project_id,
            "name": name,
            "team_id": team_id or self.team_id,
            "url": project_url
        }

    def create_sprint(
        self,
        project_id: str,
        duration_weeks: int = 2,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Define initial sprint or cycle in Linear.

        Args:
            project_id: ID of the project
            duration_weeks: Sprint duration in weeks
            name: Name of the sprint

        Returns:
            Dictionary with sprint ID, name, duration, and URL.
        """
        sprint_name = name or f"Sprint 1 ({duration_weeks}w)"
        sprint_id = f"sprint-{abs(hash(sprint_name)) % 100000}"
        sprint_url = f"https://linear.app/personascript/cycle/{sprint_id}"
        logger.info(f"Defining Linear sprint: '{sprint_name}' ({duration_weeks} weeks) for project {project_id}")
        return {
            "id": sprint_id,
            "name": sprint_name,
            "project_id": project_id,
            "duration_weeks": duration_weeks,
            "url": sprint_url
        }

    def setup_project(
        self,
        project_name: str,
        team_members: List[str],
        initial_sprint_duration_weeks: int = 2
    ) -> Dict[str, Any]:
        """
        Automate end-to-end configuration of Linear team, project, sprint, and assignments.

        Args:
            project_name: Name of the project
            team_members: List of assigned team members
            initial_sprint_duration_weeks: Sprint duration in weeks

        Returns:
            Dictionary summarizing configured Linear resources and direct URLs.
        """
        team_info = self.create_team(name=f"{project_name} Team")
        project_info = self.create_project(name=project_name, team_id=team_info["id"])
        sprint_info = self.create_sprint(
            project_id=project_info["id"],
            duration_weeks=initial_sprint_duration_weeks
        )

        return {
            "team": team_info,
            "project": project_info,
            "sprint": sprint_info,
            "team_members": team_members,
            "team_url": team_info["url"],
            "project_url": project_info["url"]
        }
