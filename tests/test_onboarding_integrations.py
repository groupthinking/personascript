"""
Unit tests for customer onboarding and support system integrations.
"""

import pytest
from urllib.parse import urlparse
from src.integrations.intercom_integration import IntercomIntegration
from src.integrations.zendesk_integration import ZendeskIntegration
from src.integrations.loom_integration import LoomIntegration


class TestIntercomIntegration:
    """Tests for IntercomIntegration."""

    def test_initialization(self):
        """Test Intercom integration initialization."""
        integration = IntercomIntegration()
        assert integration is not None
        assert integration.api_key is None

        integration_with_key = IntercomIntegration(api_key="test_key")
        assert integration_with_key.api_key == "test_key"

    def test_configure_onboarding_sequences(self):
        """Test sequence configuration."""
        integration = IntercomIntegration()
        seq_spec = [{
            "title": "Welcome Flow",
            "audience": "new_leads",
            "steps": [{"title": "Welcome Email"}]
        }]

        res = integration.configure_onboarding_sequences(seq_spec)
        assert res["status"] == "success"
        assert len(res["sequences"]) == 1
        assert res["sequences"][0]["title"] == "Welcome Flow"
        assert "dashboard_url" in res

    def test_integrate_chat_support(self):
        """Test chat support setup."""
        integration = IntercomIntegration()
        config = {"routing_rule": "assign_to_tier_1"}

        res = integration.integrate_chat_support(config)
        assert res["status"] == "success"
        assert res["widget_installed"] is True
        assert "inbox_id" in res

    def test_embed_loom_tutorials(self):
        """Test embedding Loom tutorials in Intercom."""
        integration = IntercomIntegration()
        res = integration.embed_loom_tutorials("msg-123", [{"video_url": "https://loom.com/123", "embed_code": "<iframe></iframe>"}])
        assert res["status"] == "success"
        assert res["embedded_videos_count"] == 1

    def test_configure_zendesk_integration(self):
        """Test linking to Zendesk."""
        integration = IntercomIntegration()
        res = integration.configure_zendesk_integration("personascript")
        assert res["status"] == "success"
        assert res["integration_linked"] is True


class TestZendeskIntegration:
    """Tests for ZendeskIntegration."""

    def test_initialization(self):
        """Test Zendesk integration initialization."""
        integration = ZendeskIntegration()
        assert integration is not None
        assert integration.subdomain == "personascript"

        integration_with_token = ZendeskIntegration(subdomain="custom", api_token="tok")
        assert integration_with_token.subdomain == "custom"
        assert integration_with_token.api_token == "tok"

    def test_populate_knowledge_base(self):
        """Test KB population."""
        integration = ZendeskIntegration()
        kb_content = {
            "categories": [{
                "name": "General",
                "sections": [{
                    "name": "FAQ",
                    "articles": [{"title": "How to create persona", "requires_video": True}]
                }]
            }]
        }

        res = integration.populate_knowledge_base(kb_content)
        assert res["status"] == "success"
        assert "kb_url" in res
        assert len(res["categories"]) == 1
        assert res["categories"][0]["name"] == "General"

    def test_embed_loom_tutorial_in_article(self):
        """Test embedding Loom video in help article."""
        integration = ZendeskIntegration()
        res = integration.embed_loom_tutorial_in_article("art-111", {"video_url": "https://loom.com/123", "embed_code": "<iframe></iframe>"})
        assert res["status"] == "success"
        assert res["loom_embedded"] is True


class TestLoomIntegration:
    """Tests for LoomIntegration."""

    def test_initialization(self):
        """Test Loom integration initialization."""
        integration = LoomIntegration()
        assert integration is not None

        integration_with_key = LoomIntegration(api_key="loom_key")
        assert integration_with_key.api_key == "loom_key"

    def test_generate_video_tutorial(self):
        """Test generating tutorial video."""
        integration = LoomIntegration()
        outline = {"title": "Brand Guidelines Setup", "description": "Quick setup video"}

        res = integration.generate_video_tutorial(outline)
        assert res["status"] == "success"
        assert res["title"] == "Brand Guidelines Setup"
        assert "embed_code" in res
        assert "video_url" in res

    def test_generate_multiple_tutorials(self):
        """Test generating multiple videos."""
        integration = LoomIntegration()
        outlines = [
            {"title": "Video 1"},
            {"title": "Video 2"}
        ]

        res = integration.generate_multiple_tutorials(outlines)
        assert len(res) == 2
        assert res[0]["title"] == "Video 1"
        assert res[1]["title"] == "Video 2"
