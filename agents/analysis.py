"""
Pain Point Analysis Module
Performs NLP analysis on transcripts to identify pain points
"""
import logging
from typing import List, Dict, Any
from collections import Counter
from openai import OpenAI

logger = logging.getLogger(__name__)


class PainPointAnalyzer:
    """Analyzes interview transcripts to extract and categorize pain points"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def analyze_pain_points(self, transcripts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze transcripts to identify pain points
        
        Args:
            transcripts: List of interview transcripts
            
        Returns:
            List of identified pain points with metadata
        """
        logger.info(f"Analyzing {len(transcripts)} transcripts for pain points")
        
        all_pain_points = []
        
        for transcript in transcripts:
            pain_points = self._extract_pain_points(transcript)
            all_pain_points.extend(pain_points)
        
        # Aggregate and prioritize pain points
        aggregated = self._aggregate_pain_points(all_pain_points)
        
        logger.info(f"Identified {len(aggregated)} unique pain points")
        return aggregated
    
    def _extract_pain_points(self, transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract pain points from a single transcript"""
        
        if not self.client:
            return self._extract_mock_pain_points(transcript)
        
        try:
            # Use OpenAI to extract pain points
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing user interviews and extracting pain points. Identify specific pain points, challenges, and frustrations mentioned."},
                    {"role": "user", "content": f"Extract pain points from this interview transcript:\n\n{transcript['text']}\n\nList each pain point with its category and severity (high/medium/low)."}
                ],
                temperature=0.3
            )
            
            return self._parse_pain_points_response(response.choices[0].message.content, transcript)
            
        except Exception as e:
            logger.error(f"Error extracting pain points: {str(e)}")
            return self._extract_mock_pain_points(transcript)
    
    def _extract_mock_pain_points(self, transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract mock pain points based on keywords"""
        text = transcript['text'].lower()
        pain_points = []
        
        # Define pain point patterns
        patterns = {
            "Time-consuming content creation": ["time-consuming", "60-70% of their time", "hours"],
            "Scaling personalization": ["scaling", "personalize", "segments", "bottleneck"],
            "Brand consistency": ["consistency", "brand voice", "guidelines", "enforcing"],
            "Manual processes": ["manually", "manual intervention", "templates"],
            "Resource constraints": ["don't have the resources", "leaving little room"],
            "Attribution challenges": ["struggle to attribute", "analytics", "insights"]
        }
        
        for pain_point, keywords in patterns.items():
            if any(keyword in text for keyword in keywords):
                pain_points.append({
                    "pain_point": pain_point,
                    "category": self._categorize_pain_point(pain_point),
                    "severity": self._assess_severity(text, keywords),
                    "participant": transcript['participant'],
                    "transcript_id": transcript['id'],
                    "quotes": self._extract_quotes(transcript['text'], keywords)
                })
        
        return pain_points
    
    def _categorize_pain_point(self, pain_point: str) -> str:
        """Categorize a pain point"""
        categories = {
            "content": ["content", "creation", "generation"],
            "personalization": ["personalization", "personalize", "segments"],
            "brand": ["brand", "consistency", "voice"],
            "process": ["manual", "process", "workflow"],
            "resources": ["resource", "time", "team"],
            "analytics": ["attribution", "analytics", "metrics", "insights"]
        }
        
        pain_point_lower = pain_point.lower()
        for category, keywords in categories.items():
            if any(keyword in pain_point_lower for keyword in keywords):
                return category.capitalize()
        
        return "General"
    
    def _assess_severity(self, text: str, keywords: List[str]) -> str:
        """Assess severity based on language intensity"""
        high_intensity = ["biggest", "critical", "major", "impossible", "extremely"]
        medium_intensity = ["challenging", "difficult", "problem", "issue"]
        
        if any(word in text for word in high_intensity):
            return "high"
        elif any(word in text for word in medium_intensity):
            return "medium"
        return "low"
    
    def _extract_quotes(self, text: str, keywords: List[str]) -> List[str]:
        """Extract relevant quotes containing keywords"""
        sentences = text.split('.')
        quotes = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                quote = sentence.strip()
                if len(quote) > 20:  # Only meaningful quotes
                    quotes.append(quote[:200])  # Limit quote length
        
        return quotes[:2]  # Return top 2 quotes
    
    def _aggregate_pain_points(self, pain_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate and prioritize pain points"""
        # Group by pain point text
        grouped = {}
        
        for pp in pain_points:
            key = pp['pain_point']
            if key not in grouped:
                grouped[key] = {
                    "pain_point": pp['pain_point'],
                    "category": pp['category'],
                    "severity": pp['severity'],
                    "frequency": 0,
                    "participants": [],
                    "quotes": []
                }
            
            grouped[key]['frequency'] += 1
            grouped[key]['participants'].append(pp['participant']['name'])
            grouped[key]['quotes'].extend(pp.get('quotes', []))
        
        # Sort by frequency and severity
        aggregated = sorted(
            grouped.values(),
            key=lambda x: (x['frequency'], {'high': 3, 'medium': 2, 'low': 1}[x['severity']]),
            reverse=True
        )
        
        return aggregated
    
    def _parse_pain_points_response(self, response: str, transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse OpenAI response into structured pain points"""
        # This would parse the AI response
        # For now, fall back to mock extraction
        return self._extract_mock_pain_points(transcript)
    
    def create_report(self, pain_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a comprehensive pain point analysis report
        
        Args:
            pain_points: List of aggregated pain points
            
        Returns:
            Report data structure
        """
        logger.info("Creating pain point analysis report")
        
        # Group by category
        by_category = {}
        for pp in pain_points:
            category = pp['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(pp)
        
        # Calculate summary statistics
        total_pain_points = len(pain_points)
        high_severity_count = sum(1 for pp in pain_points if pp['severity'] == 'high')
        
        report = {
            "title": "Detailed Pain Point Analysis Report",
            "summary": {
                "total_pain_points": total_pain_points,
                "high_severity_count": high_severity_count,
                "categories": list(by_category.keys()),
                "top_pain_points": pain_points[:5]
            },
            "by_category": by_category,
            "pain_points": pain_points,
            "recommendations": self._generate_recommendations(pain_points)
        }
        
        logger.info("Pain point analysis report created")
        return report
    
    def _generate_recommendations(self, pain_points: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on pain points"""
        recommendations = []
        
        # High-frequency pain points
        high_freq = [pp for pp in pain_points if pp['frequency'] >= 3]
        if high_freq:
            recommendations.append(f"Address the {len(high_freq)} most frequently mentioned pain points first")
        
        # High-severity pain points
        high_sev = [pp for pp in pain_points if pp['severity'] == 'high']
        if high_sev:
            recommendations.append(f"Prioritize {len(high_sev)} high-severity issues for immediate action")
        
        # Category-specific recommendations
        categories = set(pp['category'] for pp in pain_points)
        for category in categories:
            count = sum(1 for pp in pain_points if pp['category'] == category)
            recommendations.append(f"Focus on {category} improvements ({count} related pain points)")
        
        return recommendations
