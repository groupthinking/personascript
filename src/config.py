"""
Configuration file for PersonaScript Agent.

This file contains example configuration for API credentials and settings.
For security, actual credentials should be stored in environment variables or a secure vault.
"""

import os
from typing import Dict, Any, Optional


def get_config() -> Dict[str, Any]:
    """
    Get configuration from environment variables.
    
    Returns:
        Dictionary containing configuration values
    """
    return {
        "miro": {
            "api_key": os.environ.get("MIRO_API_KEY"),
        },
        "google": {
            "credentials_path": os.environ.get("GOOGLE_CREDENTIALS_PATH"),
        },
        "github": {
            "token": os.environ.get("GITHUB_TOKEN"),
            "repo": os.environ.get("GITHUB_REPO", "groupthinking/personascript"),
        },
    }


def load_google_credentials() -> Optional[Dict[str, Any]]:
    """
    Load Google API credentials from file.
    
    Returns:
        Credentials dictionary or None if not available
    """
    config = get_config()
    credentials_path = config["google"].get("credentials_path")
    
    if not credentials_path or not os.path.exists(credentials_path):
        return None
    
    import json
    with open(credentials_path, 'r') as f:
        return json.load(f)


# Example configuration template
CONFIG_TEMPLATE = """
# Environment Variables Configuration

# Miro API
export MIRO_API_KEY="your_miro_api_key_here"

# Google Docs API
export GOOGLE_CREDENTIALS_PATH="/path/to/google-credentials.json"

# GitHub API
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_REPO="owner/repository"
"""
