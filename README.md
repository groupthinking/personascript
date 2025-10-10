# PersonaScript

PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages, dramatically accelerating lead conversion and brand consistency.

## PersonaScriptPersonaCreatorAgent

The `PersonaScriptPersonaCreatorAgent` is an AI-powered agent that automatically creates detailed user personas and comprehensive content journey maps for PersonaScript's target audience.

### Features

- **Automated Persona Creation**: Generates detailed user personas with demographics, psychographics, and behavioral attributes
- **Content Journey Mapping**: Creates comprehensive journey maps covering awareness, consideration, and decision stages
- **Multi-Channel Output**: Delivers results via Miro (visual persona boards) and Google Docs (detailed journey maps)
- **Integration Ready**: Built-in support for Miro API, Google Docs API, and GitHub API
- **Extensible Architecture**: Easy to customize and extend for different use cases

### Agent Capabilities

The agent follows an 8-step execution plan:

1. **Analyze Input Data**: Processes product information, audience demographics, firmographics, and marketing collateral
2. **Identify User Segments**: Uses data analysis to identify distinct user segments
3. **Generate Persona Profiles**: Creates comprehensive persona profiles including:
   - Name and role
   - Company size and demographics
   - Goals and motivations
   - Challenges and pain points
   - Preferred content types
   - Information sources
4. **Develop Journey Maps**: Maps out content needs across sales funnel stages
5. **Create Miro Board**: Generates visual persona profiles in Miro
6. **Create Google Doc**: Produces detailed journey map documentation
7. **Compose GitHub Issue**: Prepares completion report
8. **Create GitHub Issue**: Posts results and captures URL

### Installation

```bash
# Clone the repository
git clone https://github.com/groupthinking/personascript.git
cd personascript

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The agent requires API credentials for external services. Configure via environment variables:

```bash
# Miro API
export MIRO_API_KEY="your_miro_api_key_here"

# Google Docs API
export GOOGLE_CREDENTIALS_PATH="/path/to/google-credentials.json"

# GitHub API
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_REPO="owner/repository"
```

### Usage

#### Basic Example

```python
from src.agents import PersonaScriptPersonaCreatorAgent
from src.agents.persona_creator_agent import AgentInputs

# Initialize the agent
agent = PersonaScriptPersonaCreatorAgent(
    miro_api_key="your_miro_key",
    google_docs_credentials={"credentials": "data"},
    github_token="your_github_token",
    github_repo="owner/repo"
)

# Prepare input data
inputs = AgentInputs(
    product_information="""
        PersonaScript empowers growth-stage B2B SaaS marketing teams...
    """,
    target_audience_demographics={
        "roles": ["Demand Generation Director", "Content Marketing Manager"]
    },
    target_audience_firmographics={
        "company_sizes": ["50-200", "200-500"]
    },
    marketing_collateral=["website", "case studies"],
    customer_interviews=None  # Optional
)

# Execute the agent
outputs = agent.execute(inputs)

# Access results
print(f"Miro Board: {outputs.miro_board_url}")
print(f"Google Doc: {outputs.google_docs_url}")
print(f"GitHub Issue: {outputs.github_issue_url}")
print(f"Generated {len(outputs.personas)} personas")
```

#### Running the Example

```bash
# Run the example usage script
python example_usage.py
```

### Generated Personas

The agent automatically generates personas tailored to B2B SaaS marketing teams:

1. **Demand Gen Director Sarah**
   - Focus: Lead generation at scale, ROI demonstration
   - Pain Points: Content bottlenecks, scaling personalization
   - Preferred Content: Case studies, ROI calculators, comparison guides

2. **Content Marketing Manager Alex**
   - Focus: Content quality and consistency at scale
   - Pain Points: Limited bandwidth, brand voice consistency
   - Preferred Content: How-to guides, templates, tutorials

3. **Growth Marketing Lead Jordan**
   - Focus: Rapid experimentation and growth
   - Pain Points: Slow content production, testing velocity
   - Preferred Content: Landing pages, email sequences, A/B test variations

### Content Journey Stages

Each persona's journey map includes three stages:

- **Awareness**: Understanding challenges and discovering solutions
- **Consideration**: Evaluating options and assessing fit
- **Decision**: Final validation and purchase commitment

For each stage, the journey map defines:
- User needs
- Key questions
- Content touchpoints
- Ideal content formats

### Testing

Run the test suite to verify functionality:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_persona_creator_agent.py
```

### Project Structure

```
personascript/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── persona_creator_agent.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── miro_integration.py
│   │   ├── google_docs_integration.py
│   │   └── github_integration.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_persona_creator_agent.py
│   └── test_integrations.py
├── example_usage.py
├── requirements.txt
└── README.md
```

### API Integration Notes

#### Miro Integration
- Creates visual persona boards with cards for each persona
- Supports custom layouts and styling
- Mock implementation provided when API key is not configured

#### Google Docs Integration
- Generates structured documents with markdown-style formatting
- Supports hierarchical content organization
- Mock implementation provided when credentials are not configured

#### GitHub Integration
- Creates completion issues with detailed reports
- Supports labels and assignees
- Mock implementation provided when token is not configured

### Extending the Agent

The agent is designed to be extensible. You can customize:

1. **Persona Generation Logic**: Modify `_create_persona_from_segment()` to adjust persona attributes
2. **Journey Map Structure**: Update `_create_journey_map_for_persona()` to change journey stages
3. **Output Formatting**: Customize `_format_persona_for_miro()` and `_format_journey_maps_for_doc()`
4. **Segmentation Logic**: Enhance `_identify_user_segments()` with ML-based clustering

### Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Type checking (if using mypy)
mypy src/

# Format code (if using black)
black src/ tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

[Add your license information here]

### Support

For questions or issues, please open a GitHub issue in this repository.
