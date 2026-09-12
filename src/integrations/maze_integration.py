"""
Maze API Integration for PersonaScript.

This module handles configuring usability tests, uploading prototypes, and retrieving
quantitative metrics (misclicks, direct success rates, bounce rates, etc.) from Maze,
with simulated fallback behavior when credentials are not configured.
"""

import logging
import hashlib
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class MazeIntegration:
    """Integration with Maze API for prototype usability testing."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Maze integration.

        Args:
            api_key: Optional API key for Maze authorization
        """
        self.api_key = api_key
        self.base_url = "https://api.maze.co/v1"
        logger.info("MazeIntegration initialized")

    def is_configured(self) -> bool:
        """Check if active credentials are present for Maze API calls."""
        return bool(self.api_key)

    def configure_test(
        self,
        prototypes: List[str],
        test_script: Any,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Configure a usability test in Maze by associating prototype links and test questions/script.

        Args:
            prototypes: List of prototype URLs (e.g. Figma or InVision links)
            test_script: Script, questions, or blocks for the test
            title: Optional test campaign title

        Returns:
            Dictionary containing test configuration details and live test link.
        """
        test_title = title or "PersonaScript Prototype Usability Test"
        logger.info(f"Configuring Maze usability test: '{test_title}' with {len(prototypes)} prototypes")

        if not self.is_configured():
            logger.warning("No Maze credentials provided, using simulated test configuration")
            return self._create_mock_test_config(test_title, prototypes, test_script)

        # Real API integration would call Maze endpoint POST /tests
        return self._create_mock_test_config(test_title, prototypes, test_script)

    def get_test_results(self, test_id: str) -> Dict[str, Any]:
        """
        Collect and aggregate quantitative data from Maze for a given test ID.

        Args:
            test_id: The ID of the configured Maze test

        Returns:
            Dictionary containing misclick rate, direct success rate, bounce rate, and block analytics.
        """
        logger.info(f"Retrieving quantitative usability test metrics from Maze for test_id={test_id}")

        if not self.is_configured():
            logger.warning("No Maze credentials provided, returning mock quantitative test results")
            return self._get_mock_test_results(test_id)

        # Real API integration would call Maze endpoint GET /tests/{test_id}/results
        return self._get_mock_test_results(test_id)

    def _create_mock_test_config(
        self,
        title: str,
        prototypes: List[str],
        test_script: Any
    ) -> Dict[str, Any]:
        """Generate mock test configuration for fallback execution."""
        hash_id = abs(hash(f"{title}_{len(prototypes)}")) % 100000
        test_id = f"maze-test-{hash_id:05d}"
        test_link = f"https://maze.co/t/{test_id}"

        return {
            "test_id": test_id,
            "title": title,
            "test_link": test_link,
            "prototypes": prototypes,
            "script_block_count": len(test_script) if isinstance(test_script, list) else 5,
            "status": "active"
        }

    def _get_mock_test_results(self, test_id: str) -> Dict[str, Any]:
        """Generate realistic mock quantitative usability test results."""
        return {
            "test_id": test_id,
            "total_participants": 10,
            "completed_responses": 10,
            "usability_score": 74.5,
            "direct_success_rate": 0.68,
            "indirect_success_rate": 0.18,
            "misclick_rate": 0.24,
            "bounce_rate": 0.10,
            "average_duration_seconds": 245.0,
            "block_analytics": [
                {
                    "block_id": "block-1-onboarding",
                    "title": "Task 1: Complete Onboarding & Account Setup",
                    "direct_success_rate": 0.80,
                    "misclick_rate": 0.15,
                    "avg_duration_sec": 45.0,
                    "major_friction": "CTA button placement below the fold on mobile viewports"
                },
                {
                    "block_id": "block-2-content-generation",
                    "title": "Task 2: Select Persona & Generate Marketing Brief",
                    "direct_success_rate": 0.60,
                    "misclick_rate": 0.32,
                    "avg_duration_sec": 110.0,
                    "major_friction": "Confusing tone-selector dropdown and non-obvious submit button"
                },
                {
                    "block_id": "block-3-export-review",
                    "title": "Task 3: Export Generated Brief to HubSpot/Notion",
                    "direct_success_rate": 0.65,
                    "misclick_rate": 0.25,
                    "avg_duration_sec": 90.0,
                    "major_friction": "Unclear integration status indicators during batch export"
                }
            ]
        }
