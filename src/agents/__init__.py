"""Agent modules for PersonaScript."""

from .persona_creator_agent import PersonaScriptPersonaCreatorAgent
from .prd_drafter_agent import PersonaScriptPRDDrafterAgent
from .ai_api_integration_agent import AIApiIntegrationAgent, AIAgentInputs, AIAgentOutputs
from .content_iteration_agent import (
    PersonaScriptContentIterationAgent,
    ContentAsset,
    AgentInputs as IterationAgentInputs,
    AgentOutputs as IterationAgentOutputs,
    WeeklyAnalyticsReport,
    ABTestResultsSummary,
    BacklogItem
)
from .persona_script_integration_agent import (
    PersonaScriptIntegrationAgent,
    PersonaScriptContent,
    HubSpotObjectDefinition,
    ContentfulContentModel,
    IntegrationTestResult,
    AgentInputs as IntegrationAgentInputs,
    AgentOutputs as IntegrationAgentOutputs
)

__all__ = [
    "PersonaScriptPersonaCreatorAgent",
    "PersonaScriptPRDDrafterAgent",
    "AIApiIntegrationAgent",
    "AIAgentInputs",
    "AIAgentOutputs",
    "PersonaScriptContentIterationAgent",
    "ContentAsset",
    "IterationAgentInputs",
    "IterationAgentOutputs",
    "WeeklyAnalyticsReport",
    "ABTestResultsSummary",
    "BacklogItem",
    "PersonaScriptIntegrationAgent",
    "PersonaScriptContent",
    "HubSpotObjectDefinition",
    "ContentfulContentModel",
    "IntegrationTestResult",
    "IntegrationAgentInputs",
    "IntegrationAgentOutputs"
]
