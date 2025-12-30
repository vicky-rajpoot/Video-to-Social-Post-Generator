"""
social-transcribe: Automated content engine for video transcription and social media post generation.
Supports multiple platforms: Twitter/X, LinkedIn, Instagram, TikTok, YouTube
"""

from .core import SocialTranscriber
from .generator import SocialPostGenerator, LinkedInGenerator
from .platforms import PLATFORMS, STYLES
from .config import load_config, save_default_config

# Backward compatibility aliases
VideoTranscriber = SocialTranscriber

__version__ = "2.0.0"
__all__ = [
    "SocialTranscriber",
    "VideoTranscriber",  # Alias for backward compatibility
    "SocialPostGenerator",
    "LinkedInGenerator",  # Backward compatibility
    "PLATFORMS",
    "STYLES",
    "load_config",
    "save_default_config"
]

