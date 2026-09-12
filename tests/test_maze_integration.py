"""Tests for MazeIntegration."""

import pytest
from urllib.parse import urlparse
from src.integrations.maze_integration import MazeIntegration


class TestMazeIntegration:
    """Tests for MazeIntegration."""

    def test_initialization(self):
        """Test Maze integration initialization."""
        integration = MazeIntegration()
        assert integration is not None
        assert integration.api_key is None
        assert integration.is_configured() is False

        integration_with_key = MazeIntegration(api_key="test_key")
        assert integration_with_key.api_key == "test_key"
        assert integration_with_key.is_configured() is True

    def test_configure_test(self):
        """Test test configuration in Maze."""
        integration = MazeIntegration()
        prototypes = [
            "https://www.figma.com/file/mock-prototype-1",
            "https://www.figma.com/file/mock-prototype-2"
        ]
        test_script = [
            "Task 1: Complete Onboarding",
            "Task 2: Select Persona & Generate Brief",
            "Task 3: Export Brief"
        ]

        config = integration.configure_test(prototypes, test_script, title="Test Campaign")
        assert config["test_id"].startswith("maze-test-")
        assert "maze.co/t/" in config["test_link"]
        assert config["status"] == "active"
        assert config["prototypes"] == prototypes

        parsed = urlparse(config["test_link"])
        assert parsed.scheme == "https"
        assert parsed.netloc == "maze.co"

    def test_get_test_results(self):
        """Test retrieving quantitative test results."""
        integration = MazeIntegration()
        results = integration.get_test_results("maze-test-12345")

        assert results["test_id"] == "maze-test-12345"
        assert results["total_participants"] == 10
        assert "usability_score" in results
        assert "direct_success_rate" in results
        assert "misclick_rate" in results
        assert "bounce_rate" in results
        assert len(results["block_analytics"]) > 0
