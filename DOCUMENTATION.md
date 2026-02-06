# UserInterviewAnalysisAgent Documentation

## Overview

The UserInterviewAnalysisAgent is an intelligent automation system designed to conduct comprehensive user interviews with target marketing leaders, analyze their pain points using advanced NLP techniques, and generate prioritized feature wish lists to guide product development.

## Architecture

### Core Components

The agent is built on a modular architecture with the following components:

#### 1. **UserInterviewAnalysisAgent** (`user_interview_agent.py`)
Main orchestrator that coordinates the entire workflow across 12 distinct steps.

**Key Methods:**
- `execute(target_profile, interview_template)` - Main execution method
- `_parse_context(target_profile)` - Context parsing and objective setting
- `_construct_issue_content(results)` - GitHub issue content generation

#### 2. **Configuration Management** (`config.py`)
Handles all configuration and credentials using Pydantic models.

**Environment Variables:**
- `OPENAI_API_KEY` - For AI-powered features
- `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `ZOOM_ACCOUNT_ID` - For interview scheduling
- `USERTESTING_API_KEY` - For participant recruitment
- `NOTION_API_KEY`, `NOTION_DATABASE_ID` - For report publishing
- `GITHUB_TOKEN`, `GITHUB_REPO` - For issue creation

#### 3. **Interview Question Generator** (`interview_generator.py`)
Generates comprehensive interview questions using OpenAI GPT-4.

**Features:**
- Context-aware question generation
- Default question fallback
- Category-based organization
- Template support

#### 4. **User Recruitment** (`recruitment.py`)
Manages participant recruitment via UserTesting.com API.

**Capabilities:**
- Target profile matching
- Configurable participant count
- Mock recruitment for testing

#### 5. **Interview Scheduler** (`scheduling.py`)
Handles scheduling and conducting interviews via Zoom API.

**Functions:**
- Interview scheduling with calendar management
- Automated recording
- Mock scheduling for development

#### 6. **Transcription Service** (`transcription.py`)
Converts interview recordings to text using OpenAI Whisper.

**Features:**
- Batch transcription
- Realistic mock transcriptions
- Error handling and retries

#### 7. **Pain Point Analyzer** (`analysis.py`)
Performs NLP analysis to extract and categorize pain points.

**Analysis Capabilities:**
- Keyword-based extraction
- Severity assessment (high/medium/low)
- Category classification
- Quote extraction
- Frequency aggregation
- Report generation

#### 8. **Feature Wish List Generator** (`feature_extractor.py`)
Extracts and prioritizes feature suggestions from interviews.

**Prioritization Criteria:**
- Frequency of mention (0-40 points)
- Explicit mentions (0-20 points)
- Alignment with value proposition (0-40 points)

**Priority Levels:**
- Critical: 70+ points
- High: 50-69 points
- Medium: 30-49 points
- Low: <30 points

#### 9. **Notion Reporter** (`reporting.py`)
Publishes comprehensive reports to Notion.

**Report Types:**
- Pain Point Analysis Report
- Prioritized Feature Wish List

**Content Structure:**
- Executive summary
- Detailed findings
- Category breakdowns
- Recommendations

#### 10. **GitHub Integration** (`github_integration.py`)
Creates GitHub issues with analysis results.

**Issue Content:**
- Execution summary
- Output URLs
- Key findings
- Next steps

## Workflow

### 12-Step Execution Process

1. **Parse Context**
   - Analyzes value proposition
   - Processes target profile
   - Defines interview objectives

2. **Generate Questions**
   - Creates 15-20 open-ended questions
   - Organizes by category
   - Focuses on pain points and features

3. **Recruit Participants**
   - Targets marketing leaders
   - Applies profile criteria
   - Recruits 20+ participants

4. **Schedule Interviews**
   - Books 30-minute sessions
   - Manages calendar conflicts
   - Sends automated invitations

5. **Conduct Interviews**
   - Facilitates sessions
   - Records video/audio
   - Ensures quality capture

6. **Transcribe Recordings**
   - Converts audio to text
   - Uses OpenAI Whisper
   - Generates clean transcripts

7. **Analyze Pain Points**
   - Performs NLP analysis
   - Identifies common themes
   - Assesses severity and frequency

8. **Synthesize Report**
   - Creates detailed analysis
   - Summarizes findings
   - Provides recommendations

9. **Extract Features**
   - Identifies feature requests
   - Consolidates suggestions
   - Prioritizes by impact

10. **Create Notion Reports**
    - Publishes pain point analysis
    - Publishes feature wish list
    - Links interview artifacts

11. **Construct GitHub Issue**
    - Prepares comprehensive summary
    - Includes all output URLs
    - Documents execution steps

12. **Create GitHub Issue**
    - Posts to repository
    - Adds appropriate labels
    - Completes workflow

## Usage Examples

### Basic Usage

```python
from agents.user_interview_agent import UserInterviewAnalysisAgent

agent = UserInterviewAnalysisAgent()

target_profile = {
    "title": ["VP of Marketing", "Marketing Director", "CMO"],
    "company_size": "50-500 employees",
    "industry": "B2B SaaS"
}

