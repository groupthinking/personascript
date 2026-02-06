"""
Feature Wish List Generator Module
Extracts and prioritizes feature suggestions from interviews
"""
import logging
from typing import List, Dict, Any
from openai import OpenAI

logger = logging.getLogger(__name__)


class FeatureWishListGenerator:
    """Generates and prioritizes feature wish list from interviews"""
    
    # Scoring weights (must sum to 100)
    FREQUENCY_MAX_SCORE = 40  # Maximum points for frequency of mention
    EXPLICIT_MENTION_MAX_SCORE = 20  # Maximum points for explicit mentions
    ALIGNMENT_MAX_SCORE = 40  # Maximum points for value proposition alignment
    
    # Priority thresholds
    PRIORITY_CRITICAL_THRESHOLD = 70  # Score >= 70 is Critical priority
    PRIORITY_HIGH_THRESHOLD = 50  # Score >= 50 is High priority
    PRIORITY_MEDIUM_THRESHOLD = 30  # Score >= 30 is Medium priority
    # Score < 30 is Low priority
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def generate_wishlist(
        self,
        transcripts: List[Dict[str, Any]],
        pain_points: List[Dict[str, Any]],
        value_proposition: str
    ) -> List[Dict[str, Any]]:
        """
        Generate prioritized feature wish list
        
        Args:
            transcripts: Interview transcripts
            pain_points: Identified pain points
            value_proposition: Company value proposition
            
        Returns:
            Prioritized list of feature suggestions
        """
        logger.info("Generating feature wish list")
        
        # Extract features from transcripts
        features = []
        for transcript in transcripts:
            extracted = self._extract_features(transcript, pain_points)
            features.extend(extracted)
        
        # Deduplicate and aggregate
        aggregated = self._aggregate_features(features)
        
        # Prioritize based on criteria
        prioritized = self._prioritize_features(aggregated, value_proposition)
        
        logger.info(f"Generated {len(prioritized)} prioritized features")
        return prioritized
    
    def _extract_features(
        self,
        transcript: Dict[str, Any],
        pain_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract feature suggestions from transcript"""
        
        if not self.client:
            return self._extract_mock_features(transcript, pain_points)
        
        try:
            # Use OpenAI to extract features
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at extracting feature suggestions from user interviews. Identify explicit and implicit feature requests."},
                    {"role": "user", "content": f"Extract feature suggestions from this interview:\n\n{transcript['text']}\n\nList each feature with a brief description."}
                ],
                temperature=0.3
            )
            
            return self._parse_features_response(response.choices[0].message.content, transcript)
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return self._extract_mock_features(transcript, pain_points)
    
    def _extract_mock_features(
        self,
        transcript: Dict[str, Any],
        pain_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract mock features based on patterns"""
        text = transcript['text'].lower()
        features = []
        
        feature_patterns = {
            "Automated content generation at scale": [
                "generate", "automatic", "scale", "high-quality"
            ],
            "AI-powered personalization engine": [
                "personalize", "segments", "audience", "adapt"
            ],
            "Brand voice consistency checker": [
                "brand voice", "consistency", "guidelines", "on-brand"
            ],
            "Content template library": [
                "templates", "reusable", "library"
            ],
            "Advanced content analytics": [
                "analytics", "insights", "measure", "track", "attribute"
            ],
            "Multi-channel content distribution": [
                "channels", "distribute", "publish"
            ],
            "Collaborative content workflow": [
                "team", "collaborate", "workflow", "approval"
            ],
            "Real-time content optimization": [
                "optimize", "improve", "performance"
            ]
        }
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in text for keyword in keywords):
                features.append({
                    "feature": feature,
                    "description": self._generate_description(feature),
                    "category": self._categorize_feature(feature),
                    "source": transcript['participant']['name'],
                    "transcript_id": transcript['id'],
                    "mentioned_explicitly": any(f'"{keyword}"' in text for keyword in keywords)
                })
        
        return features
    
    def _generate_description(self, feature: str) -> str:
        """Generate feature description"""
        descriptions = {
            "Automated content generation at scale": "System that automatically generates high-quality, on-brand content at scale without manual intervention",
            "AI-powered personalization engine": "Intelligent engine that personalizes content for different audience segments automatically",
            "Brand voice consistency checker": "Tool that ensures all content maintains consistent brand voice and adheres to guidelines",
            "Content template library": "Comprehensive library of reusable, customizable content templates",
            "Advanced content analytics": "Deep analytics and attribution system to measure content effectiveness and ROI",
            "Multi-channel content distribution": "Unified system to distribute content across multiple marketing channels",
            "Collaborative content workflow": "Workflow system for team collaboration, reviews, and approvals",
            "Real-time content optimization": "System that optimizes content in real-time based on performance data"
        }
        return descriptions.get(feature, "Feature to improve content operations")
    
    def _categorize_feature(self, feature: str) -> str:
        """Categorize feature"""
        if "generat" in feature.lower() or "creat" in feature.lower():
            return "Content Generation"
        elif "personal" in feature.lower():
            return "Personalization"
        elif "brand" in feature.lower():
            return "Brand Management"
        elif "analytic" in feature.lower() or "measure" in feature.lower():
            return "Analytics"
        elif "workflow" in feature.lower() or "collaborat" in feature.lower():
            return "Workflow"
        return "General"
    
    def _aggregate_features(self, features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate and deduplicate features"""
        grouped = {}
        
        for feature in features:
            key = feature['feature']
            if key not in grouped:
                grouped[key] = {
                    "feature": feature['feature'],
                    "description": feature['description'],
                    "category": feature['category'],
                    "frequency": 0,
                    "sources": [],
                    "explicit_mentions": 0
                }
            
            grouped[key]['frequency'] += 1
            grouped[key]['sources'].append(feature['source'])
            if feature.get('mentioned_explicitly'):
                grouped[key]['explicit_mentions'] += 1
        
        return list(grouped.values())
    
    def _prioritize_features(
        self,
        features: List[Dict[str, Any]],
        value_proposition: str
    ) -> List[Dict[str, Any]]:
        """Prioritize features based on multiple criteria"""
        
        # Score each feature
        for feature in features:
            score = 0
            
            # Frequency score (0-40 points)
            score += min(feature['frequency'] * 4, self.FREQUENCY_MAX_SCORE)
            
            # Explicit mention bonus (0-20 points)
            score += min(feature['explicit_mentions'] * 5, self.EXPLICIT_MENTION_MAX_SCORE)
            
            # Alignment with value proposition (0-40 points)
            alignment = self._calculate_alignment(feature, value_proposition)
            score += alignment
            
            feature['priority_score'] = score
            feature['priority'] = self._convert_score_to_priority_level(score)
        
        # Sort by priority score
        prioritized = sorted(features, key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized
    
    def _calculate_alignment(self, feature: Dict[str, Any], value_proposition: str) -> int:
        """Calculate how well feature aligns with value proposition"""
        vp_lower = value_proposition.lower()
        feature_lower = (feature['feature'] + ' ' + feature['description']).lower()
        
        # Key value proposition themes
        themes = {
            "personalization": ["personalized", "hyper-personalized"],
            "scale": ["scale", "high-volume", "rapid"],
            "brand": ["brand-aligned", "brand consistency"],
            "conversion": ["conversion", "lead"]
        }
        
        score = 0
        for theme, keywords in themes.items():
            if any(kw in vp_lower for kw in keywords) and any(kw in feature_lower for kw in keywords):
                score += 10
        
        return min(score, self.ALIGNMENT_MAX_SCORE)
    
    def _convert_score_to_priority_level(self, score: int) -> str:
        """Convert numeric score to priority label"""
        if score >= self.PRIORITY_CRITICAL_THRESHOLD:
            return "Critical"
        elif score >= self.PRIORITY_HIGH_THRESHOLD:
            return "High"
        elif score >= self.PRIORITY_MEDIUM_THRESHOLD:
            return "Medium"
        return "Low"
    
    def _parse_features_response(self, response: str, transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse OpenAI response into structured features"""
        # This would parse the AI response
        # For now, fall back to mock extraction
        return self._extract_mock_features(transcript, [])
