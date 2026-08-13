"""
Unit tests for MarTechPartnershipScoutAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.martech_partnership_agent import (
    MarTechPartnershipScoutAgent,
    ScoutAgentInputs,
    PartnershipCriteria,
    PartnershipLead,
    PartnershipProposal,
    ScoutAgentOutputs
)


@pytest.fixture
def sample_inputs():
    """Create sample input data for testing the scout agent."""
    return ScoutAgentInputs(
        value_proposition="PersonaScript helps growth-stage B2B SaaS teams scale personalized content.",
        criteria=PartnershipCriteria(
            target_audiences=["B2B SaaS Marketing Teams", "Demand Generation"],
            tech_stacks=["HubSpot", "Zapier"],
            min_market_reach="growth stage"
        )
    )


def test_agent_initialization():
    """Test that scout agent initializes correctly."""
    agent = MarTechPartnershipScoutAgent()
    assert agent is not None
    assert agent.linkedin_integration is not None
    assert agent.partnerstack_integration is not None
    assert agent.notion_integration is not None
    assert agent.github_integration is not None


def test_agent_with_credentials():
    """Test agent initialization with credentials."""
    agent = MarTechPartnershipScoutAgent(
        linkedin_credentials={"session_id": "test_id"},
        partnerstack_api_key="ps_key",
        notion_api_key="notion_key",
        notion_database_id="db_id",
        github_token="git_token",
        github_repo="owner/repo"
    )
    assert agent.linkedin_integration.credentials == {"session_id": "test_id"}
    assert agent.partnerstack_integration.api_key == "ps_key"
    assert agent.notion_integration.api_key == "notion_key"
    assert agent.notion_integration.database_id == "db_id"
    assert agent.github_integration.token == "git_token"
    assert agent.github_integration.repo == "owner/repo"


def test_ingest_parameters(sample_inputs):
    """Test ingestion of value proposition and partnership criteria."""
    agent = MarTechPartnershipScoutAgent()
    analysis = agent._ingest_parameters(sample_inputs.value_proposition, sample_inputs.criteria)

    assert "value_prop_summary" in analysis
    assert "keywords" in analysis
    assert "hubspot" in [k.lower() for k in analysis["keywords"]]


def test_calculate_compatibility(sample_inputs):
    """Test strategic compatibility scoring algorithm."""
    agent = MarTechPartnershipScoutAgent()
    ent = {
        "name": "SuperCRM",
        "type": "Marketing Technology Provider",
        "description": "An awesome CRM with native HubSpot integration designed for B2B SaaS marketing teams.",
        "tech_stack": ["HubSpot"],
        "target_audience": "B2B SaaS Marketing Teams"
    }

    score, rationale = agent._calculate_compatibility(ent, sample_inputs.criteria, sample_inputs.value_proposition)
    assert score > 0.5
    assert "hubspot" in rationale.lower()
    assert "SuperCRM" in rationale


def test_prioritize_leads(sample_inputs):
    """Test that leads are sorted and prioritized correctly."""
    agent = MarTechPartnershipScoutAgent()
    leads = [
        PartnershipLead(
            name="Lead A", type="Tech Provider", source="L", description="", target_audience="", tech_stack=[], market_reach="", source_url="", compatibility_score=0.4
        ),
        PartnershipLead(
            name="Lead B", type="Tech Provider", source="L", description="", target_audience="", tech_stack=[], market_reach="", source_url="", compatibility_score=0.9
        ),
        PartnershipLead(
            name="Lead C", type="Tech Provider", source="L", description="", target_audience="", tech_stack=[], market_reach="", source_url="", compatibility_score=0.7
        )
    ]

    prioritized = agent._prioritize_leads(leads)
    assert prioritized[0].name == "Lead B"
    assert prioritized[0].is_high_priority is True
    assert prioritized[1].name == "Lead C"
    assert prioritized[1].is_high_priority is True
    assert prioritized[2].name == "Lead A"
    assert prioritized[2].is_high_priority is False


def test_full_scouting_execution(sample_inputs):
    """Test full integration/scouting execution flow."""
    agent = MarTechPartnershipScoutAgent()
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, ScoutAgentOutputs)
    assert len(outputs.leads) > 0
    assert len(outputs.proposals) > 0

    # Verify high-priority leads mapped to proposals
    high_priority_names = [l.name for l in outputs.leads if l.is_high_priority]
    proposal_names = [p.lead_name for p in outputs.proposals]
    assert len(high_priority_names) == len(proposal_names)

    # Verify output URLs are schema-correct
    for prop in outputs.proposals:
        parsed = urlparse(prop.notion_url)
        assert parsed.scheme == "https"
        assert parsed.netloc == "notion.so"

    parsed_report = urlparse(outputs.comprehensive_report_url)
    assert parsed_report.scheme == "https"
    assert parsed_report.netloc == "notion.so"

    parsed_git = urlparse(outputs.github_issue_url)
    assert parsed_git.scheme == "https"
    assert parsed_git.netloc == "github.com"
