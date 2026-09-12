"""
Unit tests for MarTechPartnershipScoutAgent and its integrations.
"""

import pytest
from urllib.parse import urlparse
from src.integrations.linkedin_integration import LinkedInIntegration
from src.integrations.partnerstack_integration import PartnerStackIntegration
from src.agents.martech_partnership_agent import (
    MarTechPartnershipScoutAgent,
    PartnershipCriteria,
    PartnershipLead,
    ProposalOutline,
    AgentInputs,
    AgentOutputs
)


@pytest.fixture
def sample_inputs():
    """Create sample inputs for MarTechPartnershipScoutAgent."""
    return AgentInputs(
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
            "high-volume, hyper-personalized, and brand-aligned content across all sales funnel "
            "stages, dramatically accelerating lead conversion and brand consistency."
        ),
        partnership_criteria=PartnershipCriteria(
            target_audience=[
                "Growth-stage B2B SaaS marketing teams",
                "Demand generation leaders",
                "Content marketing managers"
            ],
            tech_stack=["HubSpot", "Contentful", "ActiveCampaign", "Copy.ai", "REST APIs"],
            market_reach="Mid-market & Growth SaaS",
            min_alignment_score=0.7
        )
    )


@pytest.fixture
def agent():
    """Create agent instance with default mock configuration."""
    return MarTechPartnershipScoutAgent()


def test_linkedin_integration_mock():
    """Test LinkedInIntegration mock entity search."""
    linkedin = LinkedInIntegration()
    results = linkedin.search_entities(query="marketing automation", entity_type="company")
    assert len(results) > 0
    assert all(r["type"] == "Company" for r in results)

    assoc_results = linkedin.search_entities(query="AI Institute", entity_type="association")
    assert len(assoc_results) > 0
    assert all(r["type"] == "Industry Association" for r in assoc_results)


def test_partnerstack_integration_mock():
    """Test PartnerStackIntegration mock program search."""
    partnerstack = PartnerStackIntegration()
    programs = partnerstack.search_programs(category="AI Writing & Marketing Automation")
    assert len(programs) > 0
    assert any("Copy.ai" in p["company_name"] for p in programs)


def test_agent_initialization():
    """Test agent initialization and integration setup."""
    agent = MarTechPartnershipScoutAgent(
        linkedin_access_token="test_linkedin_token",
        partnerstack_api_key="test_partnerstack_key",
        notion_token="test_notion_token",
        github_token="test_github_token",
        github_repo="owner/repo"
    )
    assert agent.linkedin.access_token == "test_linkedin_token"
    assert agent.partnerstack.api_key == "test_partnerstack_key"
    assert agent.notion.token == "test_notion_token"
    assert agent.github.token == "test_github_token"
    assert agent.github.repo == "owner/repo"


def test_ingest_and_parse_inputs(agent, sample_inputs):
    """Test Step 1: Input ingestion and search parameter generation."""
    params = agent._ingest_and_parse_inputs(sample_inputs)
    assert "keywords" in params
    assert "target_audiences" in params
    assert "HubSpot" in sample_inputs.partnership_criteria.tech_stack


def test_preliminary_analysis_and_prioritization(agent, sample_inputs):
    """Test Step 4 & 5: Preliminary analysis and prioritization logic."""
    entities = agent.linkedin.search_entities(query="test", entity_type="all")
    programs = agent.partnerstack.search_programs(category="test")

    analyzed = agent._perform_preliminary_analysis(entities, programs, sample_inputs)
    assert len(analyzed) == len(entities) + len(programs)

    prioritized = agent._filter_and_prioritize_leads(analyzed, sample_inputs.partnership_criteria)
    assert len(prioritized) > 0
    assert all(isinstance(l, PartnershipLead) for l in prioritized)
    assert any(l.priority == "High" for l in prioritized)


def test_draft_proposals_in_notion(agent, sample_inputs):
    """Test Step 6: Proposal outline drafting in Notion."""
    entities = agent.linkedin.search_entities(query="test", entity_type="all")
    programs = agent.partnerstack.search_programs(category="test")
    analyzed = agent._perform_preliminary_analysis(entities, programs, sample_inputs)
    prioritized = agent._filter_and_prioritize_leads(analyzed, sample_inputs.partnership_criteria)

    proposals = agent._draft_proposals_in_notion(prioritized, sample_inputs)
    assert len(proposals) > 0
    assert all(isinstance(p, ProposalOutline) for p in proposals)
    assert all(p.notion_url and "notion.so" in p.notion_url for p in proposals)


def test_full_execution(agent, sample_inputs):
    """Test complete 8-step execution of MarTechPartnershipScoutAgent."""
    outputs = agent.execute(sample_inputs)

    assert isinstance(outputs, AgentOutputs)
    assert len(outputs.qualified_leads) > 0
    assert len(outputs.proposal_outlines) > 0
    assert outputs.comprehensive_report_notion_url
    assert outputs.github_issue_url
    assert len(outputs.execution_summary) == 8

    # Verify Notion URL format
    notion_parsed = urlparse(outputs.comprehensive_report_notion_url)
    assert notion_parsed.scheme == "https"
    assert notion_parsed.netloc == "notion.so"

    # Verify GitHub URL format
    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc == "github.com"
