"""
Main script to run the complete content pipeline:
URL → Audio Download → Transcription → Social Media Post Generation

Supports multiple platforms: Twitter/X, LinkedIn, Instagram, TikTok, YouTube
"""

import sys
from pathlib import Path
import torch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_transcribe.core import SocialTranscriber
from social_transcribe.generator import SocialPostGenerator
from social_transcribe.platforms import PLATFORMS, STYLES
from social_transcribe.config import load_config, save_default_config


def ask_choice(prompt, options, default_key, display_map):
    """Helper function to ask user for choice with defaults."""
    print(f"\n{prompt}")
    for k, v in display_map.items():
        print(f"  {k}: {v}")
    choice = input(f"👉 Enter number (default = {default_key}): ").strip()
    if not choice:
        choice = default_key
    return options[choice]


def main():
    """
    Complete workflow: Transcribe video and generate social media post.
    """
    print("=" * 70)
    print("🚀 Video-to-Social Post Generator — Interactive Mode")
    print("=" * 70)
    
    # Load configuration
    config = load_config()
    
    # Device Detection
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n💻 Device detected: {device.upper()}")
    
    # Ask if user wants to use config or customize
    use_config = input("\nUse saved configuration? (y/n, default=n): ").strip().lower() or "n"
    
    if use_config == "y":
        # Use saved config - map to new platform system
        provider = config['generator']['provider']
        model_name = config['generator']['model_name']
        whisper_model = config['transcription']['model_size']
        device = config['transcription']['device']
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Map old writing_style to new system
        style_map = {
            "professional": "1",
            "casual": "2",
            "storytelling": "3",
            "technical": "4",
            "motivational": "5",
            "question-based": "6"
        }
        style_key = style_map.get(config['post']['writing_style'], "1")
        style = STYLES[style_key]
        
        # Default to LinkedIn for backward compatibility
        platform = PLATFORMS["2"]  # LinkedIn
        
        print(f"\n📋 Using saved configuration:")
        print(f"   Provider: {provider}, Model: {model_name}")
        print(f"   Whisper: {whisper_model}, Device: {device}")
        print(f"   Platform: {platform['name']}, Style: {style['name']}")
    else:
        # Interactive mode - match Colab notebook flow
        # Provider
        provider_options = {
            "1": "gemini",
            "2": "openai"
        }
        provider_display = {
            "1": "Gemini (default, creative & fast)",
            "2": "OpenAI"
        }
        provider = ask_choice(
            "Choose AI provider:",
            provider_options,
            default_key="1",
            display_map=provider_display
        )
        
        # Model
        if provider == "gemini":
            default_model = "gemini-2.5-flash-lite"
        else:
            default_model = "gpt-4o-mini"
        
        model_name = input(
            f"\n🤖 Enter model name for {provider.upper()} "
            f"(press Enter for default={default_model}): "
        ).strip()
        
        if not model_name:
            model_name = default_model
        
        # Whisper Model
        whisper_options = {
            "1": "tiny",
            "2": "base",
            "3": "small",
            "4": "large-v3"
        }
        whisper_display = {
            "1": "tiny (fastest, lowest accuracy)",
            "2": "base (balanced)",
            "3": "small (better accuracy)",
            "4": "large-v3 (best, GPU recommended)"
        }
        whisper_model = ask_choice(
            "Choose transcription model:",
            whisper_options,
            default_key="4",
            display_map=whisper_display
        )
        
        # Platform
        platform_display = {
            "1": "Twitter/X",
            "2": "LinkedIn",
            "3": "Instagram",
            "4": "TikTok",
            "5": "YouTube"
        }
        platform = ask_choice(
            "Choose target platform:",
            PLATFORMS,
            default_key="1",
            display_map=platform_display
        )
        
        # Writing Style
        style_display = {
            "1": "Professional",
            "2": "Casual",
            "3": "Storytelling",
            "4": "Technical",
            "5": "Motivational",
            "6": "Question-based"
        }
        style = ask_choice(
            "Choose writing style:",
            STYLES,
            default_key="1",
            display_map=style_display
        )
    
    # Get video URL
    print("\n" + "=" * 70)
    url = input("🔗 Paste video URL (YouTube / TikTok / Instagram): ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        return
    
    # Initialize Engines
    print("\n⚙️  Initializing engines...")
    
    compute_type = config['transcription'].get('compute_type', 'int8')
    if compute_type == "auto":
        compute_type = "float16" if device == "cuda" else "int8"
    
    transcriber = SocialTranscriber(
        model_size=whisper_model if not use_config else config['transcription']['model_size'],
        device=device,
        compute_type=compute_type
    )
    
    writer = SocialPostGenerator(
        provider=provider if not use_config else config['generator']['provider'],
        model_name=model_name if not use_config else config['generator']['model_name']
    )
    
    print("✅ Ready!\n")
    
    try:
        # Step 1: Transcribe
        print("=" * 70)
        print("🎧 STEP 1: Transcribing video")
        print("=" * 70)
        
        result = transcriber.transcribe(url)
        full_text = transcriber.get_full_text(result)
        
        print(
            f"\n✅ Transcript complete "
            f"({len(result['transcript'])} segments | "
            f"{len(full_text)} characters)"
        )
        print(
            f"🌐 Language: {result['language']} "
            f"({result['language_probability']:.2%})"
        )
        
        # Step 2: Generate
        print("\n" + "=" * 70)
        print("✍️  STEP 2: Generating post")
        print("=" * 70)
        
        temperature = config['generator']['temperature'] if use_config else 0.7
        post = writer.generate_post(
            transcript=full_text,
            platform=platform,
            style=style,
            temperature=temperature
        )
        
        # Step 3: Output
        print("\n" + "=" * 70)
        print("✨ POST READY ✨")
        print("=" * 70)
        print(post)
        print("=" * 70)
        
        print("\n💡 Tip: Copy the post above and paste it into your social media platform!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Option to create default config file
    if len(sys.argv) > 1 and sys.argv[1] == "--create-config":
        save_default_config()
        print("\n✅ Configuration file created! Edit config.yaml to customize settings.")
    else:
        main()
