# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure (Optional)

For testing without API keys:
```bash
# No configuration needed - agent works with mock data
python main.py
```

For credentialed runs:
```bash
cp .env.example .env
# Edit .env with your API keys
python main.py
```

Note: the current implementation uses live GitHub issue creation when `GITHUB_TOKEN` is set, optional OpenAI question generation when `OPENAI_API_KEY` is set, and simulated recruitment/scheduling/transcription/report publishing for the remaining steps.

### 3. Run Your First Interview Analysis

```bash
python main.py
```

Expected output:
```
INFO:__main__:Starting UserInterviewAnalysisAgent
INFO:__main__:Executing interview analysis workflow
...
INFO:__main__:EXECUTION COMPLETED SUCCESSFULLY
Pain Point Analysis: https://notion.so/pain-point-analysis-...
Feature Wish List: https://notion.so/feature-wishlist-...
GitHub Issue: https://github.com/groupthinking/personascript/issues/...
```

## Common Use Cases

### Use Case 1: Quick Test Run

```python
from agents.user_interview_agent import UserInterviewAnalysisAgent

agent = UserInterviewAnalysisAgent()
results = agent.execute({"title": ["VP of Marketing"]})
print(f"Status: {results['status']}")
```

### Use Case 2: Custom Interview Count

```python
from agents.config import AgentConfig
from agents.user_interview_agent import UserInterviewAnalysisAgent

config = AgentConfig(target_interview_count=10)
agent = UserInterviewAnalysisAgent(config)
results = agent.execute({"title": ["Marketing Director"]})
```

### Use Case 3: Access Detailed Results

```python
agent = UserInterviewAnalysisAgent()
results = agent.execute({"title": ["CMO"]})

if results['status'] == 'success':
    print(f"Pain Points Found: {len(results.get('pain_points', []))}")
    print(f"Features Identified: {len(results.get('feature_wishlist', []))}")
    print(f"Execution Steps: {len(results['execution_log'])}")
```

## What's Included

✓ Interview question generation
✓ Participant recruitment simulation
✓ Interview scheduling and recording simulation
✓ Automatic transcript generation
✓ Pain point analysis
✓ Feature wish list generation
✓ Report URL generation
✓ GitHub issue creation

## Next Steps

1. **Explore Examples:** `python examples.py`
2. **Run Tests:** `python -m unittest tests.test_agent`
3. **Read Documentation:** See `DOCUMENTATION.md`
4. **Configure APIs:** Edit `.env` for production use

## Troubleshooting

**Q: Agent runs but uses mock data?**
A: This is normal. Most integrations are simulated today; adding credentials enables GitHub issue creation and optional OpenAI question generation.

**Q: How do I see what the agent is doing?**
A: Check the console logs - they show each step in detail.

**Q: Can I customize the interview questions?**
A: Yes! Pass a custom `interview_template` to `agent.execute()`.

**Q: Where are the results saved?**
A: Results are saved to `results.json` after execution.

## Support

- Issues: https://github.com/groupthinking/personascript/issues
- Email: support@personascript.com
