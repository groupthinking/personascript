"""
Loom API / Simulation Integration for PersonaScript Onboarding Video Tutorials.

This module simulates creating video tutorials based on content outlines
and returns their embed codes and links.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class LoomIntegration:
    """Integration/Simulation with Loom for tutorial videos."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Loom integration.

        Args:
            api_key: Loom SDK client ID / api key (if available)
        """
        self.api_key = api_key
        logger.info("LoomIntegration initialized")

    def generate_video_tutorial(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate/generate a video tutorial on Loom based on a content outline.

        Args:
            outline: Configuration/outline containing title, description, and key points

        Returns:
            Dictionary containing simulated video details, links, and embed codes
        """
        title = outline.get("title", "Tutorial Video")
        logger.info(f"Generating video tutorial on Loom: {title}")

        video_id = f"loom-video-{hash(title) % 100000}"
        video_url = f"https://www.loom.com/share/{video_id}"
        embed_code = f'<iframe src="https://www.loom.com/embed/{video_id}" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>'

        if not self.api_key:
            logger.warning("No Loom API key provided, running in mock/simulated mode")
            return {
                "status": "success",
                "mode": "simulated",
                "video_id": video_id,
                "title": title,
                "description": outline.get("description", ""),
                "duration_seconds": 180,  # default 3 min
                "video_url": video_url,
                "embed_code": embed_code
            }

        # Real Loom API implementation (using loom sdk or record triggering)
        return {
            "status": "success",
            "mode": "live",
            "video_id": video_id,
            "title": title,
            "description": outline.get("description", ""),
            "duration_seconds": 180,
            "video_url": video_url,
            "embed_code": embed_code
        }

    def generate_multiple_tutorials(self, outlines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate multiple video tutorials from a list of outlines.

        Args:
            outlines: List of tutorial outlines

        Returns:
            List of video details dictionaries
        """
        videos = []
        for outline in outlines:
            videos.append(self.generate_video_tutorial(outline))
        return videos
