"""
PartnerStack API Integration for PersonaScript Partnership Scout.

This module handles looking up programs, integration partners, and complementary services.
"""

import logging
from typing import Dict, Any, Optional, List
import requests

logger = logging.getLogger(__name__)


class PartnerStackIntegration:
    """Integration with PartnerStack API / Web Scraping for partnership search."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PartnerStack integration.

        Args:
            api_key: PartnerStack API token or key.
        """
        self.api_key = api_key
        logger.info("PartnerStackIntegration initialized")

    def search_marketplace(
        self,
        categories: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Explore PartnerStack's ecosystem for existing programs and integrations.

        Args:
            categories: Optional list of categories to filter by.
            keywords: Optional search terms.

        Returns:
            List of complementary service or technology partner listings.
        """
        logger.info(f"Searching PartnerStack ecosystem with keywords: {keywords}")

        if not self.api_key:
            logger.warning("No PartnerStack API key provided, using simulated search results")
            return self._get_simulated_marketplace_listings()

        try:
            url = "https://api.partnerstack.com/v1/programs"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json"
            }
            params = {}
            if keywords:
                params["search"] = " ".join(keywords)

            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                programs = data.get("programs", [])
                if programs:
                    mapped = []
                    for prog in programs:
                        mapped.append({
                            "name": prog.get("name", "Unknown Program"),
                            "type": "Marketing Technology Provider",
                            "partnerstack_program_url": prog.get("application_url", f"https://partnerstack.com/marketplace/{prog.get('id')}"),
                            "description": prog.get("tagline", "") or prog.get("description", ""),
                            "category": prog.get("category", "Software"),
                            "commission_structure": "Standard Commission Model",
                            "overlap_score": 0.8,
                            "integrations_supported": ["APIs"]
                        })
                    return mapped

            logger.warning(f"PartnerStack API returned {response.status_code}, falling back to simulated results")
            return self._get_simulated_marketplace_listings()
        except Exception as e:
            logger.error(f"Error calling PartnerStack API: {e}", exc_info=True)
            return self._get_simulated_marketplace_listings()

    def _get_simulated_marketplace_listings(self) -> List[Dict[str, Any]]:
        """Return simulated PartnerStack marketplace listings."""
        return [
            {
                "name": "Unbounce",
                "type": "Marketing Technology Provider",
                "partnerstack_program_url": "https://partnerstack.com/marketplace/unbounce",
                "description": "The drag-and-drop landing page builder that drives conversion and leads.",
                "category": "Conversion Rate Optimization",
                "commission_structure": "20% recurring referral commission",
                "overlap_score": 0.85,
                "integrations_supported": ["Webhooks", "Zapier", "HubSpot", "Marketo"]
            },
            {
                "name": "G2",
                "type": "Marketing Technology Provider",
                "partnerstack_program_url": "https://partnerstack.com/marketplace/g2",
                "description": "The largest software marketplace and peer-to-peer review site.",
                "category": "Review Management & Lead Gen",
                "commission_structure": "Custom agency partner rates",
                "overlap_score": 0.75,
                "integrations_supported": ["HubSpot", "Salesforce", "Marketo"]
            },
            {
                "name": "Copy.ai",
                "type": "Marketing Technology Provider",
                "partnerstack_program_url": "https://partnerstack.com/marketplace/copyai",
                "description": "AI-powered copywriting assistant for teams and agencies.",
                "category": "Content Generation",
                "commission_structure": "30% recurring first-year commission",
                "overlap_score": 0.90,
                "integrations_supported": ["Chrome Extension", "APIs", "Zapier"]
            },
            {
                "name": "Lattice",
                "type": "HR Tech & Performance Provider",
                "partnerstack_program_url": "https://partnerstack.com/marketplace/lattice",
                "description": "Performance management software that helps people-centric companies succeed.",
                "category": "People & Operations",
                "commission_structure": "Flat referral fee",
                "overlap_score": 0.30,
                "integrations_supported": ["Slack", "Google Workspace"]
            },
            {
                "name": "Wistia",
                "type": "Marketing Technology Provider",
                "partnerstack_program_url": "https://partnerstack.com/marketplace/wistia",
                "description": "Video hosting, video marketing, and video analytics for B2B brands.",
                "category": "Video Marketing",
                "commission_structure": "20% recurring commission",
                "overlap_score": 0.80,
                "integrations_supported": ["HubSpot", "Marketo", "ActiveCampaign", "Zapier"]
            }
        ]
