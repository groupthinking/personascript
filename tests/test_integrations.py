"""Tests for integration modules."""

import pytest
from urllib.parse import urlparse
from src.integrations.miro_integration import MiroIntegration
from src.integrations.google_docs_integration import GoogleDocsIntegration
from src.integrations.github_integration import GitHubIntegration


class TestMiroIntegration:
    """Tests for MiroIntegration."""
    
    def test_initialization(self):
        """Test Miro integration initialization."""
        integration = MiroIntegration()
        assert integration is not None
        assert integration.api_key is None
        
        integration_with_key = MiroIntegration(api_key="test_key")
        assert integration_with_key.api_key == "test_key"
    
    def test_create_board(self):
        """Test board creation."""
        integration = MiroIntegration()
        board_data = {
            "title": "Test Board",
            "personas": []
        }
        
        url = integration.create_board(board_data)
        assert url
        # Use proper URL parsing for validation
        parsed = urlparse(url)
        assert parsed.scheme == "https"
        # Validate that netloc ends with expected domain
        assert parsed.netloc.endswith("miro.com")
    
    def test_add_persona_card(self):
        """Test adding persona card."""
        integration = MiroIntegration()
        card_id = integration.add_persona_card(
            board_id="test_board",
            persona_data={"name": "Test"},
            position={"x": 0, "y": 0}
        )
        assert card_id


class TestGoogleDocsIntegration:
    """Tests for GoogleDocsIntegration."""
    
    def test_initialization(self):
        """Test Google Docs integration initialization."""
        integration = GoogleDocsIntegration()
        assert integration is not None
        assert integration.credentials is None
        
        integration_with_creds = GoogleDocsIntegration(credentials={"type": "test"})
        assert integration_with_creds.credentials is not None
    
    def test_create_document(self):
        """Test document creation."""
        integration = GoogleDocsIntegration()
        url = integration.create_document(
            title="Test Document",
            content="Test content"
        )
        assert url
        # Use proper URL parsing for validation
        parsed = urlparse(url)
        assert parsed.scheme == "https"
        # Validate that netloc ends with expected domain
        assert parsed.netloc.endswith("docs.google.com")
    
    def test_append_content(self):
        """Test content appending."""
        integration = GoogleDocsIntegration()
        result = integration.append_content(
            doc_id="test_doc",
            content="More content"
        )
        assert result is True


class TestGitHubIntegration:
    """Tests for GitHubIntegration."""
    
    def test_initialization(self):
        """Test GitHub integration initialization."""
        integration = GitHubIntegration()
        assert integration is not None
        assert integration.token is None
        assert integration.repo is None
        
        integration_with_creds = GitHubIntegration(
            token="test_token",
            repo="owner/repo"
        )
        assert integration_with_creds.token == "test_token"
        assert integration_with_creds.repo == "owner/repo"
    
    def test_create_issue(self):
        """Test issue creation."""
        integration = GitHubIntegration(repo="test/repo")
        url = integration.create_issue(
            title="Test Issue",
            body="Test body",
            labels=["test"]
        )
        assert url
        # Use proper URL parsing for validation
        parsed = urlparse(url)
        assert parsed.scheme == "https"
        # Validate that netloc ends with expected domain
        assert parsed.netloc.endswith("github.com")
        # Check path contains "issues"
        assert parsed.path.startswith("/") and "issues" in parsed.path.split("/")
    
    def test_add_comment(self):
        """Test adding comment."""
        integration = GitHubIntegration()
        result = integration.add_comment(
            issue_number=1,
            comment="Test comment"
        )
        assert result is True


class TestHubSpotIntegration:
    """Tests for HubSpotIntegration."""

    def test_initialization(self):
        """Test HubSpot integration initialization."""
        from src.integrations.hubspot_integration import HubSpotIntegration
        integration = HubSpotIntegration()
        assert integration is not None
        assert integration.api_key is None
        assert integration.access_token is None

        integration_with_token = HubSpotIntegration(access_token="test_token")
        assert integration_with_token.access_token == "test_token"
        assert integration_with_token.is_authenticated() is True

    def test_publish_blog_post_mock(self):
        """Test publishing blog post in mock mode."""
        from src.integrations.hubspot_integration import HubSpotIntegration
        integration = HubSpotIntegration()
        blog_data = {
            "name": "Test Blog",
            "postBody": "Hello World",
            "slug": "test-blog-slug"
        }
        res = integration.publish_blog_post(blog_data)
        assert res["status"] == "success"
        assert res["id"].startswith("mock-hubspot-blog-")
        assert "test-blog-slug" in res["url"]

    def test_send_marketing_email_mock(self):
        """Test sending marketing email in mock mode."""
        from src.integrations.hubspot_integration import HubSpotIntegration
        integration = HubSpotIntegration()
        email_data = {
            "name": "Test Email",
            "subject": "Greetings",
            "htmlBody": "<p>Hello</p>"
        }
        res = integration.send_marketing_email(email_data)
        assert res["status"] == "success"
        assert res["id"].startswith("mock-hubspot-email-")

    def test_create_or_update_object_mock(self):
        """Test CRM object creation/update in mock mode."""
        from src.integrations.hubspot_integration import HubSpotIntegration
        integration = HubSpotIntegration()
        properties = {"firstname": "Sarah", "lastname": "Connor"}
        res = integration.create_or_update_object("contacts", properties)
        assert res["status"] == "success"
        assert res["id"].startswith("mock-crm-")
        assert res["data"]["properties"]["firstname"] == "Sarah"


class TestContentfulIntegration:
    """Tests for ContentfulIntegration."""

    def test_initialization(self):
        """Test Contentful integration initialization."""
        from src.integrations.contentful_integration import ContentfulIntegration
        integration = ContentfulIntegration()
        assert integration is not None
        assert integration.space_id is None
        assert integration.access_token is None
        assert integration.environment_id == "master"

        integration_with_creds = ContentfulIntegration(space_id="sp", access_token="tk", environment_id="staging")
        assert integration_with_creds.space_id == "sp"
        assert integration_with_creds.access_token == "tk"
        assert integration_with_creds.environment_id == "staging"
        assert integration_with_creds.is_authenticated() is True

    def test_localize_fields(self):
        """Test fields localization logic."""
        from src.integrations.contentful_integration import ContentfulIntegration
        integration = ContentfulIntegration()
        fields = {
            "title": "Hello",
            "body": "World",
            "already_localized": {"en-US": "Value"}
        }
        localized = integration.localize_fields(fields, locale="en-US")
        assert localized["title"] == {"en-US": "Hello"}
        assert localized["body"] == {"en-US": "World"}
        assert localized["already_localized"] == {"en-US": "Value"}

    def test_create_entry_mock(self):
        """Test entry creation in mock mode."""
        from src.integrations.contentful_integration import ContentfulIntegration
        integration = ContentfulIntegration()
        fields = {"title": "Test Title", "body": "Test Body"}
        res = integration.create_entry("blogPost", fields)
        assert res["status"] == "success"
        assert res["id"].startswith("mock-contentful-entry-")
        assert res["version"] == 1
        assert res["data"]["fields"]["title"] == {"en-US": "Test Title"}

    def test_publish_entry_mock(self):
        """Test entry publishing in mock mode."""
        from src.integrations.contentful_integration import ContentfulIntegration
        integration = ContentfulIntegration()
        res = integration.publish_entry("entry_id", version=3)
        assert res["status"] == "success"
        assert res["id"] == "entry_id"
        assert res["version"] == 4
        assert res["published"] is True
