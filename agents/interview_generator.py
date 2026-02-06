"""
Interview Question Generator Module
Generates comprehensive interview questions using OpenAI
"""
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)


class InterviewQuestionGenerator:
    """Generates interview questions for user research"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def generate_questions(
        self, 
        value_proposition: str, 
        target_profile: Dict[str, Any],
        template: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate interview questions based on value proposition and target profile
        
        Args:
            value_proposition: Company value proposition
            target_profile: Target audience profile
            template: Optional interview template
            
        Returns:
            List of interview questions with categories
        """
        logger.info("Generating interview questions")
        
        if not self.client:
            logger.warning("OpenAI client not configured, using default questions")
            return self._get_default_questions()
        
        try:
            prompt = self._build_prompt(value_proposition, target_profile, template)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert user researcher who creates insightful interview questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            questions_text = response.choices[0].message.content
            questions = self._parse_questions(questions_text)
            
            logger.info(f"Generated {len(questions)} interview questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return self._get_default_questions()
    
    def _build_prompt(self, value_proposition: str, target_profile: Dict[str, Any], template: Optional[str]) -> str:
        """Build the prompt for question generation"""
        prompt = f"""Generate a comprehensive set of interview questions for user research.

Value Proposition: {value_proposition}

Target Profile: {target_profile}

{'Template: ' + template if template else ''}

Focus areas:
1. Content generation pain points
2. Personalization challenges
3. Brand alignment issues
4. Lead conversion bottlenecks

Generate 15-20 open-ended questions organized by category. Format as:
Category: [Category Name]
- Question 1
- Question 2
...
"""
        return prompt
    
    def _parse_questions(self, questions_text: str) -> List[Dict[str, str]]:
        """Parse generated questions into structured format"""
        questions = []
        current_category = "General"
        
        for line in questions_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Category:') or line.endswith(':'):
                current_category = line.replace('Category:', '').replace(':', '').strip()
            elif line.startswith('-') or line.startswith('•') or line[0].isdigit():
                question_text = line.lstrip('-•0123456789. ').strip()
                if question_text:
                    questions.append({
                        "category": current_category,
                        "question": question_text
                    })
        
        return questions
    
    def _get_default_questions(self) -> List[Dict[str, str]]:
        """Return default interview questions"""
        return [
            {"category": "Content Generation", "question": "What are your biggest challenges in creating content for your sales funnel?"},
            {"category": "Content Generation", "question": "How much time does your team spend on content creation weekly?"},
            {"category": "Content Generation", "question": "What tools or processes do you currently use for content generation?"},
            {"category": "Personalization", "question": "How do you currently personalize content for different audience segments?"},
            {"category": "Personalization", "question": "What obstacles prevent you from creating more personalized content?"},
            {"category": "Personalization", "question": "How do you measure the effectiveness of personalized content?"},
            {"category": "Brand Alignment", "question": "How do you ensure brand consistency across all content?"},
            {"category": "Brand Alignment", "question": "What challenges do you face maintaining brand voice at scale?"},
            {"category": "Brand Alignment", "question": "Do you have brand guidelines? How well are they followed?"},
            {"category": "Lead Conversion", "question": "What content types drive the most conversions for you?"},
            {"category": "Lead Conversion", "question": "Where do prospects typically drop off in your sales funnel?"},
            {"category": "Lead Conversion", "question": "How do you track content's impact on lead conversion?"},
            {"category": "Pain Points", "question": "What's the most frustrating aspect of your current content workflow?"},
            {"category": "Pain Points", "question": "If you could wave a magic wand, what would you fix first?"},
            {"category": "Vision", "question": "What would ideal content operations look like for your team?"},
            {"category": "Vision", "question": "What features or capabilities would transform how you work?"}
        ]
