"""
Slack API Integration for PersonaScript.

This module handles interactions with the Slack API for creating channels,
inviting team members, and generating channel access links.
"""

import logging
import requests
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class SlackIntegration:
    """Integration with Slack API for workspace communications management."""

    def __init__(self, token: Optional[str] = None, bot_token: Optional[str] = None):
        """
        Initialize Slack integration.

        Args:
            token: User access token or OAuth token
            bot_token: Bot user OAuth token
        """
        self.token = token or bot_token
        self.base_url = "https://slack.com/api"
        logger.info("SlackIntegration initialized")

    def is_configured(self) -> bool:
        """Check if Slack integration is configured with an API token."""
        return bool(self.token)

    def create_channel(self, name: str, is_private: bool = False) -> Dict[str, Any]:
        """
        Create a new Slack channel.

        Args:
            name: Name of the channel (will be sanitized for Slack requirements)
            is_private: Whether channel is private

        Returns:
            Dictionary containing channel metadata including id, name, and url.
        """
        clean_name = name.lower().replace(" ", "-").replace("#", "")
        logger.info(f"Creating Slack channel: #{clean_name}")

        if not self.token:
            logger.warning("No Slack token provided, returning mock channel data")
            return self._create_mock_channel(clean_name)

        try:
            url = f"{self.base_url}/conversations.create"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            payload = {
                "name": clean_name,
                "is_private": is_private
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            res_json = response.json() if response.status_code == 200 else {}

            if response.status_code == 200 and res_json.get("ok"):
                channel_data = res_json.get("channel", {})
                ch_id = channel_data.get("id", f"C{abs(hash(clean_name)) % 1000000}")
                ch_url = f"https://slack.com/app_redirect?channel={ch_id}"
                return {
                    "id": ch_id,
                    "name": clean_name,
                    "url": ch_url,
                    "is_private": is_private,
                    "status": "created"
                }

            logger.error(f"Failed to create Slack channel #{clean_name}: {response.text}")
            return self._create_mock_channel(clean_name)
        except Exception as e:
            logger.error(f"Exception creating Slack channel #{clean_name}: {e}", exc_info=True)
            return self._create_mock_channel(clean_name)

    def invite_members(self, channel_id: str, members: List[str]) -> Dict[str, Any]:
        """
        Invite specified team members to a Slack channel.

        Args:
            channel_id: Target Slack channel ID
            members: List of member email addresses or Slack user IDs

        Returns:
            Dictionary summarizing invitation results.
        """
        logger.info(f"Inviting {len(members)} members to Slack channel {channel_id}")

        if not self.token:
            logger.warning("No Slack token provided, returning mock invite response")
            return {
                "channel_id": channel_id,
                "invited_members": members,
                "status": "simulated"
            }

        try:
            url = f"{self.base_url}/conversations.invite"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            payload = {
                "channel": channel_id,
                "users": ",".join(members)
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            res_json = response.json() if response.status_code == 200 else {}

            if response.status_code == 200 and res_json.get("ok"):
                return {
                    "channel_id": channel_id,
                    "invited_members": members,
                    "status": "success"
                }

            logger.error(f"Failed to invite members to Slack channel {channel_id}: {response.text}")
            return {
                "channel_id": channel_id,
                "invited_members": members,
                "status": "simulated_fallback",
                "error": res_json.get("error", "API request failed")
            }
        except Exception as e:
            logger.error(f"Exception inviting members to Slack channel {channel_id}: {e}", exc_info=True)
            return {
                "channel_id": channel_id,
                "invited_members": members,
                "status": "error",
                "error": str(e)
            }

    def setup_project_channels(
        self,
        project_name: str,
        team_members: List[str],
        channels: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Predefine and create a standard set of project channels and invite members.

        Args:
            project_name: Name of the project
            team_members: List of team members/emails
            channels: Optional list of specific channel name suffixes

        Returns:
            Dictionary mapping channel name (e.g., "#general-project-name") to channel URL.
        """
        sanitized_project = project_name.lower().replace(" ", "-")
        channel_suffixes = channels or ["general", "dev", "marketing"]

        channel_urls: Dict[str, str] = {}

        for suffix in channel_suffixes:
            ch_name = f"{suffix}-{sanitized_project}" if suffix != "general" else f"general-{sanitized_project}"
            ch_info = self.create_channel(ch_name)
            ch_id = ch_info.get("id", "")
            ch_url = ch_info.get("url", f"https://slack.com/app_redirect?channel={ch_id}")

            if team_members and ch_id:
                self.invite_members(ch_id, team_members)

            channel_urls[f"#{ch_name}"] = ch_url

        return channel_urls

    def _create_mock_channel(self, name: str) -> Dict[str, Any]:
        """Generate mock Slack channel response."""
        ch_id = "C" + str(abs(hash(name)) % 10000000).zfill(8)
        ch_url = f"https://slack.com/app_redirect?channel={ch_id}"
        return {
            "id": ch_id,
            "name": name,
            "url": ch_url,
            "is_private": False,
            "status": "simulated"
        }
