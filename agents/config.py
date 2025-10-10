"""
Configuration management for UserInterviewAnalysisAgent
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AgentConfig(BaseModel):
    """Configuration for the UserInterviewAnalysisAgent"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    
    # Zoom Configuration
    zoom_client_id: str = Field(default_factory=lambda: os.getenv("ZOOM_CLIENT_ID", ""))
    zoom_client_secret: str = Field(default_factory=lambda: os.getenv("ZOOM_CLIENT_SECRET", ""))
    zoom_account_id: str = Field(default_factory=lambda: os.getenv("ZOOM_ACCOUNT_ID", ""))
    
    # UserTesting Configuration
    usertesting_api_key: str = Field(default_factory=lambda: os.getenv("USERTESTING_API_KEY", ""))
    
    # Notion Configuration
    notion_api_key: str = Field(default_factory=lambda: os.getenv("NOTION_API_KEY", ""))
    notion_database_id: str = Field(default_factory=lambda: os.getenv("NOTION_DATABASE_ID", ""))
    
    # GitHub Configuration
    github_token: str = Field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    github_repo: str = Field(default_factory=lambda: os.getenv("GITHUB_REPO", "groupthinking/personascript"))
    
    # Agent Configuration
    value_proposition: str = Field(
        default="PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages, dramatically accelerating lead conversion and brand consistency."
    )
    target_interview_count: int = Field(default=20)
    interview_duration_minutes: int = Field(default=30)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config() -> AgentConfig:
    """Get the agent configuration"""
    return AgentConfig()
