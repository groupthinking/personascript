"""
Interview Scheduling Module
Simulates interview scheduling and recording with Zoom-shaped metadata
"""
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class InterviewScheduler:
    """Manages simulated interview scheduling and recording"""
    
    def __init__(self, config):
        self.config = config
        self.client_id = config.zoom_client_id
        self.client_secret = config.zoom_client_secret
        self.account_id = config.zoom_account_id
        self.access_token = None
    
    def schedule_interviews(
        self, 
        participants: List[Dict[str, Any]], 
        duration_minutes: int
    ) -> List[Dict[str, Any]]:
        """
        Schedule interviews with participants
        
        Args:
            participants: List of recruited participants
            duration_minutes: Duration of each interview
            
        Returns:
            List of scheduled interviews
        """
        logger.info(f"Scheduling {len(participants)} interviews")
        
        if self._has_credentials():
            logger.info(
                "Zoom credentials detected, but live Zoom scheduling is not implemented; "
                "using simulated schedule"
            )
        else:
            logger.warning("Zoom credentials not configured, using simulated scheduling")

        scheduled = self._mock_schedule(participants, duration_minutes)
        logger.info(f"Scheduled {len(scheduled)} interviews")
        return scheduled
    
    def conduct_interviews(self, scheduled_interviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Conduct and record interviews
        
        Args:
            scheduled_interviews: List of scheduled interviews
            
        Returns:
            List of recording information
        """
        logger.info(f"Recording {len(scheduled_interviews)} interviews")
        
        recordings = []
        for interview in scheduled_interviews:
            recording = {
                "id": f"recording_{interview['id']}",
                "interview_id": interview['id'],
                "participant": interview['participant'],
                "recording_url": f"https://zoom.us/rec/mock/{interview['id']}",
                "file_path": f"/recordings/{interview['id']}.mp4",
                "duration_seconds": interview['duration_minutes'] * 60,
                "recorded_date": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            recordings.append(recording)
        
        logger.info(f"Completed {len(recordings)} interview recordings")
        return recordings
    
    def _has_credentials(self) -> bool:
        """Check if Zoom credentials are configured"""
        return bool(self.client_id and self.client_secret and self.account_id)
    
    def _mock_schedule(self, participants: List[Dict[str, Any]], duration: int) -> List[Dict[str, Any]]:
        """Mock interview scheduling"""
        scheduled = []
        start_time = datetime.utcnow() + timedelta(days=1)
        
        for i, participant in enumerate(participants):
            interview_time = start_time + timedelta(hours=i)
            
            interview = {
                "id": f"interview_{i+1}",
                "participant": participant,
                "scheduled_time": interview_time.isoformat(),
                "duration_minutes": duration,
                "zoom_meeting_id": f"zoom_mock_{i+1}",
                "join_url": f"https://zoom.us/j/mock{i+1}",
                "status": "scheduled"
            }
            scheduled.append(interview)
        
        return scheduled
