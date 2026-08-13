"""
Unit tests for the Sales growth strategist integration modules (Salesforce, Gong.io, ZoomInfo).
"""

import pytest
from src.integrations.salesforce_integration import SalesforceIntegration
from src.integrations.gong_integration import GongIntegration
from src.integrations.zoominfo_integration import ZoomInfoIntegration


class TestSalesforceIntegration:
    """Tests for SalesforceIntegration."""

    def test_initialization(self):
        """Test initialization and parameter passing."""
        integration = SalesforceIntegration()
        assert integration.username is None
        assert integration.password is None

        integration_with_creds = SalesforceIntegration(
            username="test_user",
            password="test_password",
            security_token="test_token",
            client_id="test_id",
            client_secret="test_secret",
        )
        assert integration_with_creds.username == "test_user"
        assert integration_with_creds.password == "test_password"
        assert integration_with_creds.security_token == "test_token"
        assert integration_with_creds.client_id == "test_id"
        assert integration_with_creds.client_secret == "test_secret"

    def test_get_sales_performance_metrics(self):
        """Test retrieving simulated sales performance metrics."""
        integration = SalesforceIntegration()
        metrics = integration.get_sales_performance_metrics()

        assert isinstance(metrics, dict)
        assert "current_mrr" in metrics
        assert "lead_to_opportunity_conversion_rate" in metrics
        assert "average_sales_cycle_length_days" in metrics
        assert metrics["current_mrr"] == 45000.0
        assert metrics["lead_to_opportunity_conversion_rate"] == 0.125


class TestGongIntegration:
    """Tests for GongIntegration."""

    def test_initialization(self):
        """Test initialization and API key setting."""
        integration = GongIntegration()
        assert integration.api_key is None

        integration_with_key = GongIntegration(api_key="test_gong_key")
        assert integration_with_key.api_key == "test_gong_key"

    def test_get_call_transcripts_and_analytics(self):
        """Test retrieving simulated call analytics and transcripts."""
        integration = GongIntegration()
        analytics = integration.get_call_transcripts_and_analytics()

        assert isinstance(analytics, dict)
        assert "conversational_metrics" in analytics
        assert "objection_analysis" in analytics
        assert "common_objections" in analytics
        assert "transcripts_summary" in analytics

        metrics = analytics["conversational_metrics"]
        assert "average_talk_to_listen_ratio" in metrics
        assert len(analytics["common_objections"]) > 0


class TestZoomInfoIntegration:
    """Tests for ZoomInfoIntegration."""

    def test_initialization(self):
        """Test initialization and API key setting."""
        integration = ZoomInfoIntegration()
        assert integration.api_key is None

        integration_with_key = ZoomInfoIntegration(api_key="test_zoominfo_key")
        assert integration_with_key.api_key == "test_zoominfo_key"

    def test_get_prospect_data_and_market_intelligence(self):
        """Test retrieving simulated prospect data and intelligence."""
        integration = ZoomInfoIntegration()
        intel = integration.get_prospect_data_and_market_intelligence()

        assert isinstance(intel, dict)
        assert "ideal_customer_profile_icp" in intel
        assert "target_contacts" in intel
        assert "top_target_accounts" in intel
        assert "market_trends" in intel

        icp = intel["ideal_customer_profile_icp"]
        assert "industries" in icp
        assert "B2B SaaS" in icp["industries"]
        assert len(intel["target_contacts"]) > 0
