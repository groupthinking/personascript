"""Tests for PersonaScriptMarketingLaunchAgent."""

import pytest
from unittest.mock import patch, MagicMock

from src.agents.marketing_launch_agent import (
    PersonaScriptMarketingLaunchAgent,
    MarketingAgentInputs,
    MarketingAgentOutputs,
    CustomerTestimonialData,
    BlogPostDraft,
    CaseStudyDraft
)


@pytest.fixture
def sample_marketing_inputs():
    return MarketingAgentInputs(
        value_proposition="PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-converting, brand-aligned marketing collateral.",
        target_audience_demographics={
            "target_roles": ["VP of Marketing", "Demand Gen Director", "Content Marketing Manager"],
            "company_size": "50-500 employees",
            "industry": "B2B SaaS"
        },
        brand_guidelines={
            "tone": "Professional, Authoritative, Data-driven",
            "primary_color": "#4F46E5",
            "banned_words": ["synergy", "paradigm shift"]
        },
        key_seo_keywords=[
            "B2B AI content generation",
            "SaaS marketing automation",
            "brand compliant copy generator",
            "demand generation platform"
        ],
        customer_data=[
            CustomerTestimonialData(
                customer_name="Jane Doe",
                company_name="Acme SaaS",
                industry="Fintech",
                key_metrics={"conversion_boost": "250%", "time_saved": "15 hrs/week"},
                quote_summary="PersonaScript transformed our content creation velocity while maintaining brand alignment."
            )
        ]
    )


def test_agent_initialization():
    agent = PersonaScriptMarketingLaunchAgent(
        github_token="fake_token",
        github_repo="owner/repo"
    )
    assert agent.github is not None
    assert agent.execution_log == []


def test_full_execution(sample_marketing_inputs):
    agent = PersonaScriptMarketingLaunchAgent()
    outputs = agent.execute(sample_marketing_inputs)

    assert outputs.status == "success"
    assert outputs.marketing_site_url.startswith("https://")
    assert len(outputs.blog_post_urls) == 3
    assert len(outputs.case_study_urls) >= 1
    assert outputs.github_issue_url.startswith("https://")
    assert len(outputs.blog_posts) == 3
    assert len(outputs.case_studies) >= 1

    # Check execution log steps
    assert len(agent.execution_log) >= 9


def test_execution_with_empty_customer_data():
    inputs = MarketingAgentInputs(
        value_proposition="Test value prop for SaaS marketing.",
        target_audience_demographics={"target_roles": ["CMO"]},
        brand_guidelines={"tone": "Bold"},
        key_seo_keywords=["AI content"],
        customer_data=[]
    )
    agent = PersonaScriptMarketingLaunchAgent()
    outputs = agent.execute(inputs)

    assert outputs.status == "success"
    assert len(outputs.case_studies) == 1
    assert outputs.case_studies[0].company_name == "CloudScale SaaS"


def test_execution_error_handling(sample_marketing_inputs):
    agent = PersonaScriptMarketingLaunchAgent()
    with patch.object(agent.github, 'create_issue', side_effect=RuntimeError("GitHub API down")):
        outputs = agent.execute(sample_marketing_inputs)

    assert outputs.status == "error"
    assert "GitHub API down" in outputs.error_message
