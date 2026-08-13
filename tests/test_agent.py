"""
Tests for UserInterviewAnalysisAgent
"""
import unittest
from unittest.mock import Mock, patch
from agents.user_interview_agent import UserInterviewAnalysisAgent
from agents.config import AgentConfig


class TestUserInterviewAnalysisAgent(unittest.TestCase):
    """Test cases for UserInterviewAnalysisAgent"""
    
    def setUp(self):
        """Set up test configuration with empty credentials for mock testing"""
        self.config = AgentConfig(
            openai_api_key="",
            zoom_client_id="",
            zoom_client_secret="",
            zoom_account_id="",
            usertesting_api_key="",
            notion_api_key="",
            notion_database_id="",
            github_token=""
        )
        self.agent = UserInterviewAnalysisAgent(self.config)
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.config.target_interview_count, 20)
        self.assertEqual(self.agent.config.interview_duration_minutes, 30)
    
    def test_parse_context(self):
        """Test context parsing"""
        target_profile = {
            "title": ["VP of Marketing"],
            "industry": "B2B SaaS"
        }
        context = self.agent._parse_context(target_profile)
        
        self.assertIn("value_proposition", context)
        self.assertIn("target_profile", context)
        self.assertIn("objectives", context)
        self.assertEqual(len(context["objectives"]), 4)
    
    def test_execute_workflow(self):
        """Test complete workflow execution"""
        target_profile = {
            "title": ["VP of Marketing", "Marketing Director"],
            "company_size": "50-500 employees",
            "industry": "B2B SaaS"
        }
        
        results = self.agent.execute(target_profile)
        
        # Verify successful execution
        self.assertEqual(results["status"], "success")
        
        # Verify all outputs are present
        self.assertIn("pain_point_analysis_url", results)
        self.assertIn("feature_wishlist_url", results)
        self.assertIn("github_issue_url", results)
        self.assertIn("recording_urls", results)
        self.assertIn("transcript_urls", results)
        self.assertIn("pain_points", results)
        self.assertIn("feature_wishlist", results)
        
        # Verify expected counts
        self.assertEqual(len(results["recording_urls"]), 20)
        self.assertEqual(len(results["transcript_urls"]), 20)
        
        # Verify execution log
        self.assertIn("execution_log", results)
        self.assertEqual(len(results["execution_log"]), 24)  # 12 steps * 2 (start/complete)
    
    def test_execute_resets_execution_log_between_runs(self):
        """Test execution log is reset for each run"""
        target_profile = {"title": ["VP of Marketing"], "industry": "B2B SaaS"}
        
        first_results = self.agent.execute(target_profile)
        second_results = self.agent.execute(target_profile)
        
        self.assertEqual(first_results["status"], "success")
        self.assertEqual(second_results["status"], "success")
        self.assertEqual(len(first_results["execution_log"]), 24)
        self.assertEqual(len(second_results["execution_log"]), 24)
    
    @patch("agents.github_integration.requests.post")
    def test_execute_returns_error_when_github_issue_creation_fails(self, mock_post):
        """Test execute surfaces GitHub issue creation failures"""
        mock_post.return_value = Mock(status_code=500, text="server error")
        
        config = AgentConfig(
            openai_api_key="",
            zoom_client_id="",
            zoom_client_secret="",
            zoom_account_id="",
            usertesting_api_key="",
            notion_api_key="",
            notion_database_id="",
            github_token="test-token"
        )
        agent = UserInterviewAnalysisAgent(config)
        
        results = agent.execute({"title": ["VP of Marketing"], "industry": "B2B SaaS"})
        
        self.assertEqual(results["status"], "error")
        self.assertIsNone(results["github_issue_url"])
    
    def test_construct_issue_content(self):
        """Test GitHub issue content construction"""
        results = {
            "notion_urls": {
                "pain_point_report": "https://notion.so/test1",
                "feature_wishlist": "https://notion.so/test2"
            },
            "recordings": [{"id": "1"}] * 20,
            "transcripts": [{"id": "1"}] * 20,
            "pain_points": [{"pain_point": "test"}] * 5,
            "feature_wishlist": [{"feature": "test"}] * 8,
            "participants": [{"id": "1"}] * 20
        }
        
        issue_content = self.agent._construct_issue_content(results)
        
        self.assertIn("title", issue_content)
        self.assertIn("body", issue_content)
        self.assertIn("User Interview Analysis", issue_content["title"])
        self.assertIn("notion.so/test1", issue_content["body"])
        self.assertIn("notion.so/test2", issue_content["body"])


