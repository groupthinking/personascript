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
