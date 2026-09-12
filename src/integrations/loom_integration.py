"""
Loom Integration for PersonaScript.

This module handles creating, retrieving, and formatting Loom video tutorials,
embed codes, and metadata for onboarding and support systems.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LoomIntegration:
    """Integration with Loom for generating and embedding video tutorials."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Loom integration.

        Args:
            api_key: Loom API key or token
        """
        self.api_key = api_key
        logger.info("LoomIntegration initialized")

    def create_video_tutorial(
        self,
        title: str,
        description: str,
        duration_seconds: int = 120,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate or simulate the creation of a Loom video tutorial.

        Args:
            title: Title of video tutorial
            description: Description of video content
            duration_seconds: Duration in seconds
            tags: Optional tags for categorization

        Returns:
            Dict containing video metadata, URL, and embed HTML code
        """
        logger.info(f"Creating Loom video tutorial: '{title}'")
        video_id = "loom_" + str(abs(hash(title)) % 999999)
        share_url = f"https://www.loom.com/share/{video_id}"
        embed_url = f"https://www.loom.com/embed/{video_id}"
        embed_html = (
            f'<iframe src="{embed_url}" frameborder="0" webkitallowfullscreen '
            f'mozallowfullscreen allowfullscreen style="width:100%;height:400px;"></iframe>'
        )

        return {
            "video_id": video_id,
            "title": title,
            "description": description,
            "duration_seconds": duration_seconds,
            "share_url": share_url,
            "embed_url": embed_url,
            "embed_html": embed_html,
            "tags": tags or ["onboarding", "support", "tutorial"]
        }
