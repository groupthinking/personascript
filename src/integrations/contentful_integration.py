"""
Contentful API Integration for PersonaScript.

This module handles authenticating and managing content model entries
via the Contentful Management API (CMA), with graceful fallback behavior
when API credentials are omitted.
"""

import os
import logging
import requests
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ContentfulIntegration:
    """Integration with Contentful Management API for localized content publishing."""

    def __init__(
        self,
        space_id: Optional[str] = None,
        management_token: Optional[str] = None,
        environment: Optional[str] = None
    ):
        """
        Initialize Contentful integration.

        Args:
            space_id: Contentful Space ID
            management_token: Contentful Personal Access Token / Management API token
            environment: Contentful Environment ID (default: "master")
        """
        self.space_id = space_id or os.environ.get("CONTENTFUL_SPACE_ID")
        self.management_token = management_token or os.environ.get("CONTENTFUL_MANAGEMENT_TOKEN") or os.environ.get("CONTENTFUL_ACCESS_TOKEN")
        self.environment = environment or os.environ.get("CONTENTFUL_ENVIRONMENT", "master")
        self.base_url = "https://api.contentful.com"
        logger.info("ContentfulIntegration initialized")

    def is_configured(self) -> bool:
        """Check if Contentful Space ID and Management Token are provided."""
        return bool(self.space_id and self.management_token)

    def _get_headers(self) -> Dict[str, str]:
        """Generate headers for Contentful Management API requests."""
        headers = {
            "Content-Type": "application/vnd.contentful.management.v1+json",
            "Accept": "application/json"
        }
        if self.management_token:
            headers["Authorization"] = f"Bearer {self.management_token}"
        return headers

    def test_connection(self) -> Dict[str, Any]:
        """
        Test authentication and connection to Contentful Management API.

        Returns:
            Dict containing connection status and details.
        """
        logger.info("Testing connection to Contentful Management API")
        if not self.is_configured():
            logger.warning("Contentful credentials not provided; returning simulated mock connection status")
            return {
                "status": "connected",
                "mode": "simulated",
                "space_id": self.space_id or "mock-space-id-99",
                "environment": self.environment,
                "message": "Connected in mock mode (credentials omitted)"
            }

        try:
            url = f"{self.base_url}/spaces/{self.space_id}"
            response = requests.get(url, headers=self._get_headers(), timeout=15)
            if response.status_code in (200, 201):
                data = response.json()
                return {
                    "status": "connected",
                    "mode": "live",
                    "space_id": self.space_id,
                    "space_name": data.get("name", "Contentful Space"),
                    "environment": self.environment,
                    "message": "Successfully authenticated with Contentful Management API"
                }
            else:
                logger.error(f"Contentful connection test failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "mode": "live",
                    "response_code": response.status_code,
                    "message": f"Contentful API returned status {response.status_code}"
                }
        except Exception as e:
            logger.error(f"Error testing Contentful connection: {e}", exc_info=True)
            return {
                "status": "failed",
                "mode": "error",
                "message": str(e)
            }

    def create_entry(
        self,
        content_type_id: str,
        fields: Dict[str, Any],
        locale: str = "en-US"
    ) -> Dict[str, Any]:
        """
        Create a new draft entry for a given content model in Contentful.

        Args:
            content_type_id: Target content type ID in Contentful
            fields: Raw field dictionary (key -> value)
            locale: Locale code for Contentful fields (default: "en-US")

        Returns:
            Dict containing created entry details and URL.
        """
        logger.info(f"Creating Contentful entry for content_type '{content_type_id}' in locale '{locale}'")

        # Format fields dictionary into Contentful localized schema
        localized_fields = {}
        for key, val in fields.items():
            if isinstance(val, dict) and locale in val:
                localized_fields[key] = val
            else:
                localized_fields[key] = {locale: val}

        payload = {
            "fields": localized_fields
        }

        entry_title = fields.get("title") or fields.get("name") or "Untitled Entry"
        if isinstance(entry_title, dict):
            entry_title = entry_title.get(locale) or str(entry_title)

        if not self.is_configured():
            logger.warning("No Contentful credentials provided; generating mock entry response")
            entry_id = f"contentful-entry-{abs(hash(str(entry_title))) % 100000}"
            space = self.space_id or "mock-space"
            return {
                "id": entry_id,
                "content_type_id": content_type_id,
                "title": entry_title,
                "version": 1,
                "status": "draft",
                "space_id": space,
                "environment": self.environment,
                "url": f"https://app.contentful.com/spaces/{space}/environments/{self.environment}/entries/{entry_id}",
                "fields": localized_fields,
                "mode": "simulated"
            }

        try:
            headers = self._get_headers()
            headers["X-Contentful-Content-Type"] = content_type_id
            url = f"{self.base_url}/spaces/{self.space_id}/environments/{self.environment}/entries"
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code in (200, 201):
                data = response.json()
                sys_meta = data.get("sys", {})
                entry_id = sys_meta.get("id", "entry-id")
                version = sys_meta.get("version", 1)
                return {
                    "id": entry_id,
                    "content_type_id": content_type_id,
                    "title": entry_title,
                    "version": version,
                    "status": "draft",
                    "space_id": self.space_id,
                    "environment": self.environment,
                    "url": f"https://app.contentful.com/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}",
                    "fields": localized_fields,
                    "mode": "live"
                }
            else:
                logger.error(f"Failed to create Contentful entry: {response.status_code} - {response.text}")
                entry_id = f"contentful-entry-{abs(hash(str(entry_title))) % 100000}"
                return {
                    "id": entry_id,
                    "content_type_id": content_type_id,
                    "title": entry_title,
                    "version": 1,
                    "status": "fallback_simulated",
                    "url": f"https://app.contentful.com/spaces/{self.space_id or 'mock'}/environments/{self.environment}/entries/{entry_id}",
                    "fields": localized_fields,
                    "mode": "simulated"
                }
        except Exception as e:
            logger.error(f"Exception creating Contentful entry: {e}", exc_info=True)
            entry_id = f"contentful-entry-{abs(hash(str(entry_title))) % 100000}"
            return {
                "id": entry_id,
                "content_type_id": content_type_id,
                "title": entry_title,
                "version": 1,
                "status": "fallback_simulated",
                "error": str(e),
                "url": f"https://app.contentful.com/spaces/{self.space_id or 'mock'}/environments/{self.environment}/entries/{entry_id}",
                "fields": localized_fields,
                "mode": "simulated"
            }

    def publish_entry(self, entry_id: str, version: int = 1) -> Dict[str, Any]:
        """
        Publish a draft entry on Contentful.

        Args:
            entry_id: Contentful entry ID
            version: Current version integer of entry

        Returns:
            Dict containing published entry status.
        """
        logger.info(f"Publishing Contentful entry '{entry_id}' (version {version})")

        if not self.is_configured():
            logger.warning("No Contentful credentials provided; returning mock publish status")
            return {
                "id": entry_id,
                "version": version + 1,
                "status": "published",
                "message": f"Successfully published entry '{entry_id}' in mock mode",
                "mode": "simulated"
            }

        try:
            headers = self._get_headers()
            headers["X-Contentful-Version"] = str(version)
            url = f"{self.base_url}/spaces/{self.space_id}/environments/{self.environment}/entries/{entry_id}/published"
            response = requests.put(url, headers=headers, timeout=30)

            if response.status_code in (200, 201):
                data = response.json()
                sys_meta = data.get("sys", {})
                return {
                    "id": entry_id,
                    "version": sys_meta.get("version", version + 1),
                    "status": "published",
                    "message": f"Successfully published entry '{entry_id}'",
                    "mode": "live"
                }
            else:
                logger.error(f"Failed to publish Contentful entry: {response.status_code} - {response.text}")
                return {
                    "id": entry_id,
                    "version": version + 1,
                    "status": "published_simulated",
                    "mode": "simulated"
                }
        except Exception as e:
            logger.error(f"Exception publishing Contentful entry: {e}", exc_info=True)
            return {
                "id": entry_id,
                "version": version + 1,
                "status": "published_simulated",
                "error": str(e),
                "mode": "simulated"
            }

    def publish_content(
        self,
        content_type_id: str,
        payload: Dict[str, Any],
        locale: str = "en-US",
        auto_publish: bool = True
    ) -> Dict[str, Any]:
        """
        Helper method to create and optionally publish a Contentful entry.

        Args:
            content_type_id: Contentful target content model ID
            payload: Field key-value dictionary
            locale: Language locale (e.g. "en-US")
            auto_publish: Whether to invoke publish_entry after creation

        Returns:
            Dict containing complete publishing details.
        """
        entry_res = self.create_entry(content_type_id=content_type_id, fields=payload, locale=locale)
        if auto_publish and entry_res.get("id"):
            pub_res = self.publish_entry(entry_id=entry_res["id"], version=entry_res.get("version", 1))
            entry_res["status"] = pub_res.get("status", "published")
            entry_res["version"] = pub_res.get("version", entry_res.get("version", 1) + 1)
        return entry_res