class TestInterviewQuestionGenerator(unittest.TestCase):
    """Test interview question generation"""
    
    def setUp(self):
        """Set up test configuration"""
        from agents.interview_generator import InterviewQuestionGenerator
        self.config = AgentConfig(openai_api_key="")
        self.generator = InterviewQuestionGenerator(self.config)
    
    def test_default_questions(self):
        """Test default question generation"""
        questions = self.generator._get_default_questions()
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 10)
        
        # Verify question structure
        for q in questions:
            self.assertIn("category", q)
            self.assertIn("question", q)
    
    def test_question_categories(self):
        """Test that questions cover all key categories"""
        questions = self.generator._get_default_questions()
        categories = set(q["category"] for q in questions)
        
        expected_categories = {
            "Content Generation",
            "Personalization",
            "Brand Alignment",
            "Lead Conversion",
            "Pain Points",
            "Vision"
        }
        
        self.assertTrue(expected_categories.issubset(categories))


class TestPainPointAnalyzer(unittest.TestCase):
    """Test pain point analysis"""
    
    def setUp(self):
        """Set up test configuration"""
        from agents.analysis import PainPointAnalyzer
        self.config = AgentConfig(openai_api_key="")
        self.analyzer = PainPointAnalyzer(self.config)
    
    def test_categorize_pain_point(self):
        """Test pain point categorization"""
        self.assertEqual(
            self.analyzer._categorize_pain_point("Content generation issues"),
            "Content"
        )
        self.assertEqual(
            self.analyzer._categorize_pain_point("Brand consistency problems"),
            "Brand"
        )
        self.assertEqual(
            self.analyzer._categorize_pain_point("Manual process workflow"),
            "Process"
        )
    
    def test_assess_severity(self):
        """Test severity assessment"""
        high_text = "This is our biggest challenge and critical issue"
        medium_text = "This is a challenging problem we face"
        
        self.assertEqual(
            self.analyzer._assess_severity(high_text, ["challenge"]),
            "high"
        )
        self.assertEqual(
            self.analyzer._assess_severity(medium_text, ["challenging"]),
            "medium"
        )


class TestFeatureWishListGenerator(unittest.TestCase):
    """Test feature wish list generation"""
    
    def setUp(self):
        """Set up test configuration"""
        from agents.feature_extractor import FeatureWishListGenerator
        self.config = AgentConfig(openai_api_key="")
        self.generator = FeatureWishListGenerator(self.config)
    
    def test_categorize_feature(self):
        """Test feature categorization"""
        self.assertEqual(
            self.generator._categorize_feature("Automated content generation"),
            "Content Generation"
        )
        self.assertEqual(
            self.generator._categorize_feature("AI-powered personalization"),
            "Personalization"
        )
        self.assertEqual(
            self.generator._categorize_feature("Content analytics dashboard"),
            "Analytics"
        )
    
    def test_score_to_priority(self):
        """Test priority scoring"""
        self.assertEqual(self.generator._convert_score_to_priority_level(80), "Critical")
        self.assertEqual(self.generator._convert_score_to_priority_level(60), "High")
        self.assertEqual(self.generator._convert_score_to_priority_level(40), "Medium")
        self.assertEqual(self.generator._convert_score_to_priority_level(20), "Low")
    
    def test_extract_mock_features_marks_keyword_matches_as_explicit(self):
        """Test keyword matches count as explicit mentions in mock extraction"""
        transcript = {
            "id": "transcript_1",
            "participant": {"name": "Test User"},
            "text": "We need to generate better content at scale for every audience."
        }
        
        features = self.generator._extract_mock_features(transcript, [])
        extracted = next(
            feature for feature in features
            if feature["feature"] == "Automated content generation at scale"
        )
        
        self.assertTrue(extracted["mentioned_explicitly"])


if __name__ == "__main__":
    unittest.main()
