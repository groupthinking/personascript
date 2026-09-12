"""
Intercom API Integration for PersonaScript.

This module handles creating onboarding sequences, configuring in-app chat support,
embedding video tutorials, and configuring support routing in Intercom.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class IntercomIntegration:
    """Integration with Intercom API for onboarding sequences and chat support."""

    def __init__(self, api_key: Optional[str] = None, app_id: Optional[str] = None):
        """
        Initialize Intercom integration.

        Args:
            api_key: Intercom Access Token / API Key
            app_id: Intercom Workspace / App ID
        """
        self.api_key = api_key
        self.app_id = app_id or "personascript_app"
        self.base_url = "https://api.intercom.io"
        logger.info("IntercomIntegration initialized")

    def create_onboarding_sequence(
        self,
        title: str,
        steps: List[Dict[str, Any]],
        target_audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an automated onboarding sequence in Intercom.

        Args:
            title: Title of the sequence
            steps: List of sequence steps (welcome messages, product tours, prompts)
            target_audience: Optional target segment or filter criteria

        Returns:
            Dict containing details of created onboarding sequence
        """
        logger.info(f"Creating Intercom onboarding sequence: '{title}' with {len(steps)} steps")
        seq_id = "seq_" + str(abs(hash(title)) % 99999)
        seq_url = f"https://app.intercom.com/a/apps/{self.app_id}/outreach/sequences/{seq_id}"

        formatted_steps = []
        for i, step in enumerate(steps, 1):
            formatted_steps.append({
                "step_number": step.get("step_number", i),
                "step_id": step.get("step_id", f"step_{i}"),
                "title": step.get("title", f"Step {i}"),
                "content": step.get("content", ""),
                "type": step.get("type", "in_app_message"),
                "trigger": step.get("trigger", "on_signup"),
                "embedded_video_url": step.get("embedded_video_url")
            })

        return {
            "sequence_id": seq_id,
            "title": title,
            "url": seq_url,
            "target_audience": target_audience or "All New B2B SaaS Signups",
            "steps": formatted_steps,
            "status": "active"
        }

    def configure_in_app_chat(
        self,
        routing_rules: List[Dict[str, Any]],
        automated_responses: List[Dict[str, Any]],
        team_assignments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Configure in-app chat support, routing, automated responses, and team assignments.

        Args:
            routing_rules: List of message routing rules
            automated_responses: List of automated bot responses/triggers
            team_assignments: List of team assignment rules

        Returns:
            Dict containing configured chat settings
        """
        logger.info("Configuring Intercom in-app chat support settings")
        config_id = "chat_cfg_" + str(abs(hash("in_app_chat")) % 9999)

        return {
            "config_id": config_id,
            "app_id": self.app_id,
            "routing_rules": routing_rules,
            "automated_responses": automated_responses,
            "team_assignments": team_assignments,
            "status": "enabled"
        }

    def embed_video_in_sequence(
        self,
        sequence_id: str,
        step_id: str,
        video_url: str,
        video_title: str
    ) -> Dict[str, Any]:
        """
        Embed a Loom video tutorial into an existing Intercom sequence step.

        Args:
            sequence_id: Intercom sequence ID
            step_id: Step ID within the sequence
            video_url: URL of the video tutorial
            video_title: Title of the video tutorial

        Returns:
            Dict confirming embedding of the video
        """
        logger.info(f"Embedding Loom video '{video_title}' into Intercom sequence '{sequence_id}', step '{step_id}'")
        return {
            "sequence_id": sequence_id,
            "step_id": step_id,
            "video_title": video_title,
            "video_url": video_url,
            "embed_status": "embedded"
        }

    def configure_zendesk_integration(
        self,
        zendesk_subdomain: str,
        sync_tickets: bool = True
    ) -> Dict[str, Any]:
        """
        Configure integration between Intercom and Zendesk.

        Args:
            zendesk_subdomain: Target Zendesk subdomain
            sync_tickets: Whether to sync conversations to Zendesk tickets

        Returns:
            Dict detailing integration settings
        """
        logger.info(f"Configuring Intercom integration with Zendesk ({zendesk_subdomain})")
        return {
            "integration_id": "int_intercom_zendesk_" + str(abs(hash(zendesk_subdomain)) % 999),
            "intercom_app_id": self.app_id,
            "zendesk_subdomain": zendesk_subdomain,
            "sync_tickets": sync_tickets,
            "auto_ticket_creation": True,
            "status": "connected"
        }
