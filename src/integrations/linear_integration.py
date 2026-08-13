"""
Linear API Integration for PersonaScript.

This module handles creating Linear teams, projects, sprints, and assigning team members.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class LinearIntegration:
    """Integration with Linear API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Linear integration.

        Args:
            api_key: Linear API key for authentication
        """
        self.api_key = api_key
        self.base_url = "https://api.linear.app/v1"
        logger.info("LinearIntegration initialized")

    def create_team(self, team_name: str, members: List[str]) -> Dict[str, Any]:
        """
        Create a new team in Linear.

        Args:
            team_name: Name of the team
            members: List of team member emails/usernames

        Returns:
            Dictionary containing created team details
        """
        logger.info(f"Creating Linear team: {team_name} with members: {members}")

        # In a real implementation, this would make a GraphQL query/mutation to the Linear API.
        # We generate a unique sluggified key for the team, e.g. "PRO"
        words = [w for w in team_name.replace("-", " ").split() if w]
        if len(words) >= 3:
            key = "".join(w[0].upper() for w in words[:3])
        elif len(words) == 2:
            key = (words[0][:2] + words[1][0]).upper()
        elif len(words) == 1:
            key = words[0][:3].upper()
        else:
            key = "PRJ"

        # Limit to 3 uppercase letters
        key = key[:3].ljust(3, "X")

        team_id = f"team-{hash(team_name) % 10000:04d}"

        return {
            "id": team_id,
            "name": team_name,
            "key": key,
            "members": members,
            "url": f"https://linear.app/personascript/team/{key.lower()}"
        }

    def create_project(self, team_id: str, team_key: str, project_name: str, members: List[str]) -> Dict[str, Any]:
        """
        Create a new project under a Linear team.

        Args:
            team_id: ID of the team
            team_key: Key/Slug of the team
            project_name: Name of the project
            members: List of team member emails/usernames

        Returns:
            Dictionary containing created project details
        """
        logger.info(f"Creating Linear project: {project_name} under team: {team_id}")

        project_id = f"proj-{hash(project_name) % 10000:04d}"
        project_slug = project_name.lower().replace(" ", "-")
        project_url = f"https://linear.app/personascript/team/{team_key.lower()}/project/{project_slug}"

        return {
            "id": project_id,
            "team_id": team_id,
            "name": project_name,
            "members": members,
            "url": project_url
        }

    def create_sprints(
        self,
        project_id: str,
        sprint_duration_weeks: int,
        count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Define initial sprints/cycles.

        Args:
            project_id: ID of the project
            sprint_duration_weeks: Duration of each sprint in weeks
            count: Number of initial sprints to create

        Returns:
            List of dictionaries containing sprint details
        """
        logger.info(f"Creating {count} sprints of duration {sprint_duration_weeks} weeks for project: {project_id}")

        sprints = []
        current_date = datetime.now()

        for i in range(1, count + 1):
            start_date = current_date
            end_date = current_date + timedelta(weeks=sprint_duration_weeks)

            sprint_id = f"sprint-{hash(project_id + str(i)) % 1000:03d}"

            sprints.append({
                "id": sprint_id,
                "name": f"Sprint {i}",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_weeks": sprint_duration_weeks
            })
            current_date = end_date

        return sprints
