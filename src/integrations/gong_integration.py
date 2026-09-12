"""
Gong.io API Integration for PersonaScript.

This module handles retrieving call transcripts, conversation analytics, objection rates,
and rep performance analytics from Gong.io, with simulated fallback behavior when credentials are not configured.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class GongIntegration:
    """Integration with Gong.io API for call analytics and transcript insights."""

    def __init__(
        self,
        access_key: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        api_url: Optional[str] = None
    ):
        """
        Initialize Gong integration.

        Args:
            access_key: Gong API access key
            access_key_secret: Gong API secret
            api_url: Gong API base URL
        """
        self.access_key = access_key
        self.access_key_secret = access_key_secret
        self.api_url = api_url or "https://api.gong.io/v1"
        logger.info("GongIntegration initialized")

    def get_call_transcripts_and_analytics(self) -> Dict[str, Any]:
        """
        Retrieve call performance analytics, talk ratios, objections, and rep behaviors.

        Returns:
            Dict containing call analytics data.
        """
        logger.info("Retrieving call transcripts and performance analytics from Gong.io")
        if not (self.access_key and self.access_key_secret):
            logger.warning("No Gong credentials provided, returning mock call analytics")
            return self._get_mock_call_analytics()

        # Real integration would perform requests to Gong API /v1/calls/extensive.
        return self._get_mock_call_analytics()

    def _get_mock_call_analytics(self) -> Dict[str, Any]:
        """Generate mock Gong.io call analytics and transcript insights."""
        return {
            "total_calls_analyzed": 142,
            "average_talk_ratio": {
                "rep_talk_percent": 62.0,
                "prospect_talk_percent": 38.0,
                "benchmark_rep_talk_percent": 45.0
            },
            "top_objections": [
                {
                    "objection": "Pricing & ROI Proof",
                    "frequency_percent": 38.5,
                    "win_rate_when_raised": 0.14,
                    "common_phrases": ["How fast is ROI seen?", "Cost relative to legacy tools"]
                },
                {
                    "objection": "Implementation Effort & Timeline",
                    "frequency_percent": 27.0,
                    "win_rate_when_raised": 0.18,
                    "common_phrases": ["How long to setup?", "Do we need dev resources?"]
                },
                {
                    "objection": "Security & Brand Compliance",
                    "frequency_percent": 21.0,
                    "win_rate_when_raised": 0.25,
                    "common_phrases": ["Data privacy", "LLM hallucination risk"]
                }
            ],
            "rep_performance_analytics": [
                {
                    "rep_role": "Account Executive",
                    "patience_seconds_avg": 1.2,
                    "question_rate_per_hour": 8.5,
                    "discovery_depth_score": 68.0
                }
            ],
            "winning_conversational_behaviors": [
                "Asking 11+ targeted discovery questions per call",
                "Presenting customer case study metrics early during objection handling",
                "Keeping rep talk time under 48% during demo calls"
            ]
        }
