"""Tests for ZoomIntegration."""

import pytest
from urllib.parse import urlparse
from src.integrations.zoom_integration import ZoomIntegration


class TestZoomIntegration:
    """Tests for ZoomIntegration."""

    def test_initialization(self):
        """Test Zoom integration initialization."""
        integration = ZoomIntegration()
        assert integration is not None
        assert integration.is_configured() is False

        integration_with_creds = ZoomIntegration(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )
        assert integration_with_creds.is_configured() is True

    def test_schedule_sessions(self):
        """Test scheduling individual Zoom usability sessions."""
        integration = ZoomIntegration()
        users = [
            {"name": "Sarah Miller", "email": "sarah@example.com", "role": "VP of Marketing"},
            {"name": "Alex Chen", "email": "alex@example.com", "role": "Content Manager"}
        ]
        maze_link = "https://maze.co/t/maze-test-12345"

        sessions = integration.schedule_sessions(users, test_link=maze_link)
        assert len(sessions) == 2
        for idx, session in enumerate(sessions):
            assert session["user_email"] == users[idx]["email"]
            assert session["maze_test_link"] == maze_link
            assert "zoom.us/j/" in session["join_url"]

            parsed = urlparse(session["join_url"])
            assert parsed.scheme == "https"
            assert parsed.netloc == "zoom.us"

    def test_get_session_recordings_and_notes(self):
        """Test retrieving qualitative recording notes."""
        integration = ZoomIntegration()
        session_ids = ["zoom-session-001", "zoom-session-002"]

        notes = integration.get_session_recordings_and_notes(session_ids)
        assert len(notes) == 2
        for item in notes:
            assert "participant_id" in item
            assert "direct_quote" in item
            assert "observer_notes" in item
            assert "friction_category" in item
