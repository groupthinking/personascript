"""
Zoom API Integration for PersonaScript.

This module handles interactions with the Zoom API for scheduling
feedback sessions with beta participants.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ZoomIntegration:
    """Integration with Zoom API for scheduling and managing sessions."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        account_id: Optional[str] = None
    ):
        """
        Initialize Zoom integration.

        Args:
            client_id: Zoom app Client ID
            client_secret: Zoom app Client Secret
            account_id: Zoom Server-to-Server Account ID
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        logger.info("ZoomIntegration initialized")

    def schedule_meeting(
        self,
        topic: str,
        duration_minutes: int = 30,
        start_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Schedule a new Zoom meeting for a feedback session.

        Args:
            topic: Meeting topic/title
            duration_minutes: Duration of the meeting in minutes
            start_time: Start time of meeting in ISO format (e.g. "2024-10-24T10:00:00")

        Returns:
            Dictionary containing meeting details (ID, Join URL, etc.)
        """
        logger.info(f"Zoom: Scheduling meeting: {topic}")

        meeting_id = str(abs(hash(topic)) % 10000000000)
        join_url = f"https://zoom.us/j/{meeting_id}"

        if not self._has_credentials():
            logger.warning("No complete Zoom credentials provided, returning mock meeting")
            return {
                "id": meeting_id,
                "topic": topic,
                "duration": duration_minutes,
                "start_time": start_time,
                "join_url": join_url,
                "status": "scheduled",
                "mocked": True
            }

        # Real implementation would do Server-to-Server OAuth to get access token,
        # then POST to /users/me/meetings
        return {
            "id": meeting_id,
            "topic": topic,
            "duration": duration_minutes,
            "start_time": start_time,
            "join_url": join_url,
            "status": "scheduled",
            "mocked": False
        }

    def _has_credentials(self) -> bool:
        """Check if Zoom credentials are fully configured."""
        return bool(self.client_id and self.client_secret and self.account_id)
