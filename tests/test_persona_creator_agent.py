"""
Unit tests for PersonaScriptPersonaCreatorAgent.
"""

import pytest
from urllib.parse import urlparse
from src.agents.persona_creator_agent import (
    PersonaScriptPersonaCreatorAgent,
    AgentInputs,
    PersonaProfile,
    ContentJourneyMap,
    ContentJourneyStage
)


@pytest.fixture
def sample_inputs():
    """Create sample input data for testing."""
    return AgentInputs(
        product_information="Test product information",
        target_audience_demographics={"age": "30-40", "experience": "5-10 years"},
        target_audience_firmographics={"company_size": "50-200"},
        marketing_collateral=["Test collateral 1", "Test collateral 2"],
        customer_interviews=None
    )


@pytest.fixture
def agent():
    """Create an agent instance for testing."""
    return PersonaScriptPersonaCreatorAgent()


def test_agent_initialization():
    """Test that agent initializes correctly."""
    agent = PersonaScriptPersonaCreatorAgent()
    assert agent is not None
    assert agent.miro_integration is not None
    assert agent.google_docs_integration is not None
    assert agent.github_integration is not None
    assert len(agent.personas) == 0
    assert len(agent.journey_maps) == 0


def test_agent_with_credentials():
    """Test agent initialization with credentials."""
    agent = PersonaScriptPersonaCreatorAgent(
        miro_api_key="test_key",
        google_docs_credentials={"type": "service_account"},
        github_token="test_token",
        github_repo="owner/repo"
    )
    assert agent.miro_integration.api_key == "test_key"
    assert agent.google_docs_integration.credentials is not None
    assert agent.github_integration.token == "test_token"
    assert agent.github_integration.repo == "owner/repo"


def test_analyze_input_data(agent, sample_inputs):
    """Test input data analysis."""
    results = agent._analyze_input_data(sample_inputs)
    assert "product_summary" in results
    assert "audience_insights" in results
    assert "content_themes" in results
    assert "interview_insights" in results


def test_identify_user_segments(agent, sample_inputs):
    """Test user segment identification."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    
    assert len(segments) > 0
    assert all("name" in seg for seg in segments)
    assert all("role_category" in seg for seg in segments)
    assert all("company_size_range" in seg for seg in segments)


def test_generate_persona_profiles(agent, sample_inputs):
    """Test persona profile generation."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    personas = agent._generate_persona_profiles(segments, sample_inputs)
    
    assert len(personas) > 0
    assert all(isinstance(p, PersonaProfile) for p in personas)
    assert all(p.name for p in personas)
    assert all(p.role for p in personas)
    assert all(len(p.goals) > 0 for p in personas)
    assert all(len(p.challenges) > 0 for p in personas)


def test_develop_journey_maps(agent, sample_inputs):
    """Test content journey map development."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    personas = agent._generate_persona_profiles(segments, sample_inputs)
    journey_maps = agent._develop_journey_maps(personas)
    
    assert len(journey_maps) == len(personas)
    assert all(isinstance(jm, ContentJourneyMap) for jm in journey_maps)
    
    for journey_map in journey_maps:
        assert journey_map.persona_name
        assert len(journey_map.stages) > 0
        
        # Check that all three stages exist
        stage_names = [s.stage_name for s in journey_map.stages]
        assert "Awareness" in stage_names
        assert "Consideration" in stage_names
        assert "Decision" in stage_names
        
        # Check stage completeness
        for stage in journey_map.stages:
            assert len(stage.needs) > 0
            assert len(stage.questions) > 0
            assert len(stage.content_touchpoints) > 0
            assert len(stage.content_formats) > 0


def test_create_miro_board(agent, sample_inputs):
    """Test Miro board creation."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    personas = agent._generate_persona_profiles(segments, sample_inputs)
    
    miro_url = agent._create_miro_board(personas)
    
    assert miro_url
    # Use proper URL parsing for validation
    parsed = urlparse(miro_url)
    assert parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert parsed.netloc.endswith("miro.com")


