"""
Example usage of BetaProgramManagerAgent.

This script demonstrates how to programmatically instantiate and execute the
BetaProgramManagerAgent with a list of secured alpha customers and a stress-test plan,
and displays the generated comprehensive report and GitHub issue URL.
"""

import logging
from src.agents import (
    BetaProgramManagerAgent,
    AlphaCustomer,
    StressTestPlan,
    BetaAgentInputs
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting PersonaScript Beta Program Manager Agent Demo")

    # 1. Define a list of secured B2B SaaS alpha customers
    alpha_customers = [
        AlphaCustomer(name="Sarah Connor", email="sarah@acme.com", company="Acme Corp"),
        AlphaCustomer(name="Alex Murphy", email="alex@globex.com", company="Globex"),
        AlphaCustomer(name="John Doe", email="john@umbrella.com", company="Umbrella Pharmaceuticals")
    ]

    # 2. Define the beta program stress-test plan details
    stress_test_plan = StressTestPlan(
        title="High Load Content Generation Staging Plan",
        test_scenarios=[
            "Scenario 1: Generate 150+ custom B2B marketing articles simultaneously under high concurrent volume load.",
            "Scenario 2: Apply custom vocabulary files up to 50MB and check system consistency.",
            "Scenario 3: Stress-test multi-persona targeting rules under peak concurrent API utilization."
        ],
        target_metrics={
            "max_concurrency": 200,
            "error_rate_threshold": 0.01,
            "avg_latency_ms": 1200
        },
        duration_days=14
    )

    # 3. Instantiate the BetaProgramManagerAgent
    # (Leaving parameters empty to fallback to config environment values or mock implementations)
    agent = BetaProgramManagerAgent()

    # 4. Prepare inputs
    inputs = BetaAgentInputs(
        alpha_customers=alpha_customers,
        stress_test_plan=stress_test_plan
    )

    # 5. Execute the agent workflow
    logger.info("Executing beta program orchestrator...")
    outputs = agent.execute(inputs)

    # 6. Display generated results
    print("\n" + "="*80)
    print("BETA PROGRAM MANAGER AGENT EXECUTION SUMMARY")
    print("="*80)
    print(f"\nReport Title: {outputs.report.title}")
    print(f"Total Participants: {outputs.report.total_participants}")
    print(f"Active Participants: {outputs.report.active_participants}")
    print(f"Bugs Logged: {len(outputs.report.bugs_identified)}")
    print(f"Features Backlogged: {len(outputs.report.feature_requests)}")
    print(f"\nGitHub Issue URL:\n   {outputs.github_issue_url}")
    print("\n" + "-"*40)
    print("COMPILED REPORT PREVIEW")
    print("-"*40)
    # Print the first 25 lines of the report
    lines = outputs.report.raw_markdown.split("\n")
    preview = "\n".join(lines[:25])
    print(preview)
    print("...")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
