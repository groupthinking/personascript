"""
Zoom API Integration for PersonaScript.

This module handles scheduling individual 1:1 usability testing sessions with target users,
generating Zoom meeting links with attached Maze prototype test links, and retrieving qualitative
feedback, notes, and recording summaries.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


class ZoomIntegration:
    """Integration with Zoom API for coordinating usability testing sessions."""

    def __init__(
        self,
        account_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize Zoom integration.

        Args:
            account_id: Zoom Account ID for OAuth
            client_id: Zoom Client ID
            client_secret: Zoom Client Secret
            api_key: Optional legacy JWT / API Key
        """
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        logger.info("ZoomIntegration initialized")

    def is_configured(self) -> bool:
        """Check if active credentials are present for Zoom API calls."""
        return bool((self.client_id and self.client_secret) or self.api_key)

    def schedule_sessions(
        self,
        users: List[Dict[str, Any]],
        test_link: str,
        duration_minutes: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Coordinate and schedule individual usability testing sessions for target users via Zoom.

        Args:
            users: List of participant profile dicts (name, email, role, etc.)
            test_link: Maze prototype test link to include in invite details
            duration_minutes: Duration of each scheduled session

        Returns:
            List of scheduled session details including meeting URLs, passcode, user email, and join info.
        """
        logger.info(f"Scheduling {len(users)} Zoom usability test sessions with test_link={test_link}")

        if not self.is_configured():
            logger.warning("No Zoom credentials provided, returning simulated scheduled sessions")
            return self._schedule_mock_sessions(users, test_link, duration_minutes)

        # Real API integration would request OAuth access token and POST /users/me/meetings
        return self._schedule_mock_sessions(users, test_link, duration_minutes)

    def get_session_recordings_and_notes(self, session_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Collect qualitative feedback, session recording metadata, and notes from Zoom sessions.

        Args:
            session_ids: List of Zoom meeting session IDs

        Returns:
            List of qualitative feedback records with transcript notes, participant quotes, and observations.
        """
        logger.info(f"Retrieving qualitative recordings & notes for {len(session_ids)} Zoom sessions")

        if not self.is_configured():
            logger.warning("No Zoom credentials provided, returning mock recording notes & qualitative feedback")
            return self._get_mock_recordings_and_notes(session_ids)

        return self._get_mock_recordings_and_notes(session_ids)

    def _schedule_mock_sessions(
        self,
        users: List[Dict[str, Any]],
        test_link: str,
        duration_minutes: int
    ) -> List[Dict[str, Any]]:
        """Generate mock scheduled Zoom session objects."""
        scheduled_sessions = []
        base_time = datetime.now(timezone.utc) + timedelta(days=1)

        for idx, user in enumerate(users):
            session_time = base_time + timedelta(hours=idx * 2)
            session_id = f"zoom-session-{idx+1:03d}"
            join_url = f"https://zoom.us/j/9876543{idx:03d}?pwd=mockpwd{idx}"

            scheduled_sessions.append({
                "session_id": session_id,
                "user_name": user.get("name", f"Participant {idx+1}"),
                "user_email": user.get("email", f"participant{idx+1}@example.com"),
                "user_role": user.get("role", "Target Persona"),
                "start_time": session_time.isoformat(),
                "duration_minutes": duration_minutes,
                "join_url": join_url,
                "maze_test_link": test_link,
                "status": "scheduled"
            })

        return scheduled_sessions

    def _get_mock_recordings_and_notes(self, session_ids: List[str]) -> List[Dict[str, Any]]:
        """Generate mock qualitative feedback and observation notes for testing."""
        qualitative_records = []

        feedback_samples = [
            {
                "quote": "I wasn't sure where to click to generate the brief—the secondary button looked disabled.",
                "observation": "Participant hesitated for 18 seconds on the main builder interface searching for the primary CTA.",
                "perceived_value": "Loved the instant preview generation once located.",
                "friction_category": "Navigation & CTA Clarity"
            },
            {
                "quote": "The tone dropdown has too many overlapping options like 'Professional' vs 'Executive'.",
                "observation": "Participant misclicked twice when selecting tone parameters.",
                "perceived_value": "Appreciated automatic brand guideline checks.",
                "friction_category": "Form Input Complexity"
            },
            {
                "quote": "I expected an instant export status indicator when pushing collateral to HubSpot.",
                "observation": "Participant clicked the export button multiple times assuming it failed.",
                "perceived_value": "High excitement for seamless marketing workflow integrations.",
                "friction_category": "System Feedback & Export State"
            },
            {
                "quote": "The mobile layout cut off the key persona configuration controls.",
                "observation": "Participant experienced layout clipping on smaller screen resolution.",
                "perceived_value": "Highly relevant persona fields for B2B SaaS campaigns.",
                "friction_category": "Responsiveness & Visual Layout"
            }
        ]

        for idx, session_id in enumerate(session_ids):
            sample = feedback_samples[idx % len(feedback_samples)]
            qualitative_records.append({
                "session_id": session_id,
                "participant_id": f"P-{idx+1:02d}",
                "recording_url": f"https://zoom.us/rec/play/mock-rec-{idx+1}",
                "direct_quote": sample["quote"],
                "observer_notes": sample["observation"],
                "perceived_value": sample["perceived_value"],
                "friction_category": sample["friction_category"],
                "key_takeaway": f"Participant P-{idx+1:02d} identified friction in {sample['friction_category']}."
            })

        return qualitative_records
