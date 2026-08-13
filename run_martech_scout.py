"""
Example usage of the MarTechPartnershipScoutAgent.

This script demonstrates how to configure and execute the partnership scouting workflow.
"""

import logging
from src.agents import (
    MarTechPartnershipScoutAgent,
    ScoutAgentInputs,
    PartnershipCriteria
)
from src.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting PersonaScript MarTech Partnership Scout Agent Example")

    # Retrieve common config parameters (Miro, Google, GitHub, etc.)
    config = get_config()

    # Initialize the scout agent
    # We can pass specific credentials if available; otherwise, the agent defaults to simulation mode.
    agent = MarTechPartnershipScoutAgent(
        github_token=config["github"]["token"],
        github_repo=config["github"]["repo"]
    )

    # Define the input parameters
    inputs = ScoutAgentInputs(
        value_proposition=(
            "PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate "
            "high-volume, hyper-personalized, and brand-aligned content across all sales funnel "
            "stages, dramatically accelerating lead conversion and brand consistency."
        ),
        criteria=PartnershipCriteria(
            target_audiences=[
                "B2B SaaS Marketing Teams",
                "Demand Generation",
                "Content Marketers",
                "Growth Marketing"
            ],
            tech_stacks=[
                "HubSpot",
                "Marketo",
                "ActiveCampaign",
                "Zapier",
                "Salesforce"
            ],
            min_market_reach="growth stage or established"
        )
    )

    # Execute the scouting agent
    logger.info("Executing partnership scout agent workflow...")
    outputs = agent.execute(inputs)

    # Log and summarize scouting findings
    logger.info("\n" + "="*80)
    logger.info("PARTNERSHIP SCOUT AGENT EXECUTION COMPLETED SUCCESSFULLY")
    logger.info("="*80)
    logger.info(f"\n📑 Notion Comprehensive Scout Report URL:")
    logger.info(f"   {outputs.comprehensive_report_url}")
    logger.info(f"\n🔗 GitHub Issue URL:")
    logger.info(f"   {outputs.github_issue_url}")
    logger.info(f"\n✅ Identified {len(outputs.leads)} Potential Partnership Leads:")
    for lead in outputs.leads:
        pri_str = "🔥 [High Priority]" if lead.is_high_priority else ""
        logger.info(f"   - {lead.name} ({lead.type}) - Compatibility: {lead.compatibility_score:.2f} {pri_str}")

    logger.info(f"\n✅ Drafted {len(outputs.proposals)} Preliminary Partnership Proposals in Notion:")
    for proposal in outputs.proposals:
        logger.info(f"   - proposal for {proposal.lead_name} stored at: {proposal.notion_url}")

    logger.info("="*80 + "\n")


if __name__ == "__main__":
    main()
