"""Tests for HubSpot API Integration."""

import pytest
from unittest.mock import patch, MagicMock
from src.integrations.hubspot_integration import HubSpotIntegration


def test_hubspot_init_unconfigured():
    integration = HubSpotIntegration()
    assert not integration.is_configured()


def test_hubspot_init_configured():
    integration = HubSpotIntegration(api_key="test-key")
    assert integration.is_configured()


def test_hubspot_test_connection_simulated():
    integration = HubSpotIntegration()
    res = integration.test_connection()
    assert res["status"] == "connected"
    assert res["mode"] == "simulated"


@patch("requests.get")
def test_hubspot_test_connection_live_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    integration = HubSpotIntegration(api_key="test-key")
    res = integration.test_connection()
    assert res["status"] == "connected"
    assert res["mode"] == "live"


def test_hubspot_create_blog_post_simulated():
    integration = HubSpotIntegration()
    res = integration.create_blog_post({"title": "Test Blog", "body": "Body text"})
    assert res["status"] == "success"
    assert res["name"] == "Test Blog"
    assert "hubspot-blog-" in res["id"]


def test_hubspot_create_marketing_email_simulated():
    integration = HubSpotIntegration()
    res = integration.create_marketing_email({"name": "Test Email", "subject": "Test Subject", "body": "Email body"})
    assert res["status"] == "success"
    assert res["name"] == "Test Email"
    assert "hubspot-email-" in res["id"]


def test_hubspot_create_landing_page_simulated():
    integration = HubSpotIntegration()
    res = integration.create_landing_page({"name": "Test Page", "body": "Page content"})
    assert res["status"] == "success"
    assert res["name"] == "Test Page"
    assert "hubspot-page-" in res["id"]


def test_hubspot_publish_content_dispatch():
    integration = HubSpotIntegration()
    res_blog = integration.publish_content("blog_post", {"title": "Dispatch Blog"})
    assert "hubspot-blog-" in res_blog["id"]

    res_email = integration.publish_content("marketing_email", {"name": "Dispatch Email"})
    assert "hubspot-email-" in res_email["id"]

    res_page = integration.publish_content("landing_page", {"name": "Dispatch Page"})
    assert "hubspot-page-" in res_page["id"]
