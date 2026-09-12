"""
Execution script for PersonaScript CICDPipelineArchitectAgent.

This script demonstrates how to run the agent to design CI/CD pipelines,
compile a comprehensive blueprint, and create a tracking issue on GitHub.
"""

import os
import logging
from src.agents import CICDPipelineArchitectAgent, CICDInputs
from src.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("Starting PersonaScript CICDPipelineArchitectAgent")

    # Retrieve configuration from environment or config
    config = get_config()

    github_token = config["github"].get("token") or os.environ.get("GITHUB_TOKEN")
    github_repo = config["github"].get("repo") or os.environ.get("GITHUB_REPO", "groupthinking/personascript")

    # Initialize the agent
    agent = CICDPipelineArchitectAgent(
        github_token=github_token,
        github_repo=github_repo
    )

    # Define business context and task requirements
    inputs = CICDInputs(
        business_context="PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate high-volume, hyper-personalized, and brand-aligned content across all sales funnel stages.",
        task_to_automate="Implement CI/CD pipelines for automated testing, building, and deployment",
        target_platform="GitHub Actions",
        github_token=github_token,
        github_repo=github_repo
    )

    # Execute the agent
    logger.info("Executing pipeline architect workflow...")
    outputs = agent.execute(inputs)

    # Display results
    logger.info("\n" + "="*80)
    logger.info("AGENT EXECUTION COMPLETED SUCCESSFULLY")
    logger.info("="*80)
    logger.info(f"\n🔗 GitHub Issue URL:")
    logger.info(f"   {outputs.github_issue_url}")
    logger.info("\n✅ Consolidated CI/CD Pipeline Blueprint generated!")
    logger.info("High-Level Architecture & workflow YAMLs compiled successfully.")
    logger.info("="*80 + "\n")

    # Write the blueprint to a local file for records/review
    blueprint_filename = "CICD_PIPELINE_BLUEPRINT.md"
    with open(blueprint_filename, "w", encoding="utf-8") as f:
        f.write(outputs.consolidated_blueprint)
    logger.info(f"Saved consolidated blueprint to '{blueprint_filename}'")


if __name__ == "__main__":
    main()
