"""
Notion API Integration for PersonaScript.

This module handles all interactions with the Notion API for creating competitor matrices.
"""

import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class NotionIntegration:
    """Integration with Notion API for creating competitor matrices."""

    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        """
        Initialize Notion integration.

        Args:
            api_key: Notion API key
            database_id: Target database ID for compiling matrix data
        """
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        logger.info("NotionIntegration initialized")

    def create_competitor_matrix(self, matrix_data: Dict[str, Any]) -> str:
        """
        Create a new competitor matrix in Notion.

        Args:
            matrix_data: Dictionary containing competitor matrix structure and rows

        Returns:
            URL of the created Notion page or database
        """
        logger.info(f"Creating Notion Competitor Matrix: {matrix_data.get('title', 'Competitor Matrix')}")

        if not self.api_key or not self.database_id:
            logger.warning("No Notion credentials provided, returning mock URL")
            return self._create_mock_matrix_url(matrix_data)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }

            # For each competitor, insert a page (row) into the target Notion database
            for comp in matrix_data.get("competitors", []):
                payload = {
                    "parent": {"database_id": self.database_id},
                    "properties": {
                        "Name": {
                            "title": [
                                {"text": {"content": comp.get("name", "Unknown Competitor")}}
                            ]
                        },
                        "Features": {
                            "rich_text": [
                                {"text": {"content": ", ".join(comp.get("features", []))}}
                            ]
                        },
                        "Pricing": {
                            "rich_text": [
                                {"text": {"content": comp.get("pricing", "N/A")}}
                            ]
                        },
                        "Audience": {
                            "rich_text": [
                                {"text": {"content": comp.get("audience", "N/A")}}
                            ]
                        },
                        "Strengths": {
                            "rich_text": [
                                {"text": {"content": ", ".join(comp.get("strengths", []))}}
                            ]
                        },
                        "Pain Points": {
                            "rich_text": [
                                {"text": {"content": ", ".join(comp.get("pain_points", []))}}
                            ]
                        }
                    }
                }

                # Make real HTTP POST request to Notion API
                url = f"{self.base_url}/pages"
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                response.raise_for_status()

            logger.info("Successfully populated Notion competitor database")
            return f"https://notion.so/{self.database_id}"

        except Exception as e:
            logger.error(f"Failed to create competitor matrix on Notion: {e}", exc_info=True)
            # Safe fallback to mock URL so execution doesn't crash completely
            return self._create_mock_matrix_url(matrix_data)

    def _create_mock_matrix_url(self, matrix_data: Dict[str, Any]) -> str:
        """Create a mock Notion matrix URL for demonstration purposes."""
        matrix_id = "mock-notion-" + str(hash(matrix_data.get('title', '')))[:16]
        return f"https://notion.so/{matrix_id}"
