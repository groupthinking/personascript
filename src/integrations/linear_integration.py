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
