"""
Unit tests for the new integration modules.
"""

import pytest
from urllib.parse import urlparse
from src.integrations.linkedin_integration import LinkedInIntegration
from src.integrations.partnerstack_integration import PartnerStackIntegration
from src.integrations.notion_integration import NotionPartnershipIntegration


def test_linkedin_integration_simulated():
    """Test LinkedIn Integration with/without credentials."""
    integration = LinkedInIntegration()
    results = integration.search_companies_and_associations(keywords=["HubSpot"])
    assert len(results) > 0
    assert any(r["name"] == "HubSpot" for r in results)


def test_partnerstack_integration_simulated():
    """Test PartnerStack Integration simulated search."""
    integration = PartnerStackIntegration()
    results = integration.search_marketplace(keywords=["Copy.ai"])
    assert len(results) > 0
    assert any(r["name"] == "Copy.ai" for r in results)


def test_notion_partnership_integration_simulated():
    """Test Notion Partnership Integration page creation."""
    integration = NotionPartnershipIntegration()
    proposal_url = integration.create_proposal_page("HubSpot", "Test proposal")
    assert proposal_url
    parsed = urlparse(proposal_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "notion.so"

    report_url = integration.create_comprehensive_report_page("Scout Report", "Test report")
    assert report_url
    parsed_report = urlparse(report_url)
    assert parsed_report.scheme == "https"
    assert parsed_report.netloc == "notion.so"
