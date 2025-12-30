"""
The Ear: Video transcription engine using faster-whisper and yt-dlp.
Handles audio download and transcription, returning clean text for the LLM.
"""

import os
import shutil
import tempfile
import yt_dlp
from faster_whisper import WhisperModel
from typing import Dict, List, Optional


class SocialTranscriber:
    """
    Downloads video audio and transcribes it using faster-whisper.
    Returns clean transcript text ready for LLM processing.
    """
    
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",  # Change default to "cpu"
        compute_type: str = "int8"  # Change default to "int8"
    ):
        """
        Initialize the transcriber.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v3, large-v3-turbo)
            device: 'cuda' or 'cpu'
            compute_type: 'float16', 'int8', or 'int8_float16'
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        
    def _load_model(self):
        """Lazy load the Whisper model with automatic fallback."""
        if self.model is None:
            print(f"📥 Loading Whisper model: {self.model_size}...")
            
            # Try to load with specified device/compute_type
            try:
                self.model = WhisperModel(
                    self.model_size,
                    device=self.device,
                    compute_type=self.compute_type
                )
                print(f"✅ Model loaded on {self.device}")
            except Exception as e:
                if self.device == "cuda":
                    print(f"⚠️  CUDA error: {str(e)[:100]}")
                    print("🔄 Falling back to CPU...")
                    self.device = "cpu"
                    self.compute_type = "int8"
                    self.model = WhisperModel(
                        self.model_size,
                        device="cpu",
                        compute_type="int8"
                    )
                    print("✅ Model loaded on CPU")
                else:
                    raise
    
    def _download_audio(self, url: str) -> str:
        """
        Download audio from video URL with enhanced options to avoid 403 errors.
        Returns path to temporary audio file.
        """
        print(f"⬇️  Downloading audio from: {url}")
        temp_dir = tempfile.mkdtemp()
        temp_base = os.path.join(temp_dir, "audio")

        # Enhanced yt-dlp options to bypass 403 errors
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_base + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Enhanced headers to mimic real browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            },
            # Additional options to avoid blocking
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],  # Try Android client first, fallback to web
                }
            },
            'quiet': False,
            'no_warnings': False,
            'retries': 10,  # Retry on failures
            'fragment_retries': 10,
            'ignoreerrors': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            actual_path = temp_base + '.mp3'
            if os.path.exists(actual_path):
                return actual_path
            else:
                # Try to find any audio file in temp directory
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp3', '.m4a', '.webm', '.ogg')):
                        return os.path.join(temp_dir, file)
                raise FileNotFoundError(f"Downloaded audio file not found at {actual_path}")
        except Exception as e:
            # Try alternative method with different extractor
            if "403" in str(e) or "Forbidden" in str(e):
                print("⚠️  First attempt failed with 403. Trying alternative method...")
                try:
                    # Alternative options with different player client
                    ydl_opts_alt = {
                        'format': 'bestaudio/best',
                        'outtmpl': temp_base + '.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        },
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['ios', 'android'],  # Try iOS/Android clients
                            }
                        },
                        'quiet': False,
                        'no_warnings': False,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_alt) as ydl:
                        ydl.download([url])

                    actual_path = temp_base + '.mp3'
                    if os.path.exists(actual_path):
                        return actual_path
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp3', '.m4a', '.webm', '.ogg')):
                            return os.path.join(temp_dir, file)
                except Exception as e2:
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    raise Exception(f"Failed to download audio after retry: {str(e2)}")

            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise Exception(f"Failed to download audio: {str(e)}")
    
    def _transcribe_audio(self, audio_path: str) -> Dict:
        """
        Transcribe audio file using Whisper.
        Returns dict with transcript segments and full text.
        """
        self._load_model()
        
        print("🎤 Transcribing audio...")
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            language="en",  # Can be made configurable
            task="transcribe"
        )
        
        transcript_segments = []
        for segment in segments:
            transcript_segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip()
            })
        
        return {
            'transcript': transcript_segments,
            'language': info.language,
            'language_probability': info.language_probability
        }
    
    def transcribe(self, url: str) -> Dict:
        """
        Main method: Download video and transcribe it.
        
        Args:
            url: Video URL (YouTube, TikTok, Instagram Reels, etc.)
            
        Returns:
            Dict with 'transcript' (list of segments) and metadata
        """
        audio_path = None
        temp_dir = None
        try:
            # Step 1: Download audio
            audio_path = self._download_audio(url)
            # Get temp directory from audio path
            temp_dir = os.path.dirname(audio_path)
            
            # Step 2: Transcribe
            result = self._transcribe_audio(audio_path)
            
            return result
            
        finally:
            # Clean up temporary audio file and directory
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except:
                    pass
    
    def get_full_text(self, result: Dict) -> str:
        """
        Helper method to combine all transcript segments into a single text block.
        Useful for passing to the LLM generator.
        
        Args:
            result: Result dict from transcribe() method
            
        Returns:
            Combined transcript text as a single string
        """
        return " ".join([seg['text'] for seg in result['transcript']])


# Backward compatibility alias
VideoTranscriber = SocialTranscriber

