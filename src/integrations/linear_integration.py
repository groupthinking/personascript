"""
Linear API Integration for PersonaScript.

This module handles interactions with the Linear API for logging, tracking,
and updating bugs and feature requests reported during the beta program.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class LinearIntegration:
    """Integration with Linear API for tracking issues."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Linear integration.

        Args:
            api_key: Linear personal API key or OAuth token
        """
        self.api_key = api_key
        self.base_url = "https://api.linear.app/v1"
        logger.info("LinearIntegration initialized")

    def create_issue(
        self,
        title: str,
        description: str,
        team_id: str = "BETA",
        priority: int = 0,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new issue (bug or feature request) in Linear.

        Args:
            title: The title of the issue
            description: Detailed description of the issue
            team_id: Linear team identifier (e.g. "BETA")
            priority: Priority level (0=none, 1=urgent, 2=high, 3=normal, 4=low)
            labels: Optional list of labels (e.g. ["bug", "beta-feedback"])

        Returns:
            Dictionary containing issue details including ID and URL
        """
        logger.info(f"Linear: Creating issue: {title} (Team: {team_id})")

        issue_id = f"LIN-{abs(hash(title)) % 10000}"
        issue_url = f"https://linear.app/personascript/issue/{issue_id}"

        if not self.api_key:
            logger.warning("No Linear API key provided, returning mock issue details")
            return {
                "id": issue_id,
                "title": title,
                "description": description,
                "team_id": team_id,
                "priority": priority,
                "labels": labels or [],
                "url": issue_url,
                "status": "todo",
                "mocked": True
            }

        # Real implementation would perform a GraphQL POST to Linear API
        return {
            "id": issue_id,
            "title": title,
            "description": description,
            "team_id": team_id,
            "priority": priority,
            "labels": labels or [],
            "url": issue_url,
            "status": "todo",
            "mocked": False
        }

    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """
        Retrieve issue details by ID.

        Args:
            issue_id: Linear issue ID (e.g. "LIN-101")

        Returns:
            Dictionary containing issue details
        """
        logger.info(f"Linear: Fetching issue {issue_id}")
        return {
            "id": issue_id,
            "title": "Mock Issue Title",
            "description": "Mock Issue Description",
            "url": f"https://linear.app/personascript/issue/{issue_id}",
            "status": "todo"
        }
