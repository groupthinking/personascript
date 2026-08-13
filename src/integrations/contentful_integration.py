"""
Contentful CMS Management API Integration for PersonaScript.

This module handles all interactions with the Contentful Management API, including creating,
updating, and publishing content entries with support for localized fields.
"""

import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class ContentfulIntegration:
    """Integration with Contentful Management API for creating and publishing content."""

    def __init__(
        self,
        space_id: Optional[str] = None,
        access_token: Optional[str] = None,
        environment_id: str = "master"
    ):
        """
        Initialize Contentful integration.

        Args:
            space_id: Contentful Space ID
            access_token: Contentful Management API access token (CMA)
            environment_id: Contentful environment (default: 'master')
        """
        self.space_id = space_id
        self.access_token = access_token
        self.environment_id = environment_id
        self.base_url = "https://api.contentful.com"
        logger.info("ContentfulIntegration initialized")

    def _get_headers(self, version: Optional[int] = None, content_type_id: Optional[str] = None) -> Dict[str, str]:
        """Get request headers for Contentful Management API."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/vnd.contentful.management.v1+json"
        }
        if version is not None:
            headers["X-Contentful-Version"] = str(version)
        if content_type_id is not None:
            headers["X-Contentful-Content-Type"] = content_type_id
        return headers

    def is_authenticated(self) -> bool:
        """Check if Contentful API credentials are configured."""
        return bool(self.space_id and self.access_token)

    def localize_fields(self, fields: Dict[str, Any], locale: str = "en-US") -> Dict[str, Dict[str, Any]]:
        """
        Format standard flat fields into Contentful's localized fields structure.
        E.g., {"title": "Hello"} -> {"title": {"en-US": "Hello"}}

        Args:
            fields: Flat dictionary of field keys and values
            locale: Target locale string (default: 'en-US')

        Returns:
            Dictionary with Contentful's localized structure
        """
        localized = {}
        for key, val in fields.items():
            # If the value is already a dict and looks like localization, keep it
            if isinstance(val, dict) and any(k.count("-") == 1 for k in val.keys()):
                localized[key] = val
            else:
                localized[key] = {locale: val}
        return localized

    def create_entry(
        self,
        content_type_id: str,
        fields: Dict[str, Any],
        locale: str = "en-US"
    ) -> Dict[str, Any]:
        """
        Create a new draft entry in Contentful.

        Args:
            content_type_id: Content Type ID
            fields: Flat dictionary of field values
            locale: Locale to use for localization

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"Creating entry of type '{content_type_id}' in Contentful")

        # Localize fields for Contentful format
        localized_fields = self.localize_fields(fields, locale=locale)

        if not self.is_authenticated():
            logger.warning("No Contentful credentials provided, returning mock response")
            return self._create_mock_entry_response(content_type_id, fields, locale)

        url = f"{self.base_url}/spaces/{self.space_id}/environments/{self.environment_id}/entries"
        headers = self._get_headers(content_type_id=content_type_id)
        payload = {"fields": localized_fields}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                res_data = response.json()
                return {
                    "status": "success",
                    "id": res_data.get("sys", {}).get("id"),
                    "version": res_data.get("sys", {}).get("version", 1),
                    "data": res_data
                }
            else:
                logger.error(f"Contentful entry creation failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling Contentful API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def update_entry(
        self,
        entry_id: str,
        fields: Dict[str, Any],
        version: int,
        locale: str = "en-US"
    ) -> Dict[str, Any]:
        """
        Update an existing draft entry in Contentful.

        Args:
            entry_id: ID of entry to update
            fields: Flat dictionary of field values
            version: Current version of entry (required by Contentful)
            locale: Locale to use for localization

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"Updating entry '{entry_id}' in Contentful")

        localized_fields = self.localize_fields(fields, locale=locale)

        if not self.is_authenticated():
            logger.warning("No Contentful credentials provided, returning mock response")
            return self._create_mock_entry_response(
                content_type_id="unknown", fields=fields, locale=locale, entry_id=entry_id, version=version + 1
            )

        url = f"{self.base_url}/spaces/{self.space_id}/environments/{self.environment_id}/entries/{entry_id}"
        headers = self._get_headers(version=version)
        payload = {"fields": localized_fields}

        try:
            response = requests.put(url, headers=headers, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                res_data = response.json()
                return {
                    "status": "success",
                    "id": res_data.get("sys", {}).get("id"),
                    "version": res_data.get("sys", {}).get("version", version + 1),
                    "data": res_data
                }
            else:
                logger.error(f"Contentful entry update failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling Contentful API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def publish_entry(self, entry_id: str, version: int) -> Dict[str, Any]:
        """
        Publish a draft entry in Contentful.

        Args:
            entry_id: ID of the entry to publish
            version: Current version of the entry (required by Contentful)

        Returns:
            Dictionary containing the API response or mock response
        """
        logger.info(f"Publishing entry '{entry_id}' in Contentful")

        if not self.is_authenticated():
            logger.warning("No Contentful credentials provided, returning mock response")
            return {
                "status": "success",
                "id": entry_id,
                "version": version + 1,
                "published": True
            }

        url = f"{self.base_url}/spaces/{self.space_id}/environments/{self.environment_id}/entries/{entry_id}/published"
        headers = self._get_headers(version=version)

        try:
            response = requests.put(url, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                res_data = response.json()
                return {
                    "status": "success",
                    "id": res_data.get("sys", {}).get("id", entry_id),
                    "version": res_data.get("sys", {}).get("version", version + 1),
                    "published": True,
                    "data": res_data
                }
            else:
                logger.error(f"Contentful entry publish failed: {response.status_code} - {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"Error calling Contentful API: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _create_mock_entry_response(
        self,
        content_type_id: str,
        fields: Dict[str, Any],
        locale: str,
        entry_id: Optional[str] = None,
        version: int = 1
    ) -> Dict[str, Any]:
        """Create a mock entry response for demonstration purposes."""
        eid = entry_id or ("mock-contentful-entry-" + str(hash(str(fields)))[:8])
        return {
            "status": "success",
            "id": eid,
            "version": version,
            "data": {
                "sys": {
                    "id": eid,
                    "type": "Entry",
                    "version": version,
                    "contentType": {
                        "sys": {
                            "type": "Link",
                            "linkType": "ContentType",
                            "id": content_type_id
                        }
                    }
                },
                "fields": self.localize_fields(fields, locale=locale)
            }
        }
