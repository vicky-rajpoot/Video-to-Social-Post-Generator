# test_cache.py
from pathlib import Path
import os

def check_whisper_cache():
    """Check what Whisper models are cached."""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    print("=" * 60)
    print("🔍 Whisper Model Cache Check")
    print("=" * 60)
    print(f"\nCache directory: {cache_dir}")
    
    if not cache_dir.exists():
        print("\n❌ Cache directory doesn't exist yet")
        print("   Models will be downloaded on first use")
        return
    
    print(f"\n📁 Cache directory exists: {cache_dir.exists()}")
    
    # Find whisper models
    whisper_models = []
    for item in cache_dir.iterdir():
        if item.is_dir() and "whisper" in item.name.lower():
            whisper_models.append(item)
    
    if whisper_models:
        print(f"\n✅ Found {len(whisper_models)} cached Whisper model(s):")
        for model in whisper_models:
            size = os.path.getsize(model) / (1024 * 1024)  # MB
            print(f"   • {model.name}")
            print(f"     Size: {size:.1f} MB")
    else:
        print("\n⚠️  No Whisper models found in cache")
        print("   Models will be downloaded on first use")

if __name__ == "__main__":
    check_whisper_cache()