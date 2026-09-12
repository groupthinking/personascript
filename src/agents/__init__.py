"""Agent modules for PersonaScript."""

from .persona_creator_agent import PersonaScriptPersonaCreatorAgent
from .prd_drafter_agent import PersonaScriptPRDDrafterAgent
from .ai_api_integration_agent import AIApiIntegrationAgent, AIAgentInputs, AIAgentOutputs
from .content_iteration_agent import (
    PersonaScriptContentIterationAgent,
    ContentAsset,
    AgentInputs as ContentIterationAgentInputs,
    AgentOutputs as ContentIterationAgentOutputs,
    WeeklyAnalyticsReport,
    ABTestResultsSummary,
    BacklogItem
)
from .martech_partnership_agent import (
    MarTechPartnershipScoutAgent,
    PartnershipCriteria,
    PartnershipLead,
    ProposalOutline,
    AgentInputs as PartnershipAgentInputs,
    AgentOutputs as PartnershipAgentOutputs
)

__all__ = [
    "PersonaScriptPersonaCreatorAgent",
    "PersonaScriptPRDDrafterAgent",
    "AIApiIntegrationAgent",
    "AIAgentInputs",
    "AIAgentOutputs",
    "PersonaScriptContentIterationAgent",
    "ContentAsset",
    "ContentIterationAgentInputs",
    "ContentIterationAgentOutputs",
    "WeeklyAnalyticsReport",
    "ABTestResultsSummary",
    "BacklogItem",
    "MarTechPartnershipScoutAgent",
    "PartnershipCriteria",
    "PartnershipLead",
    "ProposalOutline",
    "PartnershipAgentInputs",
    "PartnershipAgentOutputs"
]
