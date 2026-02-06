"""
UserInterviewAnalysisAgent - Main agent implementation
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from .config import AgentConfig, get_config
from .interview_generator import InterviewQuestionGenerator
from .recruitment import UserRecruitment
from .scheduling import InterviewScheduler
from .transcription import TranscriptionService
from .analysis import PainPointAnalyzer
from .feature_extractor import FeatureWishListGenerator
from .reporting import NotionReporter
from .github_integration import GitHubIssueCreator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserInterviewAnalysisAgent:
    """
    Agent for conducting user interviews, analyzing pain points, 
    and generating prioritized feature wish lists.
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the agent with configuration"""
        self.config = config or get_config()
        self.execution_log: List[Dict[str, Any]] = []
        
        # Initialize components
        self.question_generator = InterviewQuestionGenerator(self.config)
        self.recruitment = UserRecruitment(self.config)
        self.scheduler = InterviewScheduler(self.config)
        self.transcription = TranscriptionService(self.config)
        self.analyzer = PainPointAnalyzer(self.config)
        self.feature_generator = FeatureWishListGenerator(self.config)
        self.notion_reporter = NotionReporter(self.config)
        self.github_creator = GitHubIssueCreator(self.config)
        
        logger.info("UserInterviewAnalysisAgent initialized")
    
    def _log_step(self, step_number: int, description: str, status: str = "started", data: Optional[Dict] = None):
        """Log execution step"""
        log_entry = {
            "step": step_number,
            "description": description,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data or {}
        }
        self.execution_log.append(log_entry)
        logger.info(f"Step {step_number}: {description} - {status}")
    
    def execute(self, target_profile: Dict[str, Any], interview_template: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the complete user interview analysis workflow
        
        Args:
            target_profile: Criteria for target marketing leaders
            interview_template: Optional template for interview questions
            
        Returns:
            Dictionary containing URLs to outputs and execution summary
        """
        logger.info("Starting UserInterviewAnalysisAgent execution")
        results = {}
        
        try:
            # Step 1: Parse value proposition and target profile
            self._log_step(1, "Parse value proposition and target profile")
            context = self._parse_context(target_profile)
            self._log_step(1, "Parse value proposition and target profile", "completed", context)
            
            # Step 2: Generate interview questions
            self._log_step(2, "Generate interview questions")
            questions = self.question_generator.generate_questions(
                self.config.value_proposition,
                target_profile,
                interview_template
            )
            results["interview_questions"] = questions
            self._log_step(2, "Generate interview questions", "completed", {"question_count": len(questions)})
            
            # Step 3: Recruit participants
            self._log_step(3, "Recruit target marketing leaders")
            participants = self.recruitment.recruit_participants(
                target_profile,
                self.config.target_interview_count
            )
            results["participants"] = participants
            self._log_step(3, "Recruit target marketing leaders", "completed", {"participant_count": len(participants)})
            
            # Step 4: Schedule interviews
            self._log_step(4, "Schedule interview sessions")
            scheduled_interviews = self.scheduler.schedule_interviews(
                participants,
                self.config.interview_duration_minutes
            )
            results["scheduled_interviews"] = scheduled_interviews
            self._log_step(4, "Schedule interview sessions", "completed", {"scheduled_count": len(scheduled_interviews)})
            
            # Step 5: Conduct and record interviews
            self._log_step(5, "Facilitate and record interview sessions")
            recordings = self.scheduler.conduct_interviews(scheduled_interviews)
            results["recordings"] = recordings
            self._log_step(5, "Facilitate and record interview sessions", "completed", {"recording_count": len(recordings)})
            
            # Step 6: Transcribe interviews
            self._log_step(6, "Transcribe recorded interviews")
            transcripts = self.transcription.transcribe_all(recordings)
            results["transcripts"] = transcripts
            self._log_step(6, "Transcribe recorded interviews", "completed", {"transcript_count": len(transcripts)})
            
            # Step 7: Analyze pain points
            self._log_step(7, "Perform NLP analysis on transcripts")
            pain_points = self.analyzer.analyze_pain_points(transcripts)
            results["pain_points"] = pain_points
            self._log_step(7, "Perform NLP analysis on transcripts", "completed", {"pain_point_count": len(pain_points)})
            
            # Step 8: Synthesize pain point report
            self._log_step(8, "Synthesize detailed pain point analysis report")
            pain_point_report = self.analyzer.create_report(pain_points)
            results["pain_point_report"] = pain_point_report
            self._log_step(8, "Synthesize detailed pain point analysis report", "completed")
            
            # Step 9: Extract and prioritize features
            self._log_step(9, "Extract and prioritize feature suggestions")
            feature_wishlist = self.feature_generator.generate_wishlist(
                transcripts,
                pain_points,
                self.config.value_proposition
            )
            results["feature_wishlist"] = feature_wishlist
            self._log_step(9, "Extract and prioritize feature suggestions", "completed", {"feature_count": len(feature_wishlist)})
            
            # Step 10: Create Notion reports
            self._log_step(10, "Create Notion reports")
            notion_urls = self.notion_reporter.create_reports(
                pain_point_report,
                feature_wishlist,
                transcripts
            )
            results["notion_urls"] = notion_urls
            self._log_step(10, "Create Notion reports", "completed", notion_urls)
            
            # Step 11: Construct GitHub issue content
            self._log_step(11, "Construct GitHub issue")
            issue_content = self._construct_issue_content(results)
            self._log_step(11, "Construct GitHub issue", "completed")
            
            # Step 12: Create GitHub issue
            self._log_step(12, "Create GitHub issue")
            github_issue_url = self.github_creator.create_issue(issue_content)
            results["github_issue_url"] = github_issue_url
            self._log_step(12, "Create GitHub issue", "completed", {"issue_url": github_issue_url})
            
            logger.info("UserInterviewAnalysisAgent execution completed successfully")
            
            return {
                "status": "success",
                "pain_point_analysis_url": notion_urls.get("pain_point_report"),
                "feature_wishlist_url": notion_urls.get("feature_wishlist"),
                "recording_urls": [r.get("recording_url") for r in recordings],
                "transcript_urls": [t.get("url") for t in transcripts],
                "github_issue_url": github_issue_url,
                "execution_log": self.execution_log
            }
            
        except Exception as e:
            # Log detailed error internally while sanitizing external error messages
            logger.error("Error during execution", exc_info=True)
            return {
                "status": "error",
                "error": "An error occurred during execution. Check logs for details.",
                "pain_point_analysis_url": None,
                "feature_wishlist_url": None,
                "recording_urls": [],
                "transcript_urls": [],
                "github_issue_url": None,
                "execution_log": self.execution_log
            }
    
    def _parse_context(self, target_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Parse value proposition and target profile"""
        return {
            "value_proposition": self.config.value_proposition,
            "target_profile": target_profile,
            "objectives": [
                "Uncover pain points in content generation",
                "Identify personalization challenges",
                "Understand brand alignment issues",
                "Discover lead conversion bottlenecks"
            ]
        }
    
    def _construct_issue_content(self, results: Dict[str, Any]) -> Dict[str, str]:
        """Construct GitHub issue content"""
        return {
            "title": "User Interview Analysis Complete - Feature Insights",
            "body": f"""# User Interview Analysis Results

## Goal
Conduct user interviews with target marketing leaders, analyze their pain points, and generate a prioritized feature wish list.

## Inputs Processed
- PersonaScript Value Proposition
- Target Marketing Leader Profile/Criteria
- Interview Script Template
- Access Credentials (Zoom, Notion, UserTesting.com)

## Outputs Generated

### Reports
- **Pain Point Analysis Report**: {results.get('notion_urls', {}).get('pain_point_report', 'N/A')}
- **Prioritized Feature Wish List**: {results.get('notion_urls', {}).get('feature_wishlist', 'N/A')}

### Interview Artifacts
- **Recordings**: {len(results.get('recordings', []))} sessions recorded
- **Transcripts**: {len(results.get('transcripts', []))} transcripts generated

### Key Findings
- **Pain Points Identified**: {len(results.get('pain_points', []))}
- **Feature Suggestions**: {len(results.get('feature_wishlist', []))}
- **Participants Interviewed**: {len(results.get('participants', []))}

## Execution Summary
The agent completed all 12 steps of the workflow successfully:
1. ✅ Parsed value proposition and target profile
2. ✅ Generated comprehensive interview questions
3. ✅ Recruited {self.config.target_interview_count}+ marketing leaders
4. ✅ Scheduled individual interview sessions
5. ✅ Facilitated and recorded interviews
6. ✅ Transcribed all recordings
7. ✅ Performed NLP analysis
8. ✅ Synthesized pain point report
9. ✅ Extracted and prioritized features
10. ✅ Created Notion reports
11. ✅ Constructed issue content
12. ✅ Created this GitHub issue

## Next Steps
- Review the detailed reports in Notion
- Prioritize features for the product roadmap
- Schedule follow-up sessions with key participants
- Begin implementation planning for top-priority features
"""
        }
