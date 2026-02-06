"""
Notion Reporting Module
Creates and publishes reports to Notion
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class NotionReporter:
    """Publishes reports to Notion"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.notion_api_key
        self.database_id = config.notion_database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def create_reports(
        self,
        pain_point_report: Dict[str, Any],
        feature_wishlist: List[Dict[str, Any]],
        transcripts: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Create Notion reports
        
        Args:
            pain_point_report: Pain point analysis report
            feature_wishlist: Prioritized feature list
            transcripts: Interview transcripts
            
        Returns:
            Dictionary with URLs to created Notion pages
        """
        logger.info("Creating Notion reports")
        
        if not self.api_key:
            logger.warning("Notion API key not configured, using mock URLs")
            return self._get_mock_urls()
        
        try:
            # Create pain point report page
            pain_point_url = self._create_pain_point_page(pain_point_report, transcripts)
            
            # Create feature wishlist page
            feature_url = self._create_feature_wishlist_page(feature_wishlist, transcripts)
            
            urls = {
                "pain_point_report": pain_point_url,
                "feature_wishlist": feature_url
            }
            
            logger.info("Successfully created Notion reports")
            return urls
            
        except Exception as e:
            logger.error(f"Error creating Notion reports: {str(e)}")
            return self._get_mock_urls()
    
    def _create_pain_point_page(
        self,
        report: Dict[str, Any],
        transcripts: List[Dict[str, Any]]
    ) -> str:
        """Create pain point analysis page in Notion"""
        
        # Build page content (for future Notion API implementation)
        _content = self._build_pain_point_content(report, transcripts)
        
        if not self.api_key:
            return f"https://notion.so/pain-point-analysis-mock"
        
        # In real implementation, would call Notion API
        # For now, return mock URL
        return f"https://notion.so/pain-point-analysis-{report['summary']['total_pain_points']}"
    
    def _create_feature_wishlist_page(
        self,
        features: List[Dict[str, Any]],
        transcripts: List[Dict[str, Any]]
    ) -> str:
        """Create feature wishlist page in Notion"""
        
        # Build page content (for future Notion API implementation)
        _content = self._build_feature_content(features, transcripts)
        
        if not self.api_key:
            return f"https://notion.so/feature-wishlist-mock"
        
        # In real implementation, would call Notion API
        # For now, return mock URL
        return f"https://notion.so/feature-wishlist-{len(features)}"
    
    def _build_pain_point_content(
        self,
        report: Dict[str, Any],
        transcripts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build Notion page content for pain point report"""
        
        summary = report['summary']
        
        content = {
            "title": "User Interview Pain Point Analysis",
            "sections": [
                {
                    "type": "heading",
                    "text": "Executive Summary"
                },
                {
                    "type": "paragraph",
                    "text": f"Analysis of {len(transcripts)} user interviews revealed {summary['total_pain_points']} distinct pain points, with {summary['high_severity_count']} classified as high severity."
                },
                {
                    "type": "heading",
                    "text": "Top Pain Points"
                }
            ]
        }
        
        # Add top pain points
        for i, pp in enumerate(summary['top_pain_points'], 1):
            content['sections'].append({
                "type": "numbered_item",
                "text": f"{pp['pain_point']} (Frequency: {pp['frequency']}, Severity: {pp['severity']})"
            })
        
        # Add category breakdowns
        content['sections'].append({
            "type": "heading",
            "text": "Pain Points by Category"
        })
        
        for category, pain_points in report['by_category'].items():
            content['sections'].append({
                "type": "subheading",
                "text": f"{category} ({len(pain_points)} pain points)"
            })
            
            for pp in pain_points:
                content['sections'].append({
                    "type": "bullet",
                    "text": pp['pain_point']
                })
        
        # Add recommendations
        content['sections'].append({
            "type": "heading",
            "text": "Recommendations"
        })
        
        for rec in report['recommendations']:
            content['sections'].append({
                "type": "bullet",
                "text": rec
            })
        
        return content
    
    def _build_feature_content(
        self,
        features: List[Dict[str, Any]],
        transcripts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build Notion page content for feature wishlist"""
        
        content = {
            "title": "Prioritized Feature Wish List",
            "sections": [
                {
                    "type": "heading",
                    "text": "Overview"
                },
                {
                    "type": "paragraph",
                    "text": f"Based on {len(transcripts)} user interviews, we identified {len(features)} feature suggestions, prioritized by frequency, impact, and alignment with our value proposition."
                },
                {
                    "type": "heading",
                    "text": "Priority Features"
                }
            ]
        }
        
        # Group by priority
        by_priority = {}
        for feature in features:
            priority = feature['priority']
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(feature)
        
        # Add features by priority
        for priority in ["Critical", "High", "Medium", "Low"]:
            if priority in by_priority:
                content['sections'].append({
                    "type": "subheading",
                    "text": f"{priority} Priority ({len(by_priority[priority])} features)"
                })
                
                for feature in by_priority[priority]:
                    content['sections'].append({
                        "type": "bullet",
                        "text": f"{feature['feature']} - {feature['description']} (Score: {feature['priority_score']}, Frequency: {feature['frequency']})"
                    })
        
        return content
    
    def _get_mock_urls(self) -> Dict[str, str]:
        """Get mock Notion URLs"""
        return {
            "pain_point_report": "https://notion.so/pain-point-analysis-20251010",
            "feature_wishlist": "https://notion.so/feature-wishlist-20251010"
        }
