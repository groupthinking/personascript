"""
Unit tests for PersonaScriptMarketingLaunchAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.marketing_launch_agent import (
    PersonaScriptMarketingLaunchAgent,
    MarketingLaunchInputs,
    MarketingLaunchOutputs
)


@pytest.fixture
def sample_marketing_inputs():
    """Create sample input data for testing the marketing launch agent."""
    return MarketingLaunchInputs(
        value_proposition="Empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content.",
        target_audience={
            "roles": ["VP of Marketing", "Marketing Director", "CMO"],
            "company_size": "50-500 employees",
            "industries": ["B2B SaaS"]
        },
        brand_guidelines={
            "voice": "professional, modern, authoritative",
            "primary_color": "#4F46E5",
            "logo_url": "https://personascript.com/logo.png"
        },
        seo_keywords=["personalized B2B content", "AI marketing automation"],
        customer_data=[
            {
                "company": "Acme Corp",
                "metrics": "250% increase in content scaling",
                "quote": "PersonaScript made our content scaling seamless."
            },
            {
                "company": "SaaSify",
                "metrics": "40% increase in lead conversion",
                "quote": "Amazing tool for B2B marketers!"
            }
        ]
    )


@pytest.fixture
def default_agent():
    """Create a default agent instance for testing."""
    return PersonaScriptMarketingLaunchAgent()


def test_marketing_agent_initialization():
    """Test that the marketing launch agent initializes correctly."""
    agent = PersonaScriptMarketingLaunchAgent(
        webflow_api_key="wf_test",
        copy_ai_api_key="copyai_test",
        hubspot_api_key="hs_test",
        github_token="gh_test",
        github_repo="owner/repo"
    )
    assert agent is not None
    assert agent.webflow_integration.api_key == "wf_test"
    assert agent.copy_ai_integration.api_key == "copyai_test"
    assert agent.hubspot_integration.api_key == "hs_test"
    assert agent.github_integration.token == "gh_test"
    assert agent.github_integration.repo == "owner/repo"


def test_analyze_core_messaging(default_agent, sample_marketing_inputs):
    """Test internal step 1: NLP analysis of core messaging and brand guidelines."""
    analysis = default_agent._analyze_core_messaging(sample_marketing_inputs)
    assert "design_principles" in analysis
    assert "primary_messaging_hooks" in analysis
    assert "brand_voice" in analysis
    assert len(analysis["design_principles"]) > 0
    assert "professional" in analysis["brand_voice"]


def test_conduct_seo_research(default_agent, sample_marketing_inputs):
    """Test internal step 2: SEO keyword research."""
    keywords = default_agent._conduct_seo_research(sample_marketing_inputs)
    assert len(keywords) > len(sample_marketing_inputs.seo_keywords)
    assert "personalized B2B content" in keywords
    assert "AI content personalization" in keywords


def test_outline_website_structure(default_agent, sample_marketing_inputs):
    """Test internal step 3: Outlining website structure and page messaging."""
    seo_keywords = ["personalized B2B content", "AI marketing automation"]
    structure = default_agent._outline_website_structure(sample_marketing_inputs, seo_keywords)

    assert "homepage" in structure
    assert "features" in structure
    assert "pricing" in structure
    assert "blog" in structure
    assert "case_studies" in structure

    assert "title" in structure["homepage"]
    assert "core_messaging" in structure["homepage"]
    assert "sections" in structure["homepage"]
    assert "personalized B2B content" in structure["homepage"]["core_messaging"]


def test_generate_blog_drafts(default_agent, sample_marketing_inputs):
    """Test internal step 5: Generating blog post drafts using Copy.ai."""
    seo_keywords = ["personalized B2B content", "AI marketing automation"]
    drafts = default_agent._generate_blog_drafts(sample_marketing_inputs, seo_keywords)

    assert len(drafts) == 3
    for draft in drafts:
        assert "title" in draft
        assert "body" in draft
        assert "topic" in draft
        assert draft["status"] == "draft"
        assert "personalized B2B content" in draft["body"]


def test_optimize_blog_posts(default_agent):
    """Test internal step 6: Refining and optimizing blog drafts."""
    drafts = [
        {"title": "Test Blog Title", "body": "This is a raw draft body.", "status": "draft"}
    ]
    brand_guidelines = {"voice": "modern and bold"}
    optimized = default_agent._optimize_blog_posts(drafts, brand_guidelines)

    assert len(optimized) == 1
    assert optimized[0]["title"] == "Test Blog Title"
    assert "Refined for brand voice: 'modern and bold'" in optimized[0]["body"]
    assert optimized[0]["seo_optimized"] is True
    assert optimized[0]["readability_score"] >= 90


def test_generate_testimonial_drafts(default_agent, sample_marketing_inputs):
    """Test internal step 7: Testimonial drafting from customer data."""
    testimonials = default_agent._generate_testimonial_drafts(sample_marketing_inputs)

    assert len(testimonials) == 2
    assert testimonials[0]["company"] == "Acme Corp"
    assert testimonials[1]["company"] == "SaaSify"
    assert "250% increase" in testimonials[0]["body"]
    assert "40% increase" in testimonials[1]["body"]


def test_full_agent_execution(default_agent, sample_marketing_inputs):
    """Test full execute workflow of PersonaScriptMarketingLaunchAgent."""
    outputs = default_agent.execute(sample_marketing_inputs)

    assert isinstance(outputs, MarketingLaunchOutputs)

    # Verify outputs URL formats
    website_parsed = urlparse(outputs.website_url)
    assert website_parsed.scheme == "https"
    assert website_parsed.netloc.endswith("webflow.io")

    assert len(outputs.blog_post_urls) == 3
    for blog_url in outputs.blog_post_urls:
        blog_parsed = urlparse(blog_url)
        assert blog_parsed.scheme == "https"
        assert blog_parsed.netloc == "blog.personascript.com"
        assert blog_parsed.path.startswith("/posts/")

    assert len(outputs.testimonial_urls) == 2
    for testimonial_url in outputs.testimonial_urls:
        testimonial_parsed = urlparse(testimonial_url)
        assert testimonial_parsed.scheme == "https"
        assert testimonial_parsed.netloc == "personascript.com"
        assert testimonial_parsed.path.startswith("/case-studies/")

    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    assert github_parsed.netloc.endswith("github.com")
    assert "issues" in github_parsed.path

    # Check internal metadata and structures stored in output
    assert len(outputs.analyzed_data) > 0
    assert len(outputs.seo_keywords_research) >= len(sample_marketing_inputs.seo_keywords)
    assert len(outputs.website_structure) == 5
    assert len(outputs.blog_drafts) == 3
    assert len(outputs.optimized_blogs) == 3
    assert len(outputs.testimonial_drafts) == 2
