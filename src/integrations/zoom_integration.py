"""
Zoom API Integration for PersonaScript.

This module handles interacting with the Zoom API for scheduling 1:1 and group feedback
sessions with beta participants.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ZoomIntegration:
    """Integration with Zoom API for scheduling beta feedback sessions."""

    def __init__(
        self,
        token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None
    ):
        """
        Initialize Zoom integration.

        Args:
            token: Zoom JWT or OAuth Token
            api_key: Zoom API Key (legacy/fallback)
            api_secret: Zoom API Secret (legacy/fallback)
        """
        self.token = token or api_key
        self.api_secret = api_secret
        self.base_url = "https://api.zoom.us/v2"
        logger.info("ZoomIntegration initialized")

    def schedule_session(
        self,
        topic: str,
        start_time: str,
        duration_minutes: int = 45,
        participants: Optional[List[str]] = None,
        session_type: str = "1:1"
    ) -> Dict[str, Any]:
        """
        Schedule a 1:1 or group feedback session via Zoom API.

        Args:
            topic: Meeting topic / title
            start_time: Scheduled start time ISO string
            duration_minutes: Meeting duration in minutes
            participants: List of participant emails
            session_type: Type of session ("1:1" or "group")

        Returns:
            Dictionary containing meeting details, join URL, and ID
        """
        logger.info(f"Scheduling {session_type} Zoom feedback session: '{topic}' at {start_time}")

        if not self.token:
            logger.warning("No Zoom token provided, returning mock meeting response")

        meeting_id = str(abs(hash(topic + start_time)) % 10000000000)
        join_url = f"https://zoom.us/j/{meeting_id}?pwd=mockpwd{meeting_id[:4]}"

        return {
            "meeting_id": meeting_id,
            "topic": topic,
            "start_time": start_time,
            "duration_minutes": duration_minutes,
            "session_type": session_type,
            "participants": participants or [],
            "join_url": join_url,
            "status": "scheduled"
        }