def test_create_google_doc(agent, sample_inputs):
    """Test Google Doc creation."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    personas = agent._generate_persona_profiles(segments, sample_inputs)
    journey_maps = agent._develop_journey_maps(personas)
    
    docs_url = agent._create_google_doc(journey_maps)
    
    assert docs_url
    # Use proper URL parsing for validation
    parsed = urlparse(docs_url)
    assert parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert parsed.netloc.endswith("docs.google.com")


def test_create_github_issue(agent, sample_inputs):
    """Test GitHub issue creation."""
    miro_url = "https://miro.com/app/board/test/"
    docs_url = "https://docs.google.com/document/d/test/edit"
    
    github_url = agent._create_github_issue(miro_url, docs_url, sample_inputs)
    
    assert github_url
    # Use proper URL parsing for validation
    parsed = urlparse(github_url)
    assert parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert parsed.netloc.endswith("github.com")
    # Check path contains "issues"
    assert parsed.path.startswith("/") and "issues" in parsed.path.split("/")


def test_full_execution(agent, sample_inputs):
    """Test full agent execution."""
    outputs = agent.execute(sample_inputs)
    
    # Check all outputs are present
    assert outputs.miro_board_url
    assert outputs.google_docs_url
    assert outputs.github_issue_url
    assert len(outputs.personas) > 0
    assert len(outputs.journey_maps) > 0
    
    # Check URLs are valid using proper URL parsing
    miro_parsed = urlparse(outputs.miro_board_url)
    assert miro_parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert miro_parsed.netloc.endswith("miro.com")
    
    docs_parsed = urlparse(outputs.google_docs_url)
    assert docs_parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert docs_parsed.netloc.endswith("docs.google.com")
    
    github_parsed = urlparse(outputs.github_issue_url)
    assert github_parsed.scheme == "https"
    # Validate that netloc ends with expected domain
    assert github_parsed.netloc.endswith("github.com")
    # Check path contains "issues"
    assert github_parsed.path.startswith("/") and "issues" in github_parsed.path.split("/")
    
    # Check personas were stored
    assert len(agent.personas) == len(outputs.personas)
    assert len(agent.journey_maps) == len(outputs.journey_maps)


def test_format_persona_for_miro(agent):
    """Test persona formatting for Miro."""
    persona = PersonaProfile(
        name="Test User",
        role="Test Role",
        company_size="50-200",
        goals=["Goal 1", "Goal 2"],
        challenges=["Challenge 1"],
        pain_points=["Pain 1"],
        motivations=["Motivation 1"],
        preferred_content_types=["Blog", "Video"],
        information_sources=["LinkedIn"]
    )
    
    formatted = agent._format_persona_for_miro(persona)
    
    assert formatted["name"] == "Test User"
    assert formatted["role"] == "Test Role"
    assert len(formatted["goals"]) == 2
    assert "content_preferences" in formatted


def test_format_journey_maps_for_doc(agent, sample_inputs):
    """Test journey map formatting for Google Docs."""
    analysis = agent._analyze_input_data(sample_inputs)
    segments = agent._identify_user_segments(analysis)
    personas = agent._generate_persona_profiles(segments, sample_inputs)
    journey_maps = agent._develop_journey_maps(personas)
    
    content = agent._format_journey_maps_for_doc(journey_maps)
    
    assert content
    assert "PersonaScript Content Journey Maps" in content
    assert "Awareness Stage" in content
    assert "Consideration Stage" in content
    assert "Decision Stage" in content
    
    # Check that all personas are included
    for journey_map in journey_maps:
        assert journey_map.persona_name in content


def test_compose_issue_content(agent, sample_inputs):
    """Test GitHub issue content composition."""
    agent.personas = [
        PersonaProfile(
            name="Test Persona",
            role="Test Role",
            company_size="Test Size",
            goals=[],
            challenges=[],
            pain_points=[],
            motivations=[],
            preferred_content_types=[],
            information_sources=[]
        )
    ]
    
    miro_url = "https://miro.com/app/board/test/"
    docs_url = "https://docs.google.com/document/d/test/edit"
    
    content = agent._compose_issue_content(miro_url, docs_url, sample_inputs)
    
    assert "PersonaScript Persona Creation" in content
    assert miro_url in content
    assert docs_url in content
    assert "Test Persona" in content
    assert "Goal" in content
    assert "Outputs Generated" in content
    assert "Execution Summary" in content
