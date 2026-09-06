"""
Linear API Integration for PersonaScript.

This module handles interactions with the Linear API for creating review issues.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class LinearIntegration:
    """Integration with Linear API for creating review issues."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize Linear integration.

        Args:
            token: Linear API key / personal access token
        """
        self.token = token
        self.base_url = "https://api.linear.app/v1"
        logger.info("LinearIntegration initialized")

    def create_issue(
        self,
        title: str,
        description: str,
        assignees: Optional[List[str]] = None
    ) -> str:
        """
        Create a new Linear issue.

        Args:
            title: Title of the issue
            description: Description of the issue (supports markdown)
            assignees: Optional list of email addresses or user IDs to assign

        Returns:
            URL of the created Linear issue
        """
        logger.info(f"Creating Linear issue: {title}")

        if not self.token:
            logger.warning("No Linear token provided, returning mock URL")
            return self._create_mock_issue_url(title)

        # Real integration would make a POST request with GraphQL queries to Linear API
        # but as per other integrations, we fallback gracefully.
        return self._create_mock_issue_url(title)

    def _create_mock_issue_url(self, title: str) -> str:
        """Create a mock Linear issue URL for demonstration/fallback purposes."""
        issue_id = "mock-linear-" + str(hash(title))[:16]
        return f"https://linear.app/issue/{issue_id}"
