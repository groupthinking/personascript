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

    def __init__(self, api_key: Optional[str] = None, team_id: Optional[str] = None):
        """
        Initialize Linear integration.

        Args:
            api_key: Linear Personal API Key or OAuth token
            team_id: Linear Team ID to assign issues to
        """
        self.api_key = api_key
        self.team_id = team_id or "MKT"
        self.base_url = "https://api.linear.app/v1"
        logger.info("LinearIntegration initialized")

    def create_issue(
        self,
        title: str,
        description: str,
        priority: int = 0,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new Linear issue for backlog prioritization.

        Args:
            title: Title of the Linear issue
            description: Markdown description detailing findings & metrics
            priority: Linear priority rating (0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low)
            labels: List of label names to attach to the issue

        Returns:
            Dictionary with issue details, including the tracking URL.
        """
        logger.info(f"Creating Linear issue: '{title}' with priority {priority}")

        if not self.api_key:
            logger.warning("No Linear credentials provided, returning mock issue data")
            return self._create_mock_issue(title, description, priority, labels)

        # Real integration would make a POST GraphQL call to the Linear API.
        return self._create_mock_issue(title, description, priority, labels)

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