results = agent.execute(target_profile)
print(f"Pain Points: {results['pain_point_analysis_url']}")
print(f"Features: {results['feature_wishlist_url']}")
```

### Custom Configuration

```python
from agents.config import AgentConfig
from agents.user_interview_agent import UserInterviewAnalysisAgent

config = AgentConfig(
    target_interview_count=30,
    interview_duration_minutes=45
)

agent = UserInterviewAnalysisAgent(config)
results = agent.execute(target_profile)
```

### With Interview Template

```python
template = """
Introduction (5 min)
- Welcome and overview
- Recording consent

Discovery (20 min)
- Current workflow
- Pain points
- Wish list

Wrap-up (5 min)
- Summary
- Next steps
"""

results = agent.execute(target_profile, template)
```

## Testing

### Running Tests

```bash
# Run all tests
python -m unittest tests.test_agent

# Run specific test class
python -m unittest tests.test_agent.TestUserInterviewAnalysisAgent

# Run with verbose output
python -m unittest tests.test_agent -v
```

### Test Coverage

- Agent initialization
- Context parsing
- Workflow execution
- Question generation
- Pain point analysis
- Feature extraction
- Issue creation

## Development

### Adding New Analysis Methods

To add custom analysis methods to the Pain Point Analyzer:

```python
# In agents/analysis.py

def custom_analysis(self, transcripts):
    """Your custom analysis logic"""
    # Process transcripts
    # Extract insights
    return results
```

### Extending Feature Extraction

To add new feature extraction patterns:

```python
# In agents/feature_extractor.py

feature_patterns = {
    "Your New Feature": [
        "keyword1", "keyword2", "keyword3"
    ]
}
```

### Customizing Reports

To modify Notion report format:

```python
# In agents/reporting.py

def _build_custom_content(self, data):
    """Build custom report structure"""
    return {
        "title": "Custom Report",
        "sections": [
            # Your custom sections
        ]
    }
```

## API Integration Details

### OpenAI API
- **Models Used:** GPT-4, Whisper
- **Rate Limits:** Handled automatically
- **Error Handling:** Fallback to mock data

### Zoom API
- **OAuth 2.0:** Server-to-Server authentication
- **Endpoints:** Meetings, Recordings
- **Webhooks:** Optional for real-time updates

### UserTesting.com API
- **Authentication:** API Key
- **Recruitment:** Demographic targeting
- **Scheduling:** Integrated with Zoom

### Notion API
- **Version:** 2022-06-28
- **Authentication:** Bearer token
- **Operations:** Page creation, database updates

### GitHub API
- **Version:** v3 (REST)
- **Authentication:** Personal Access Token
- **Operations:** Issue creation, labeling

## Output Formats

### Pain Point Analysis Report

```
Executive Summary
├── Total pain points identified
├── High severity count
└── Categories covered

Top Pain Points
├── Pain Point 1 (Frequency, Severity)
├── Pain Point 2 (Frequency, Severity)
└── Pain Point 3 (Frequency, Severity)

Pain Points by Category
├── Content (X pain points)
├── Personalization (Y pain points)
└── Brand (Z pain points)

Recommendations
├── Recommendation 1
├── Recommendation 2
└── Recommendation 3
```

### Feature Wish List

```
Overview
└── Total features, prioritization method

Critical Priority Features
├── Feature 1 (Score, Frequency)
└── Feature 2 (Score, Frequency)

High Priority Features
├── Feature 3 (Score, Frequency)
└── Feature 4 (Score, Frequency)

Medium Priority Features
└── Feature 5 (Score, Frequency)

Low Priority Features
└── Feature 6 (Score, Frequency)
```

## Best Practices

1. **Configuration Management**
   - Use environment variables for credentials
   - Never commit API keys
   - Use `.env` files locally

2. **Error Handling**
   - Agent includes comprehensive error handling
   - Falls back to mock data when APIs unavailable
   - Logs all errors for debugging

3. **Testing**
   - Test without API credentials using mock mode
   - Validate with real credentials in staging
   - Run full test suite before deployment

4. **Scalability**
   - Batch operations where possible
   - Handle rate limits gracefully
   - Use async operations for long-running tasks

5. **Security**
   - Rotate API keys regularly
   - Use minimal required permissions
   - Audit access logs periodically

## Troubleshooting

### Common Issues

**Issue: API authentication fails**
- Verify credentials in `.env`
- Check API key permissions
- Confirm account has necessary access

**Issue: Transcription takes too long**
- Reduce interview count
- Use batch processing
- Enable async mode

**Issue: Pain points not detected**
- Review transcript quality
- Adjust keyword patterns
- Use OpenAI for better NLP

**Issue: Notion reports not created**
- Verify Notion API key
- Check database permissions
- Ensure database ID is correct

## Performance

### Benchmarks

- **20 Interviews:** ~5-10 minutes (with real APIs)
- **Transcription:** ~30 seconds per 30-minute interview
- **Analysis:** ~1-2 minutes for 20 transcripts
- **Report Generation:** ~10-15 seconds

### Optimization Tips

1. Use batch operations for transcription
2. Cache frequently accessed data
3. Parallel API calls where possible
4. Optimize prompts for faster responses

## Support and Contributing

### Getting Help

- GitHub Issues: Report bugs or request features
- Documentation: Refer to README.md
- Examples: See examples.py for usage patterns

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for full details
