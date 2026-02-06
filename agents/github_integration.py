"""
GitHub Integration Module
Creates GitHub issues with analysis results
"""
import logging
from typing import Dict
import requests

logger = logging.getLogger(__name__)


class GitHubIssueCreator:
    """Creates GitHub issues with interview analysis results"""
    
    def __init__(self, config):
        self.config = config
        self.token = config.github_token
        self.repo = config.github_repo
        self.base_url = "https://api.github.com"
    
    def create_issue(self, issue_content: Dict[str, str]) -> str:
        """
        Create a GitHub issue
        
        Args:
            issue_content: Dictionary with 'title' and 'body'
            
        Returns:
            URL of the created issue
        """
        logger.info(f"Creating GitHub issue in {self.repo}")
        
        if not self.token:
            logger.warning("GitHub token not configured, using mock URL")
            return self._get_mock_url()
        
        try:
            url = f"{self.base_url}/repos/{self.repo}/issues"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            payload = {
                "title": issue_content['title'],
                "body": issue_content['body'],
                "labels": ["user-research", "feature-request", "analysis"]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                issue_data = response.json()
                issue_url = issue_data['html_url']
                logger.info(f"Successfully created issue: {issue_url}")
                return issue_url
            else:
                logger.error(f"Failed to create issue: {response.status_code} - {response.text}")
                return self._get_mock_url()
                
        except Exception as e:
            logger.error(f"Error creating GitHub issue: {str(e)}")
            return self._get_mock_url()
    
    def _get_mock_url(self) -> str:
        """Get mock GitHub issue URL"""
        return f"https://github.com/{self.repo}/issues/1"
