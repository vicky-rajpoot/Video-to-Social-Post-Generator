"""
Configuration loader for Social Transcribe
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG = {
    "transcription": {
        "model_size": "large-v3",
        "device": "auto",
        "compute_type": "auto"
    },
    "generator": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash-lite",
        "temperature": 0.7
    },
    "post": {
        "platform": "1",  # Twitter/X (1), LinkedIn (2), Instagram (3), TikTok (4), YouTube (5)
        "writing_style": "1",  # Professional (1), Casual (2), Storytelling (3), Technical (4), Motivational (5), Question-based (6)
        "word_count": "medium",  # Legacy support
        "include_hashtags": True,  # Legacy support
        "include_emoji": False  # Legacy support
    }
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file or use defaults.
    
    Args:
        config_path: Path to config.yaml file. If None, looks for config.yaml in project root.
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        # Look for config.yaml in project root
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config.yaml"
    
    config_path = Path(config_path)
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                # Merge with defaults
                merged_config = _merge_dicts(DEFAULT_CONFIG.copy(), config)
                print(f"✅ Loaded configuration from {config_path}")
                return merged_config
        except Exception as e:
            print(f"⚠️  Error loading config file: {e}")
            print("   Using default configuration")
            return DEFAULT_CONFIG.copy()
    else:
        print(f"ℹ️  Config file not found at {config_path}")
        print("   Using default configuration")
        return DEFAULT_CONFIG.copy()


def _merge_dicts(default: Dict, override: Dict) -> Dict:
    """Recursively merge two dictionaries."""
    result = default.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def save_default_config(output_path: str = "config.yaml"):
    """
    Save default configuration to a file.
    
    Args:
        output_path: Path where to save the config file
    """
    output_path = Path(output_path)
    
    config_text = """# Social Transcribe 2.0 Configuration File
# Modify these settings as needed

# Whisper Transcription Settings
transcription:
  model_size: "large-v3"  # Options: tiny, base, small, medium, large-v3, large-v3-turbo
  device: "auto"  # Options: cpu, cuda, auto
  compute_type: "auto"  # Options: int8, float16, float32, auto

# LLM Generator Settings
generator:
  provider: "gemini"  # Options: gemini, openai, ollama
  model_name: "gemini-2.5-flash-lite"  # Examples: gemini-2.5-flash-lite, gemini-pro, gpt-4o, gpt-4o-mini, llama3
  temperature: 0.7  # 0.0-1.0, higher = more creative

# Post Generation Settings
post:
  platform: "1"  # Options: 1=Twitter/X, 2=LinkedIn, 3=Instagram, 4=TikTok, 5=YouTube
  writing_style: "1"  # Options: 1=Professional, 2=Casual, 3=Storytelling, 4=Technical, 5=Motivational, 6=Question-based
  # Legacy options (for backward compatibility):
  word_count: "medium"  # Options: short (100-200), medium (200-400), long (400-600), very-long (600+)
  include_hashtags: true
  include_emoji: false

# API Keys (set via environment variables or .env file)
# GEMINI_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
"""
    
    with open(output_path, 'w') as f:
        f.write(config_text)
    
    print(f"✅ Default configuration saved to {output_path}")

