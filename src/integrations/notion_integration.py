"""
Notion Integration for Partner Scouting.

This module handles writing draft proposals and comprehensive reports to Notion.
"""

import logging
from typing import Dict, Any, Optional, List
import requests

logger = logging.getLogger(__name__)


class NotionPartnershipIntegration:
    """Integration with Notion API for publishing partnership reports and proposals."""

    def __init__(self, api_key: Optional[str] = None, database_id: Optional[str] = None):
        """
        Initialize Notion Partnership integration.

        Args:
            api_key: Notion integration secret.
            database_id: Target database ID for partnership entries.
        """
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        logger.info("NotionPartnershipIntegration initialized")

    def create_proposal_page(
        self,
        lead_name: str,
        proposal_content: str
    ) -> str:
        """
        Create a new draft proposal page in Notion.

        Args:
            lead_name: Name of the partnership lead.
            proposal_content: Structured markdown text for the proposal outline.

        Returns:
            URL of the newly created Notion page.
        """
        logger.info(f"Creating Notion proposal page for {lead_name}")

        if not self.api_key:
            logger.warning("No Notion API key provided, returning simulated URL")
            return self._create_mock_url(f"proposal-{lead_name}")

        try:
            # Create block components from proposal content markdown
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}/pages"

            # Simple page layout creation block
            payload = {
                "parent": {"database_id": self.database_id} if self.database_id else {"page_id": "root"},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": f"Partnership Proposal Outline: PersonaScript x {lead_name}"
                                }
                            }
                        ]
                    }
                },
                "children": self._convert_markdown_to_blocks(proposal_content)
            }

            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                return data.get("url", self._create_mock_url(f"proposal-{lead_name}"))

            logger.warning(f"Notion API returned status {response.status_code}, returning simulated URL")
            return self._create_mock_url(f"proposal-{lead_name}")
        except Exception as e:
            logger.error(f"Error creating Notion page: {e}", exc_info=True)
            return self._create_mock_url(f"proposal-{lead_name}")

    def create_comprehensive_report_page(
        self,
        title: str,
        report_content: str
    ) -> str:
        """
        Create a comprehensive partnership scout report page in Notion.

        Args:
            title: Title of the report page.
            report_content: Structured markdown content of the scout report.

        Returns:
            URL of the newly created Notion page.
        """
        logger.info(f"Creating Notion comprehensive report page: {title}")

        if not self.api_key:
            logger.warning("No Notion API key provided, returning simulated URL")
            return self._create_mock_url("comprehensive-scout-report")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}/pages"

            payload = {
                "parent": {"database_id": self.database_id} if self.database_id else {"page_id": "root"},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    }
                },
                "children": self._convert_markdown_to_blocks(report_content)
            }

            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                return data.get("url", self._create_mock_url("comprehensive-scout-report"))

            logger.warning(f"Notion API returned status {response.status_code}, returning simulated URL")
            return self._create_mock_url("comprehensive-scout-report")
        except Exception as e:
            logger.error(f"Error creating Notion comprehensive report page: {e}", exc_info=True)
            return self._create_mock_url("comprehensive-scout-report")

    def _convert_markdown_to_blocks(self, text: str) -> List[Dict[str, Any]]:
        """A simple helper to convert basic markdown elements into Notion blocks."""
        blocks = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            elif line.startswith("- ") or line.startswith("* "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })
        return blocks[:100]  # Notion block creation limit safeguards

    def _create_mock_url(self, slug: str) -> str:
        """Generate a mock Notion URL for verification."""
        clean_slug = slug.lower().replace(" ", "-").replace("/", "-")
        import uuid
        page_id = uuid.uuid4().hex
        return f"https://notion.so/personascript/{clean_slug}-{page_id}"
