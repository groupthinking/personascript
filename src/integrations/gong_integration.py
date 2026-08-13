"""
Gong.io API Integration for PersonaScript.

This module handles interactions with the Gong.io API to retrieve call transcripts and conversational analytics.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class GongIntegration:
    """Integration with Gong.io API to retrieve call transcripts and performance analytics."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gong.io integration.

        Args:
            api_key: Gong.io API key
        """
        self.api_key = api_key
        self.base_url = "https://api.gong.io/v2"
        logger.info("GongIntegration initialized")

    def get_call_transcripts_and_analytics(self) -> Dict[str, Any]:
        """
        Retrieve call transcripts and performance analytics.

        Returns:
            Dictionary containing transcripts, conversation metrics, and representative feedback.
        """
        logger.info("Retrieving call transcripts and analytics from Gong.io")

        if not self.api_key:
            logger.warning("No Gong.io API key provided, returning mock call analytics")
            return self._get_mock_analytics()

        # Real implementation would make requests to Gong REST API
        # e.g., GET to /v2/calls or /v2/transcripts
        return self._get_mock_analytics()

    def _get_mock_analytics(self) -> Dict[str, Any]:
        """Generate mock call transcripts and performance metrics for PersonaScript."""
        return {
            "conversational_metrics": {
                "average_talk_to_listen_ratio": {
                    "representatives": 0.63,  # 63% talk, 37% listen (too high)
                    "prospects": 0.37,
                    "target_representative_ratio": 0.45,  # industry target is 43-45%
                },
                "average_longest_monologue_seconds": 145,  # too long (target < 60s)
                "average_patience_seconds": 0.8,         # low patience / cutting off prospects
                "questions_asked_per_call_average": 8.2,   # target is 11-14
            },
            "objection_analysis": {
                "pricing_objections_handled_successfully_pct": 0.32,  # low (32% success)
                "security_and_compliance_objections_success_pct": 0.40,  # low
                "competitor_objections_success_pct": 0.48,
            },
            "common_objections": [
                {
                    "topic": "Pricing / Budget",
                    "frequency_pct": 0.58,
                    "example_quote": "PersonaScript seems helpful, but the budget is tight right now and we cannot justify another SaaS subscription.",
                    "current_handling_notes": "Representatives tend to offer immediate discounts rather than emphasizing ROI or cost-savings.",
                },
                {
                    "topic": "Security / AI Safety",
                    "frequency_pct": 0.42,
                    "example_quote": "How do we know our brand-aligned content data isn't used to train public models or shared with competitors?",
                    "current_handling_notes": "Representatives struggle to explain data privacy policies and LLM boundaries clearly.",
                },
                {
                    "topic": "Integration / Compatibility",
                    "frequency_pct": 0.35,
                    "example_quote": "Does PersonaScript integrate directly into Hubspot and Marketo, or is it a separate dashboard we have to copy-paste from?",
                    "current_handling_notes": "Representatives lack technical knowledge of API pipelines and copy-paste fallback is perceived as friction.",
                }
            ],
            "transcripts_summary": [
                {
                    "call_id": "call-101",
                    "prospect_title": "Director of Growth Marketing",
                    "duration_minutes": 25,
                    "transcript_snippet": (
                        "Prospect: We generate a lot of content but scaling it across 5 personas is painful. "
                        "How does PersonaScript automate that without sounding robotic?\n"
                        "Rep: Oh, our AI is very advanced. It uses advanced algorithms. "
                        "You just click button and it generates content. Let me show you a 15-minute demo on my screen."
                    ),
                    "bottleneck_identified": "Lack of qualification/discovery before moving to demo; talking too much about features instead of persona pain points.",
                },
                {
                    "call_id": "call-102",
                    "prospect_title": "VP of Marketing",
                    "duration_minutes": 35,
                    "transcript_snippet": (
                        "Prospect: We have strict brand guidelines. "
                        "If the AI outputs something off-brand, it's a huge liability for us.\n"
                        "Rep: Don't worry, you can always edit it in our UI before publishing."
                    ),
                    "bottleneck_identified": "Weak objection handling. Missed opportunity to highlight PersonaScript's deterministic brand-voice consistency and style guide enforcement engine.",
                }
            ]
        }
