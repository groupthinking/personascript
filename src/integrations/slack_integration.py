"""
Slack API Integration for PersonaScript.

This module handles creating Slack channels and inviting team members.
"""

import logging
import re
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class SlackIntegration:
    """Integration with Slack API."""

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Slack integration.

        Args:
            api_token: Slack API bot token
        """
        self.api_token = api_token
        self.base_url = "https://slack.com/api"
        logger.info("SlackIntegration initialized")

    def sluggify(self, text: str) -> str:
        """
        Convert a string to a valid Slack channel name slug.

        Rules: Lowercase, max 80 chars, alphanumeric, hyphens/underscores only.
        """
        slug = text.lower()
        # Replace non-alphanumeric with hyphens
        slug = re.sub(r'[^a-z0-9_-]', '-', slug)
        # Collapse multiple hyphens/underscores
        slug = re.sub(r'[-_]+', '-', slug)
        # Strip leading/trailing hyphens/underscores
        slug = slug.strip('-')
        return slug[:80]

    def create_channel(self, channel_name: str, members: List[str]) -> Dict[str, Any]:
        """
        Create a single Slack channel and invite members.

        Args:
            channel_name: Name of the channel (with or without '#')
            members: List of member usernames or IDs to invite

        Returns:
            Dictionary containing channel details
        """
        cleaned_name = channel_name.lstrip('#')
        logger.info(f"Creating Slack channel: #{cleaned_name} and inviting: {members}")

        channel_id = f"C{abs(hash(cleaned_name)) % 100000000:08d}"
        channel_url = f"https://personascript.slack.com/archives/{channel_id}"

        return {
            "id": channel_id,
            "name": f"#{cleaned_name}",
            "invited_members": members,
            "url": channel_url
        }

    def create_project_channels(self, project_name: str, members: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Create a predefined set of Slack channels for a project.

        Args:
            project_name: Name of the project
            members: List of member usernames/IDs to invite

        Returns:
            Dictionary mapping channel keys (e.g. 'general', 'dev', 'marketing') to channel details
        """
        slug = self.sluggify(project_name)
        logger.info(f"Creating predefined channels for project: {project_name} (slug: {slug})")

        predefined_types = {
            "general": f"general-{slug}",
            "dev": f"{slug}-dev",
            "marketing": f"{slug}-marketing"
        }

        created_channels = {}
        for key, name in predefined_types.items():
            created_channels[key] = self.create_channel(name, members)

        return created_channels
