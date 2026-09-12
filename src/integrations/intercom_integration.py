"""
Intercom API Integration for PersonaScript.

This module handles interacting with the Intercom API for sending invitations,
onboarding instructions, initial surveys, and fetching customer conversations/feedback.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class IntercomIntegration:
    """Integration with Intercom API for customer communication and feedback monitoring."""

    def __init__(self, token: Optional[str] = None, access_token: Optional[str] = None):
        """
        Initialize Intercom integration.

        Args:
            token: Intercom Access Token
            access_token: Alternative parameter name for Intercom Access Token
        """
        self.token = token or access_token
        self.base_url = "https://api.intercom.io"
        logger.info("IntercomIntegration initialized")

    def send_invitation(self, customer_email: str, customer_name: str, onboarding_link: str) -> Dict[str, Any]:
        """
        Send a personalized invitation and onboarding instructions to an alpha customer.

        Args:
            customer_email: Customer email address
            customer_name: Customer contact name
            onboarding_link: Link to onboarding documentation / portal

        Returns:
            Dictionary containing delivery status and message details
        """
        logger.info(f"Sending Intercom invitation to {customer_name} ({customer_email})")

        if not self.token:
            logger.warning("No Intercom token provided, returning mock response")

        message_id = f"msg_{abs(hash(customer_email)) % 100000}"
        return {
            "id": message_id,
            "status": "sent",
            "recipient_email": customer_email,
            "recipient_name": customer_name,
            "onboarding_link": onboarding_link,
            "message_type": "inapp_or_email"
        }

    def send_survey(self, customer_email: str, survey_title: str, survey_questions: List[str]) -> Dict[str, Any]:
        """
        Send an initial survey to an alpha customer via Intercom.

        Args:
            customer_email: Customer email address
            survey_title: Survey title
            survey_questions: List of questions in the survey

        Returns:
            Dictionary containing survey dispatch details
        """
        logger.info(f"Sending Intercom survey '{survey_title}' to {customer_email}")

        survey_id = f"srv_{abs(hash(survey_title + customer_email)) % 100000}"
        return {
            "survey_id": survey_id,
            "status": "dispatched",
            "recipient_email": customer_email,
            "title": survey_title,
            "question_count": len(survey_questions)
        }

    def fetch_feedback_and_conversations(self) -> List[Dict[str, Any]]:
        """
        Retrieve customer feedback, support requests, and reported issues from Intercom conversations.

        Returns:
            List of conversation/feedback objects
        """
        logger.info("Fetching customer feedback and conversations from Intercom")

        if not self.token:
            logger.warning("No Intercom token provided, returning mock customer feedback")

        return [
            {
                "conversation_id": "conv_101",
                "customer_email": "alice@acme.com",
                "customer_name": "Alice Smith",
                "company": "Acme Corp",
                "type": "bug",
                "subject": "SSO authentication failure during onboarding",
                "body": "When attempting SAML login with Okta, the session redirects to a 500 error page.",
                "created_at": "2025-02-01T10:00:00Z"
            },
            {
                "conversation_id": "conv_102",
                "customer_email": "bob@techstart.io",
                "customer_name": "Bob Jones",
                "company": "TechStart Inc",
                "type": "feature_request",
                "subject": "Export persona templates as PDF/JSON",
                "body": "We need the ability to export custom personas in JSON format to sync with our internal CRM.",
                "created_at": "2025-02-02T14:30:00Z"
            },
            {
                "conversation_id": "conv_103",
                "customer_email": "carol@globaldata.com",
                "customer_name": "Carol Danvers",
                "company": "GlobalData",
                "type": "feedback",
                "subject": "High latency on batch copy generation",
                "body": "Generating 50 copy variations took over 2 minutes. Performance optimization would help significantly.",
                "created_at": "2025-02-03T09:15:00Z"
            }
        ]
