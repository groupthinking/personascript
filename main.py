"""
Main entry point for UserInterviewAnalysisAgent
"""
import sys
import json
import logging
from agents.user_interview_agent import UserInterviewAnalysisAgent
from agents.config import get_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    logger.info("Starting UserInterviewAnalysisAgent")
    
    # Initialize agent
    config = get_config()
    agent = UserInterviewAnalysisAgent(config)
    
    # Define target profile for marketing leaders
    target_profile = {
        "title": ["VP of Marketing", "Marketing Director", "CMO", "Head of Marketing"],
        "company_size": "growth-stage B2B SaaS (50-500 employees)",
        "industry": "B2B SaaS",
        "responsibilities": [
            "Content strategy",
            "Lead generation",
            "Brand management",
            "Marketing operations"
        ],
        "pain_points": [
            "Content scaling",
            "Personalization",
            "Brand consistency",
            "Lead conversion"
        ]
    }
    
    # Optional interview template
    interview_template = """
    Introduction (5 min)
    - Thank you for your time
    - Overview of the interview purpose
    - Consent for recording
    
    Current State (10 min)
    - Content creation process
    - Team structure and resources
    - Tools and platforms used
    
    Pain Points (10 min)
    - Biggest challenges
    - Time and resource constraints
    - Personalization obstacles
    - Brand consistency issues
    
    Vision (5 min)
    - Ideal solution
    - Feature requests
    - Success metrics
    """
    
    # Execute the agent
    logger.info("Executing interview analysis workflow")
    results = agent.execute(target_profile, interview_template)
    
    # Display results
    if results['status'] == 'success':
        logger.info("="*80)
        logger.info("EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"\nPain Point Analysis: {results['pain_point_analysis_url']}")
        logger.info(f"Feature Wish List: {results['feature_wishlist_url']}")
        logger.info(f"GitHub Issue: {results['github_issue_url']}")
        logger.info(f"\nRecordings: {len(results['recording_urls'])} files")
        logger.info(f"Transcripts: {len(results['transcript_urls'])} files")
        logger.info("="*80)
        
        # Save results to file
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=2)
        logger.info("\nDetailed results saved to results.json")
        
        return 0
    else:
        logger.error("="*80)
        logger.error("EXECUTION FAILED")
        logger.error("="*80)
        logger.error(f"Error: {results.get('error', 'Unknown error')}")
        logger.error("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
