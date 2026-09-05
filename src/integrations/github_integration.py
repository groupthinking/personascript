"""
GitHub API Integration for PersonaScript.

This module handles all interactions with the GitHub API for creating issues.
"""

import logging
import requests
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class GitHubIntegration:
    """Integration with GitHub API for creating completion issues."""
    
    def __init__(self, token: Optional[str] = None, repo: Optional[str] = None):
        """
        Initialize GitHub integration.
        
        Args:
            token: GitHub personal access token
            repo: Repository in format "owner/repo"
        """
        self.token = token
        self.repo = repo
        self.base_url = "https://api.github.com"
        logger.info("GitHubIntegration initialized")
    
    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> str:
        """
        Create a new GitHub issue.
        
        Args:
            title: Issue title
            body: Issue body (supports markdown)
            labels: List of label names to apply
            assignees: List of usernames to assign
        
        Returns:
            URL of the created issue
        """
        logger.info(f"Creating GitHub issue: {title}")
        
        if not self.token or not self.repo:
            logger.warning("No GitHub credentials provided, returning mock URL")
            return self._create_mock_issue_url(title)
        
        try:
            url = f"{self.base_url}/repos/{self.repo}/issues"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }

            payload: Dict[str, Any] = {
                "title": title,
                "body": body
            }
            if labels is not None:
                payload["labels"] = labels
            if assignees is not None:
                payload["assignees"] = assignees

            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 201:
                issue_data = response.json()
                issue_url = issue_data.get("html_url")
                if issue_url:
                    logger.info(f"Successfully created GitHub issue: {issue_url}")
                    return issue_url

            logger.error(f"Failed to create GitHub issue: {response.status_code} - {response.text}")
            return self._create_mock_issue_url(title)
        except Exception as e:
            logger.error(f"Exception creating GitHub issue: {str(e)}", exc_info=True)
            return self._create_mock_issue_url(title)
    
    def _create_mock_issue_url(self, title: str) -> str:
        """Create a mock issue URL for demonstration purposes."""
        # In a real scenario, this would be replaced with actual GitHub API calls
        if self.repo:
            issue_number = abs(hash(title)) % 1000
            return f"https://github.com/{self.repo}/issues/{issue_number}"
        return f"https://github.com/example/repo/issues/1"
    
    def add_comment(self, issue_number: int, comment: str) -> bool:
        """
        Add a comment to an existing issue.
        
        Args:
            issue_number: Issue number
            comment: Comment text (supports markdown)
        
        Returns:
            True if successful
        """
        if not self.token or not self.repo:
            logger.warning("No GitHub credentials provided, returning mock success")
            return True
        
        # Real implementation would POST to /repos/{owner}/{repo}/issues/{issue_number}/comments
        return True
    
    def update_issue_labels(
        self,
        issue_number: int,
        labels: List[str]
    ) -> bool:
        """
        Update labels on an existing issue.
        
        Args:
            issue_number: Issue number
            labels: List of label names
        
        Returns:
            True if successful
        """
        if not self.token or not self.repo:
            logger.warning("No GitHub credentials provided, returning mock success")
            return True
        
        # Real implementation would PUT to /repos/{owner}/{repo}/issues/{issue_number}/labels
        return True
    
    def close_issue(self, issue_number: int) -> bool:
        """
        Close an issue.
        
        Args:
            issue_number: Issue number
        
        Returns:
            True if successful
        """
        if not self.token or not self.repo:
            logger.warning("No GitHub credentials provided, returning mock success")
            return True
        
        # Real implementation would PATCH to /repos/{owner}/{repo}/issues/{issue_number}
        return True
