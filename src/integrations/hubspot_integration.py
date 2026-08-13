"""
HubSpot CRM API Integration for PersonaScript.

This module handles all interactions with the HubSpot API, including publishing blog posts,
sending marketing emails, and managing CRM objects.
"""

import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class HubSpotIntegration:
    """Integration with HubSpot API for deploying content and managing CRM objects."""

    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        """
        Initialize HubSpot integration.

        Args:
            api_key: HubSpot developer/API key (hapikey legacy)
            access_token: HubSpot Private App / OAuth access token
        """
        self.api_key = api_key
        self.access_token = access_token
        self.base_url = "https://api.hubapi.com"
        logger.info("HubSpotIntegration initialized")

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers for HubSpot API requests."""
        headers = {
            "Content-Type": "application/json"
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.api_key:
            # Private App access tokens are also frequently passed as Authorization Bearer tokens.
            # But let's also support the legacy hapikey behavior via params or direct Bearer fallback.
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _get_params(self) -> Dict[str, str]:
        """Get query parameters, handling legacy hapikey if needed."""
        params = {}
        # Only use hapikey param if access_token is not present and api_key doesn't look like a Bearer token
        # (usually hapikey is shorter, private app token starts with pat-).
        # We can add hapikey only if self.api_key is provided and self.access_token is not.
        if self.api_key and not self.access_token and not self.api_key.startswith("pat-"):
            params["hapikey"] = self.api_key
        return params

    def is_authenticated(self) -> bool:
        """Check if HubSpot API credentials are configured."""
        return bool(self.api_key or self.access_token)

    def publish_blog_post(self, blog_post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish a blog post to HubSpot CMS.

        Args:
            blog_post_data: Dictionary containing blog post properties like name, postBody, blogAuthorId, etc.

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"Publishing blog post to HubSpot: {blog_post_data.get('name', 'Untitled')}")

        if not self.is_authenticated():
            logger.warning("No HubSpot credentials provided, returning mock response")
            return self._create_mock_blog_post_response(blog_post_data)

        # HubSpot CMS Blog Posts API endpoint (v3)
        url = f"{self.base_url}/cms/v3/blogs/posts"
        headers = self._get_headers()
        params = self._get_params()

        try:
            response = requests.post(url, headers=headers, params=params, json=blog_post_data, timeout=10)
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "id": response.json().get("id", "mock-id"),
                    "url": response.json().get("url", "https://blog.example.com"),
                    "data": response.json()
                }
            else:
                logger.error(f"HubSpot blog post creation failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling HubSpot API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def send_marketing_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and send/schedule a marketing email in HubSpot.

        Args:
            email_data: Email properties such as name, subject, htmlBody, fromName, etc.

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"Creating marketing email in HubSpot: {email_data.get('name', 'Untitled')}")

        if not self.is_authenticated():
            logger.warning("No HubSpot credentials provided, returning mock response")
            return self._create_mock_email_response(email_data)

        # HubSpot Marketing Email API endpoint (v3)
        url = f"{self.base_url}/marketing/v3/emails"
        headers = self._get_headers()
        params = self._get_params()

        try:
            response = requests.post(url, headers=headers, params=params, json=email_data, timeout=10)
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "id": response.json().get("id", "mock-email-id"),
                    "data": response.json()
                }
            else:
                logger.error(f"HubSpot email creation failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling HubSpot API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def create_or_update_object(self, object_type: str, properties: Dict[str, Any], object_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create or update a standard or custom object in HubSpot CRM.

        Args:
            object_type: Type of object (e.g. "contacts", "companies", "deals")
            properties: Dictionary of properties to set
            object_id: Optional ID to update an existing object

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"CRM operation on {object_type} (ID: {object_id})")

        if not self.is_authenticated():
            logger.warning("No HubSpot credentials provided, returning mock response")
            return self._create_mock_crm_response(object_type, properties, object_id)

        headers = self._get_headers()
        params = self._get_params()

        try:
            if object_id:
                # Update
                url = f"{self.base_url}/crm/v3/objects/{object_type}/{object_id}"
                response = requests.patch(url, headers=headers, params=params, json={"properties": properties}, timeout=10)
            else:
                # Create
                url = f"{self.base_url}/crm/v3/objects/{object_type}"
                response = requests.post(url, headers=headers, params=params, json={"properties": properties}, timeout=10)

            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "id": response.json().get("id", "mock-id"),
                    "data": response.json()
                }
            else:
                logger.error(f"HubSpot CRM operation failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling HubSpot CRM API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _create_mock_blog_post_response(self, blog_post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock blog post response for demonstration purposes."""
        post_id = "mock-hubspot-blog-" + str(hash(blog_post_data.get("name", "")))[:8]
        return {
            "status": "success",
            "id": post_id,
            "url": f"https://blog.example.com/{blog_post_data.get('slug', 'mock-slug')}",
            "data": {
                "id": post_id,
                "name": blog_post_data.get("name", "Mock Blog Post"),
                "postBody": blog_post_data.get("postBody", "Mock body"),
                "publishDate": blog_post_data.get("publishDate", "2025-10-10"),
                "state": "PUBLISHED"
            }
        }

    def _create_mock_email_response(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock email response for demonstration purposes."""
        email_id = "mock-hubspot-email-" + str(hash(email_data.get("name", "")))[:8]
        return {
            "status": "success",
            "id": email_id,
            "data": {
                "id": email_id,
                "name": email_data.get("name", "Mock Email"),
                "subject": email_data.get("subject", "Mock Subject"),
                "htmlBody": email_data.get("htmlBody", "Mock body"),
                "state": "SENT"
            }
        }

    def _create_mock_crm_response(self, object_type: str, properties: Dict[str, Any], object_id: Optional[str]) -> Dict[str, Any]:
        """Create a mock CRM response for demonstration purposes."""
        crm_id = object_id or ("mock-crm-" + str(hash(str(properties)))[:8])
        return {
            "status": "success",
            "id": crm_id,
            "data": {
                "id": crm_id,
                "objectType": object_type,
                "properties": properties
            }
        }
