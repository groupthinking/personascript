"""
Example usage of UserInterviewAnalysisAgent
"""
from agents.user_interview_agent import UserInterviewAnalysisAgent
from agents.config import AgentConfig

# Example 1: Basic usage with default configuration
print("Example 1: Basic Usage")
print("=" * 80)

agent = UserInterviewAnalysisAgent()

target_profile = {
    "title": ["VP of Marketing", "Marketing Director", "CMO"],
    "company_size": "growth-stage B2B SaaS (50-500 employees)",
    "industry": "B2B SaaS"
}

results = agent.execute(target_profile)

if results['status'] == 'success':
    print(f"✓ Pain Point Analysis: {results['pain_point_analysis_url']}")
    print(f"✓ Feature Wish List: {results['feature_wishlist_url']}")
    print(f"✓ GitHub Issue: {results['github_issue_url']}")
    print(f"✓ Interviews Conducted: {len(results['recording_urls'])}")
else:
    print(f"✗ Error: {results.get('error', 'Unknown error')}")

print()

# Example 2: Custom configuration
print("Example 2: Custom Configuration")
print("=" * 80)

config = AgentConfig(
    target_interview_count=10,  # Fewer interviews
    interview_duration_minutes=45  # Longer interviews
)

agent2 = UserInterviewAnalysisAgent(config)
results2 = agent2.execute(target_profile)

print(f"Conducted {len(results2.get('recording_urls', []))} interviews")
print()

# Example 3: Access detailed execution log
print("Example 3: Execution Log")
print("=" * 80)

if 'execution_log' in results:
    completed_steps = [
        entry for entry in results['execution_log'] 
        if entry['status'] == 'completed'
    ]
    print(f"Completed {len(completed_steps)} steps:")
    for entry in completed_steps:
        print(f"  Step {entry['step']}: {entry['description']}")
