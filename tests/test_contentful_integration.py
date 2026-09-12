"""Tests for Contentful API Integration."""

import pytest
from unittest.mock import patch, MagicMock
from src.integrations.contentful_integration import ContentfulIntegration


def test_contentful_init_unconfigured():
    integration = ContentfulIntegration()
    assert not integration.is_configured()


def test_contentful_init_configured():
    integration = ContentfulIntegration(space_id="space123", management_token="token123")
    assert integration.is_configured()


def test_contentful_test_connection_simulated():
    integration = ContentfulIntegration()
    res = integration.test_connection()
    assert res["status"] == "connected"
    assert res["mode"] == "simulated"


@patch("requests.get")
def test_contentful_test_connection_live_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"name": "Test Space"}
    mock_get.return_value = mock_resp

    integration = ContentfulIntegration(space_id="space123", management_token="token123")
    res = integration.test_connection()
    assert res["status"] == "connected"
    assert res["mode"] == "live"


def test_contentful_create_entry_simulated():
    integration = ContentfulIntegration()
    fields = {"title": "Test Entry", "body": "Entry content"}
    res = integration.create_entry(content_type_id="blogPost", fields=fields, locale="en-US")
    assert res["status"] == "draft"
    assert res["content_type_id"] == "blogPost"
    assert res["fields"]["title"]["en-US"] == "Test Entry"


def test_contentful_publish_entry_simulated():
    integration = ContentfulIntegration()
    res = integration.publish_entry(entry_id="contentful-entry-123", version=1)
    assert res["status"] == "published"
    assert res["version"] == 2


def test_contentful_publish_content_helper():
    integration = ContentfulIntegration()
    fields = {"title": "Auto Publish Entry", "body": "Body content"}
    res = integration.publish_content(content_type_id="blogPost", payload=fields, auto_publish=True)
    assert res["status"] == "published"
    assert "contentful-entry-" in res["id"]
