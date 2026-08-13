"""
User Recruitment Module
Builds simulated interview participant cohorts
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class UserRecruitment:
    """Manages user recruitment for interviews"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.usertesting_api_key
        self.base_url = "https://api.usertesting.com/v1"
    
    def recruit_participants(
        self, 
        target_profile: Dict[str, Any], 
        target_count: int
    ) -> List[Dict[str, Any]]:
        """
        Recruit participants matching the target profile
        
        Args:
            target_profile: Criteria for target participants
            target_count: Number of participants to recruit
            
        Returns:
            List of recruited participants
        """
        logger.info(f"Recruiting {target_count} participants")
        
        if self.api_key:
            logger.info(
                "UserTesting API key detected, but live recruitment is not implemented; "
                "using simulated participants"
            )
        else:
            logger.warning("UserTesting API key not configured, using simulated participants")

        participants = self._simulate_recruitment(target_profile, target_count)
        logger.info(f"Successfully recruited {len(participants)} participants")
        return participants
    
    def _simulate_recruitment(self, target_profile: Dict[str, Any], target_count: int) -> List[Dict[str, Any]]:
        """Simulate participant recruitment"""
        participants = []
        for i in range(target_count):
            participants.append({
                "id": f"participant_{i+1}",
                "name": f"Marketing Leader {i+1}",
                "email": f"leader{i+1}@example.com",
                "company": f"Company {chr(65+i%26)}",
                "title": "VP of Marketing" if i % 3 == 0 else "Marketing Director" if i % 3 == 1 else "CMO",
                "profile": target_profile,
                "recruited_date": "2025-10-10"
            })
        return participants
    
    def _get_mock_participants(self, count: int) -> List[Dict[str, Any]]:
        """Get mock participants for testing"""
        return self._simulate_recruitment({}, count)
