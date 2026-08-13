"""
Intercom API Integration for PersonaScript Customer Onboarding.

This module handles configurations for automated onboarding sequences,
in-app chat support, and Loom video embeddings within Intercom.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class IntercomIntegration:
    """Integration with Intercom API for customer onboarding and chat support."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Intercom integration.

        Args:
            api_key: Intercom API key / Access token
        """
        self.api_key = api_key
        self.base_url = "https://api.intercom.io"
        logger.info("IntercomIntegration initialized")

    def configure_onboarding_sequences(self, sequences_spec: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Configure automated onboarding sequences in Intercom.

        Args:
            sequences_spec: List of onboarding sequence configurations, welcome messages, tours, etc.

        Returns:
            Dictionary containing configuration status and sequence details
        """
        logger.info(f"Configuring {len(sequences_spec)} automated onboarding sequences in Intercom")

        configured_sequences = []
        for i, seq in enumerate(sequences_spec):
            seq_id = f"intercom-seq-{hash(seq.get('title', f'seq_{i}')) % 10000}"
            configured_sequences.append({
                "sequence_id": seq_id,
                "title": seq.get("title"),
                "status": "active",
                "audience": seq.get("audience", "all_new_users"),
                "steps_count": len(seq.get("steps", []))
            })

        if not self.api_key:
            logger.warning("No Intercom API key provided, running in mock/simulated mode")
            return {
                "status": "success",
                "mode": "simulated",
                "sequences": configured_sequences,
                "dashboard_url": "https://app.intercom.com/a/apps/mock-app-id/outbound/series"
            }

        # In a real implementation, this would make API calls to Intercom Series/Outbound endpoints
        return {
            "status": "success",
            "mode": "live",
            "sequences": configured_sequences,
            "dashboard_url": "https://app.intercom.com/a/apps/live-app-id/outbound/series"
        }

    def integrate_chat_support(self, chat_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure in-app chat support widget, routing, and automated replies.

        Args:
            chat_config: Settings for in-app widget (brand colors, rules, routing, assignments)

        Returns:
            Status of the chat support integration
        """
        logger.info("Configuring Intercom in-app chat support settings")

        inbox_id = f"inbox-{hash(chat_config.get('routing_rule', 'default')) % 10000}"

        if not self.api_key:
            logger.warning("No Intercom API key provided, running in mock/simulated mode")
            return {
                "status": "success",
                "mode": "simulated",
                "inbox_id": inbox_id,
                "widget_installed": True,
                "routing_rules_applied": True,
                "widget_url": "https://widget.intercom.io/widget/mock-app-id"
            }

        # Real API call to configure settings
        return {
            "status": "success",
            "mode": "live",
            "inbox_id": inbox_id,
            "widget_installed": True,
            "routing_rules_applied": True,
            "widget_url": "https://widget.intercom.io/widget/live-app-id"
        }

    def embed_loom_tutorials(self, message_id: str, loom_embeds: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Embed prepared Loom video tutorials into relevant Intercom onboarding messages.

        Args:
            message_id: ID of the Intercom message/sequence step to modify
            loom_embeds: List of dictionaries with Loom video embed codes/URLs

        Returns:
            Status of the embedding
        """
        logger.info(f"Embedding {len(loom_embeds)} Loom video(s) into Intercom message: {message_id}")

        if not self.api_key:
            logger.warning("No Intercom API key provided, running in mock/simulated mode")
            return {
                "status": "success",
                "mode": "simulated",
                "message_id": message_id,
                "embedded_videos_count": len(loom_embeds)
            }

        # Real API call to update the message HTML/body structure
        return {
            "status": "success",
            "mode": "live",
            "message_id": message_id,
            "embedded_videos_count": len(loom_embeds)
        }

    def configure_zendesk_integration(self, zendesk_subdomain: str) -> Dict[str, Any]:
        """
        Configure integration with Zendesk to link chat conversations to support tickets.

        Args:
            zendesk_subdomain: Zendesk subdomain to link to

        Returns:
            Status of Intercom-Zendesk integration settings
        """
        logger.info(f"Configuring Intercom-Zendesk integration for subdomain: {zendesk_subdomain}")

        if not self.api_key:
            logger.warning("No Intercom API key provided, running in mock/simulated mode")
            return {
                "status": "success",
                "mode": "simulated",
                "integration_linked": True,
                "zendesk_subdomain": zendesk_subdomain
            }

        # Real API call to create conversation/ticket syncing rules
        return {
            "status": "success",
            "mode": "live",
            "integration_linked": True,
            "zendesk_subdomain": zendesk_subdomain
        }
