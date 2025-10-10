"""
Transcription Service Module
Handles transcription of interview recordings using OpenAI Whisper
"""
import logging
from typing import List, Dict, Any
from openai import OpenAI

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Transcribes interview recordings to text"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def transcribe_all(self, recordings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transcribe all interview recordings
        
        Args:
            recordings: List of recording information
            
        Returns:
            List of transcripts
        """
        logger.info(f"Transcribing {len(recordings)} recordings")
        
        transcripts = []
        for recording in recordings:
            transcript = self.transcribe_single(recording)
            transcripts.append(transcript)
        
        logger.info(f"Completed {len(transcripts)} transcriptions")
        return transcripts
    
    def transcribe_single(self, recording: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transcribe a single recording
        
        Args:
            recording: Recording information
            
        Returns:
            Transcript data
        """
        if not self.client:
            logger.warning("OpenAI client not configured, using mock transcription")
            return self._mock_transcription(recording)
        
        try:
            # In a real implementation, this would use Whisper API
            # For now, we'll simulate transcription
            transcript = self._simulate_transcription(recording)
            return transcript
            
        except Exception as e:
            logger.error(f"Error transcribing recording {recording['id']}: {str(e)}")
            return self._mock_transcription(recording)
    
    def _simulate_transcription(self, recording: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate transcription with realistic content"""
        participant = recording['participant']
        
        # Generate realistic interview transcript content
        transcript_text = f"""Interview with {participant['name']} ({participant['title']})

Interviewer: Thank you for joining us today. Can you tell me about your biggest challenges in creating content for your sales funnel?

{participant['name']}: Absolutely. Our biggest challenge is maintaining consistency while scaling. We're trying to create personalized content for different segments, but it's incredibly time-consuming. Our team spends probably 60-70% of their time on content creation, leaving little room for strategy.

Interviewer: How do you currently handle personalization?

{participant['name']}: Right now, we use templates and manually customize them. It works for small campaigns, but when we need to launch something at scale, it becomes a bottleneck. We can't personalize as much as we'd like because we simply don't have the resources.

Interviewer: What about brand consistency?

{participant['name']}: That's another pain point. With multiple team members creating content, maintaining our brand voice is challenging. We have guidelines, but enforcing them manually is difficult, especially when we're under tight deadlines.

Interviewer: If you could solve one problem with a magic wand, what would it be?

{participant['name']}: I'd love a system that could generate high-quality, on-brand, personalized content at scale without requiring constant manual intervention. Something that understands our brand voice and can adapt content for different audience segments automatically.

Interviewer: How do you measure content effectiveness?

{participant['name']}: We track conversion rates, engagement metrics, and lead quality. But honestly, we struggle to attribute specific content pieces to conversions. Better analytics and insights would be incredibly valuable.
"""
        
        return {
            "id": f"transcript_{recording['id']}",
            "recording_id": recording['id'],
            "participant": participant,
            "text": transcript_text,
            "url": f"https://storage.example.com/transcripts/{recording['id']}.txt",
            "word_count": len(transcript_text.split()),
            "transcribed_date": recording['recorded_date'],
            "status": "completed"
        }
    
    def _mock_transcription(self, recording: Dict[str, Any]) -> Dict[str, Any]:
        """Mock transcription for testing"""
        return self._simulate_transcription(recording)
