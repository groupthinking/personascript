"""
Example script to run and showcase the PersonaScriptMVPDevelopmentRoadmapAgent.
"""

import os
import logging
from src.agents.mvp_roadmap_agent import PersonaScriptMVPDevelopmentRoadmapAgent, RoadmapAgentInputs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution entry point."""
    logger.info("Initializing PersonaScriptMVPDevelopmentRoadmapAgent...")

    # Check if there are environment variables for actual integration
    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO", "groupthinking/personascript")

    # Initialize our roadmap agent
    agent = PersonaScriptMVPDevelopmentRoadmapAgent(
        openai_api_key=openai_key,
        github_token=github_token,
        github_repo=github_repo
    )

    # Define the precise inputs requested in the prompt
    inputs = RoadmapAgentInputs(
        company_name="PersonaScript",
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly "
            "generate high-volume, hyper-personalized, and brand-aligned content across "
            "all sales funnel stages, dramatically accelerating lead conversion and "
            "brand consistency."
        ),
        timeframe="3-6 months",
        target_platform="Linear",
        internal_docs_paths=["DOCUMENTATION.md", "README.md", "IMPLEMENTATION_SUMMARY.md"]
    )

    logger.info("Executing MVP Roadmap Agent...")
    outputs = agent.execute(inputs)

    print("\n" + "="*80)
    print("      PERSONASCRIPT MVP DEVELOPMENT ROADMAP GENERATION COMPLETE")
    print("="*80)
    print(f"\n🔗 GitHub Issue URL: {outputs.github_issue_url}")
    print(f"\n💡 Key Strategic Themes Identified:")
    for i, theme in enumerate(outputs.key_themes, 1):
        print(f"  {i}. {theme}")

    print("\n📦 MVP Roadmap (Linear Structured Epics & Features):")
    for epic in outputs.roadmap.epics:
        print(f"\n🚀 Epic: {epic.title} ({epic.id})")
        print(f"  Target Timeline: {epic.target_timeline}")
        print(f"  Description: {epic.description}")
        for feat in epic.features:
            print(f"    🛠 Feature: {feat.title} ({feat.id}) [Priority: {feat.priority}]")
            print(f"      Description: {feat.description}")
            print(f"      Linear User Stories:")
            for story in feat.user_stories:
                print(f"        - [{story.id}] {story.title} ({story.estimate}) - {story.priority} Priority")
                print(f"          Description: {story.description}")

    print("\n" + "="*80)
    logger.info("Example execution completed successfully.")


if __name__ == "__main__":
    main()
