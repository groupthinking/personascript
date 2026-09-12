"""Agent modules for PersonaScript."""

from .persona_creator_agent import PersonaScriptPersonaCreatorAgent
from .prd_drafter_agent import PersonaScriptPRDDrafterAgent
from .ai_api_integration_agent import AIApiIntegrationAgent, AIAgentInputs, AIAgentOutputs
from .content_iteration_agent import (
    PersonaScriptContentIterationAgent,
    ContentAsset,
    AgentInputs,
    AgentOutputs,
    WeeklyAnalyticsReport,
    ABTestResultsSummary,
    BacklogItem
)
from .targeted_outreach_agent import (
    TargetedOutreachAgent,
    ICPDetails,
    CampaignConfig,
    AdCreative,
    Lead,
    PersonalizedMessage,
    AdPerformanceMetrics,
    AgentInputs as TargetedOutreachInputs,
    AgentOutputs as TargetedOutreachOutputs
)

__all__ = [
    "PersonaScriptPersonaCreatorAgent",
    "PersonaScriptPRDDrafterAgent",
    "AIApiIntegrationAgent",
    "AIAgentInputs",
    "AIAgentOutputs",
    "PersonaScriptContentIterationAgent",
    "ContentAsset",
    "AgentInputs",
    "AgentOutputs",
    "WeeklyAnalyticsReport",
    "ABTestResultsSummary",
    "BacklogItem",
    "TargetedOutreachAgent",
    "ICPDetails",
    "CampaignConfig",
    "AdCreative",
    "Lead",
    "PersonalizedMessage",
    "AdPerformanceMetrics",
    "TargetedOutreachInputs",
    "TargetedOutreachOutputs"
]
