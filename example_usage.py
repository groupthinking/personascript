"""
Example usage of PersonaScriptPersonaCreatorAgent.

This script demonstrates how to use the agent to create personas and journey maps.
"""

import logging
from src.agents import PersonaScriptPersonaCreatorAgent
from src.agents.persona_creator_agent import AgentInputs
from src.config import get_config, load_google_credentials

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("Starting PersonaScript Persona Creator Agent")
    
    # Get configuration
    config = get_config()
    
    # Initialize the agent
    agent = PersonaScriptPersonaCreatorAgent(
        miro_api_key=config["miro"]["api_key"],
        google_docs_credentials=load_google_credentials(),
        github_token=config["github"]["token"],
        github_repo=config["github"]["repo"]
    )
    
    # Prepare input data
    inputs = AgentInputs(
        product_information="""
        PersonaScript empowers growth-stage B2B SaaS marketing teams to rapidly generate 
        high-volume, hyper-personalized, and brand-aligned content across all sales funnel 
        stages, dramatically accelerating lead conversion and brand consistency.
        
        Key Features:
        - AI-powered content generation
        - Brand voice consistency
        - Multi-persona targeting
        - Content personalization at scale
        - Integration with marketing tools
        """,
        target_audience_demographics={
            "age_ranges": ["25-35", "35-45", "45-55"],
            "experience_levels": ["3-8 years", "8-15 years", "15+ years"],
            "roles": [
                "Demand Generation Director",
                "Content Marketing Manager", 
                "Growth Marketing Lead"
            ]
        },
        target_audience_firmographics={
            "company_sizes": ["20-100", "100-500", "500+"],
            "industries": ["B2B SaaS", "Technology", "Professional Services"],
            "company_stages": ["Series A", "Series B", "Growth Stage"]
        },
        marketing_collateral=[
            "Website copy",
            "Case studies",
            "Blog posts",
            "Email campaigns",
            "Social media content"
        ],
        customer_interviews=None  # Optional
    )
    
    # Execute the agent
    logger.info("Executing agent workflow...")
    outputs = agent.execute(inputs)
    
    # Display results
    logger.info("\n" + "="*80)
    logger.info("AGENT EXECUTION COMPLETED SUCCESSFULLY")
    logger.info("="*80)
    logger.info(f"\n📊 Miro Board URL:")
    logger.info(f"   {outputs.miro_board_url}")
    logger.info(f"\n📄 Google Docs URL:")
    logger.info(f"   {outputs.google_docs_url}")
    logger.info(f"\n🔗 GitHub Issue URL:")
    logger.info(f"   {outputs.github_issue_url}")
    logger.info(f"\n✅ Generated {len(outputs.personas)} personas:")
    for persona in outputs.personas:
        logger.info(f"   - {persona.name} ({persona.role})")
    logger.info(f"\n✅ Created {len(outputs.journey_maps)} content journey maps")
    logger.info("="*80 + "\n")


if __name__ == "__main__":
    main()
