# PersonaScript

PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages, dramatically accelerating lead conversion and brand consistency.

## UserInterviewAnalysisAgent

An intelligent agent that conducts comprehensive user interviews with target marketing leaders, analyzes their pain points, and generates prioritized feature wish lists to guide product development.

### Features

- **Automated Interview Workflow**: Simulates recruitment, scheduling, recording, and reporting flows end-to-end
- **Generated Transcripts**: Produces realistic transcript artifacts for testing and demos
- **Advanced Pain Point Analysis**: Uses deterministic extraction to identify, categorize, and prioritize pain points
- **Feature Extraction**: Automatically extracts and ranks feature suggestions based on frequency and alignment
- **Report Scaffolding**: Produces report structures and placeholder Notion URLs for downstream publishing
- **GitHub Integration**: Creates detailed GitHub issues with findings and recommendations when a token is configured

### Architecture

The agent is composed of modular components:

```
agents/
├── user_interview_agent.py    # Main agent orchestrator
├── config.py                   # Configuration management
├── interview_generator.py      # Question generation
├── recruitment.py              # Participant recruitment simulation
├── scheduling.py               # Interview scheduling simulation
├── transcription.py            # Transcript generation simulation
├── analysis.py                 # Pain point analysis
├── feature_extractor.py        # Feature wish list generation
├── reporting.py                # Report URL scaffolding
└── github_integration.py       # GitHub issue creation
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/groupthinking/personascript.git
cd personascript
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure credentials:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create a `.env` file with the following credentials:

```env
# OpenAI (required for AI features)
OPENAI_API_KEY=your_openai_api_key

# Zoom (required for interview scheduling)
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret
ZOOM_ACCOUNT_ID=your_zoom_account_id

# UserTesting.com (required for recruitment)
USERTESTING_API_KEY=your_usertesting_api_key

# Notion (required for reporting)
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id

# GitHub (required for issue creation)
GITHUB_TOKEN=your_github_token
GITHUB_REPO=groupthinking/personascript
```

### Usage

Run the agent:

```bash
python main.py
```

Or use it programmatically:

```python
from agents.user_interview_agent import UserInterviewAnalysisAgent
from agents.config import get_config

# Initialize agent
config = get_config()
agent = UserInterviewAnalysisAgent(config)

# Define target profile
target_profile = {
    "title": ["VP of Marketing", "Marketing Director", "CMO"],
    "company_size": "growth-stage B2B SaaS (50-500 employees)",
    "industry": "B2B SaaS"
}

# Execute
results = agent.execute(target_profile)

# Access results
print(f"Pain Point Analysis: {results['pain_point_analysis_url']}")
print(f"Feature Wish List: {results['feature_wishlist_url']}")
print(f"GitHub Issue: {results['github_issue_url']}")
```

### Workflow

The agent follows a 12-step workflow:

1. **Parse Context** - Analyzes value proposition and target profile
2. **Generate Questions** - Creates comprehensive interview questions
3. **Recruit Participants** - Finds 20+ target marketing leaders
4. **Schedule Interviews** - Creates simulated 30-minute sessions
5. **Conduct Interviews** - Facilitates and records sessions
6. **Transcribe** - Generates transcript artifacts from simulated recordings
7. **Analyze Pain Points** - Performs NLP analysis on transcripts
8. **Synthesize Report** - Creates detailed pain point analysis
9. **Extract Features** - Identifies and prioritizes feature suggestions
10. **Create Notion Reports** - Produces report URLs and structures for publishing
11. **Construct Issue** - Prepares GitHub issue content
12. **Create GitHub Issue** - Posts findings to repository

### Outputs

The agent generates:

- **Pain Point Analysis Report** (placeholder URL): Detailed breakdown of identified challenges
- **Prioritized Feature Wish List** (placeholder URL): Ranked feature suggestions
- **Interview Recordings** (simulated): Video/audio file metadata for sessions
- **Transcripts**: Text versions of all interviews
- **GitHub Issue**: Comprehensive summary with links to all artifacts

### Testing

The agent includes simulated implementations for most external services, allowing you to test without API credentials:

```bash
# Run without credentials - uses mock data
python main.py
```

### Dependencies

- `openai>=1.0.0` - Optional OpenAI-backed question generation
- `requests>=2.31.0` - API interactions
- `python-dotenv>=1.0.0` - Environment configuration
- `pydantic>=2.0.0` - Data validation

### Development

The codebase is structured for easy extension:

- Add new analysis methods in `analysis.py`
- Extend feature extraction in `feature_extractor.py`
- Customize report format in `reporting.py`
- Modify interview questions in `interview_generator.py`

### License

MIT License - See LICENSE file for details

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Support

For issues or questions:
- Open a GitHub issue
- Contact: support@personascript.com
