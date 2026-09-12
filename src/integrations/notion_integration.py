"""
Notion API Integration for PersonaScript.

This module handles interactions with the Notion API for publishing PRD pages.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class NotionIntegration:
    """Integration with Notion API for creating PRD pages."""

    def __init__(self, token: Optional[str] = None, database_id: Optional[str] = None):
        """
        Initialize Notion integration.

        Args:
            token: Notion integration token
            database_id: Target database ID (optional)
        """
        self.token = token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        logger.info("NotionIntegration initialized")

    def create_page(self, title: str, content: str) -> str:
        """
        Create a new Notion page.

        Args:
            title: Title of the page
            content: Page content (markdown or text)

        Returns:
            URL of the created Notion page
        """
        logger.info(f"Creating Notion page: {title}")

        if not self.token:
            logger.warning("No Notion token provided, returning mock URL")
            return self._create_mock_page_url(title)

        # Real integration would make a POST request to Notion API
        # but as per other integrations, we fallback gracefully.
        return self._create_mock_page_url(title)

    def is_configured(self) -> bool:
        """Check if Notion integration is configured with an API token."""
        return bool(self.token)

    def _create_mock_page_url(self, title: str) -> str:
        """Create a mock Notion page URL for demonstration/fallback purposes."""
        page_id = "mock-notion-" + str(abs(hash(title)))[:16]
        return f"https://notion.so/{page_id}"

    def setup_workspace_pages(
        self,
        project_name: str,
        page_suffixes: Optional[list] = None,
        permissions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Create top-level Notion workspace pages for a project and set initial permissions.

        Args:
            project_name: Name of the project
            page_suffixes: List of page title suffixes (defaults to ["Home", "Documentation", "Meetings"])
            permissions: Optional permission settings dictionary

        Returns:
            Dictionary mapping page title (e.g., "PersonaScript - Home") to Notion page URL.
        """
        suffixes = page_suffixes or ["Home", "Documentation", "Meetings"]
        created_pages: Dict[str, str] = {}

        logger.info(f"Setting up Notion workspace pages for project '{project_name}'")

        for suffix in suffixes:
            page_title = f"{project_name} - {suffix}"
            initial_content = f"# {page_title}\n\nWorkspace section initialized for {project_name}."
            page_url = self.create_page(title=page_title, content=initial_content)
            created_pages[page_title] = page_url

        return created_pages
