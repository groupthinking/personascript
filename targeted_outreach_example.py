"""
Example usage of PersonaScript TargetedOutreachAgent.

This script demonstrates how to initialize and execute the TargetedOutreachAgent
to initiate outbound sales pipelines and configure LinkedIn Ads campaigns.
"""

import logging
from src.agents import TargetedOutreachAgent, TargetedOutreachInputs
from src.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("Starting PersonaScript Targeted Outreach Agent Example")

    # Retrieve configuration settings
    config = get_config()

    # Initialize the Targeted Outreach Agent
    agent = TargetedOutreachAgent(
        apollo_api_key=config["apollo"]["api_key"],
        linkedin_client_id=config["linkedin"]["client_id"],
        linkedin_client_secret=config["linkedin"]["client_secret"],
        linkedin_account_id=config["linkedin"]["account_id"],
        github_token=config["github"]["token"],
        github_repo=config["github"]["repo"]
    )

    # Define Campaign Input parameters (using target marketing ICP)
    inputs = TargetedOutreachInputs(
        icp_industries=["B2B SaaS", "Technology", "Marketing Technology"],
        icp_company_sizes=["50-200", "201-500"],
        icp_job_titles=["VP of Marketing", "Director of Demand Generation", "CMO"],
        ad_budget=3500.0,
        ad_objective="LEAD_GENERATION",
        ad_copy=(
            "Tired of manual, slow content personalization? Boost lead conversion by 3x "
            "with PersonaScript. Set up hyper-personalized sales funnels in minutes!"
        ),
        ad_asset_url="https://personascript.com/static/ads/banner-lead-gen.png",
        message_template=(
            "Hi {first_name},\n\n"
            "I noticed you lead marketing efforts as {title} at {company_name}. "
            "Many growth-stage teams in {industry} struggle with maintaining brand "
            "consistency while scaling content output. We built PersonaScript to "
            "automate this seamlessly.\n\n"
            "Would you be open to a quick 10-minute chat next Tuesday?\n\n"
            "Best,\nSales Team @ PersonaScript"
        )
    )

    # Execute Campaign
    logger.info("Executing TargetedOutreachAgent workflow...")
    outputs = agent.execute(inputs)

    # Output execution summary
    logger.info("\n" + "="*80)
    logger.info("TARGETED OUTREACH CAMPAIGN EXECUTED SUCCESSFULLY")
    logger.info("="*80)
    logger.info(f"\n📂 Leads list file generated: {outputs.lead_list_file_path}")
    logger.info(f"   (Contains contact details & personalized drafts for {len(outputs.leads)} qualified leads)")
    logger.info(f"\n🚀 LinkedIn Ads Campaign Configured:")
    logger.info(f"   Campaign ID: {outputs.linkedin_campaign_id}")
    logger.info(f"   Dashboard Link: {outputs.linkedin_dashboard_url}")
    logger.info(f"\n📊 Initial Ad Performance Stats:")
    logger.info(f"   Impressions: {outputs.performance_metrics['impressions']:,}")
    logger.info(f"   Clicks: {outputs.performance_metrics['clicks']}")
    logger.info(f"   Ad Spend: ${outputs.performance_metrics['spend']:,.2f}")
    logger.info(f"   CTR: {outputs.performance_metrics['ctr']:.2%}")
    logger.info(f"\n🔗 Published Report (GitHub Issue):")
    logger.info(f"   {outputs.github_issue_url}")
    logger.info("="*80 + "\n")


if __name__ == "__main__":
    main()
