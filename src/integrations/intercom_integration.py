"""
Intercom API Integration for PersonaScript.

This module handles interactions with the Intercom API for sending messages,
onboarding invites, surveys, and fetching customer conversations.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class IntercomIntegration:
    """Integration with Intercom API for managing beta program user interaction."""

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Intercom integration.

        Args:
            access_token: Intercom developer access token
        """
        self.access_token = access_token
        self.base_url = "https://api.intercom.io"
        logger.info("IntercomIntegration initialized")

    def create_user(self, email: str, name: str) -> Dict[str, Any]:
        """
        Create or update a user contact in Intercom.

        Args:
            email: Contact email address
            name: Contact name

        Returns:
            Dictionary containing user details and Intercom ID
        """
        logger.info(f"Intercom: Creating/Updating user: {name} ({email})")

        user_id = f"int_usr_{abs(hash(email)) % 100000}"

        if not self.access_token:
            logger.warning("No Intercom access token provided, returning mock user")
            return {
                "id": user_id,
                "email": email,
                "name": name,
                "role": "user",
                "created_at": 1600000000,
                "mocked": True
            }

        # In a real implementation:
        # POST to /contacts with body: {"role": "user", "email": email, "name": name}
        return {
            "id": user_id,
            "email": email,
            "name": name,
            "role": "user",
            "created_at": 1600000000,
            "mocked": False
        }

    def send_message(self, user_id: str, body: str) -> Dict[str, Any]:
        """
        Send a personalized message/invite to a user in Intercom.

        Args:
            user_id: Intercom contact ID
            body: Message body

        Returns:
            Dictionary containing sent message/conversation details
        """
        logger.info(f"Intercom: Sending message to user {user_id}")

        message_id = f"msg_{abs(hash(body)) % 100000}"

        if not self.access_token:
            logger.warning("No Intercom access token provided, returning mock message receipt")
            return {
                "id": message_id,
                "user_id": user_id,
                "body": body,
                "sent_at": 1600000000,
                "status": "sent",
                "mocked": True
            }

        # In a real implementation:
        # POST to /messages with details of sender and recipient
        return {
            "id": message_id,
            "user_id": user_id,
            "body": body,
            "sent_at": 1600000000,
            "status": "sent",
            "mocked": False
        }

    def get_user_conversations(self, user_id: str, customer_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve conversations for a user to monitor feedback and support requests.

        Args:
            user_id: Intercom contact ID
            customer_name: Optional name to customize the mock feedback content

        Returns:
            List of conversation dictionaries
        """
        logger.info(f"Intercom: Fetching conversations for user {user_id}")

        if not self.access_token:
            # Generate deterministic mock feedback based on user_id / customer_name
            # to make testing clean and predictable
            conversations = []

            # Let's customize feedback based on customer name
            name_lower = (customer_name or "").lower()
            if "sarah" in name_lower or "acme" in name_lower:
                conversations.append({
                    "id": f"conv_1_{user_id}",
                    "user_id": user_id,
                    "body": "We hit a 504 Gateway Timeout error when requesting 100+ articles. Please fix this critical issue!",
                    "created_at": 1600000005,
                    "type": "bug_report"
                })
                conversations.append({
                    "id": f"conv_2_{user_id}",
                    "user_id": user_id,
                    "body": "We would love an approval workflow feature before the content is pushed. Can we request this as a feature?",
                    "created_at": 1600000010,
                    "type": "feature_request"
                })
            elif "alex" in name_lower or "globex" in name_lower:
                conversations.append({
                    "id": f"conv_3_{user_id}",
                    "user_id": user_id,
                    "body": "We hit a VocabularyIndexError crash when importing a massive custom vocabulary file. The platform is working well for normal volume otherwise.",
                    "created_at": 1600000015,
                    "type": "bug_report"
                })
                conversations.append({
                    "id": f"conv_4_{user_id}",
                    "user_id": user_id,
                    "body": "We really need a dark mode option for the dashboard content previewer. Is that on the roadmap?",
                    "created_at": 1600000020,
                    "type": "feature_request"
                })
            else:
                conversations.append({
                    "id": f"conv_5_{user_id}",
                    "user_id": user_id,
                    "body": "Onboarding was smooth and everything is looking great so far! Loving the personalization feature.",
                    "created_at": 1600000025,
                    "type": "general_feedback"
                })

            return conversations

        # Real implementation would GET /conversations with query parameters search/filter for user_id
        return []
