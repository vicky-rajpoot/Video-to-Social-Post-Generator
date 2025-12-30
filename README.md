# Social Transcribe 2.0 🚀

**Automated Content Engine**: Transform video URLs into viral social media posts with AI. Supports Twitter/X, LinkedIn, Instagram, TikTok, and YouTube.

## Architecture

This project splits into two distinct engines:

- **The Ear (Transcriber)**: Downloads video audio and transcribes it using faster-whisper
- **The Brain (Generator)**: Reads the transcript and generates a professional LinkedIn post using LLMs

### Data Flow

```
URL → [Audio Downloader] → .mp3 → [Whisper Model] → Raw Transcript → [LLM + Platform-Specific Prompt] → Viral Social Media Post
```

## Features

✅ **Multi-Platform Support**: Twitter/X, LinkedIn, Instagram, TikTok, YouTube with platform-specific formatting  
✅ **Multiple LLM Providers**: Supports Gemini (free tier), OpenAI (paid), and Ollama (free/local)  
✅ **High-Quality Transcription**: Uses faster-whisper with GPU/CPU support  
✅ **6 Writing Styles**: Professional, casual, storytelling, technical, motivational, question-based  
✅ **Platform-Optimized**: Automatic formatting, hashtags, and emojis based on platform  
✅ **Google Colab Ready**: Pre-built notebook in `notebooks/` directory  
✅ **Configuration File**: Easy default settings management  
✅ **CPU/GPU Support**: Automatic device detection with manual override  
✅ **Interactive CLI**: Step-by-step prompts for easy customization  

## Installation

### 1. Clone or Download the Project

```bash
cd ~/ml-project  # or your project directory
```

### 2. Create Virtual Environment (Recommended)

**For WSL/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# If python3-venv is not installed:
sudo apt install python3-venv python3-full
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install FFmpeg

**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux/Ubuntu/WSL:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 5. Set Up API Keys

You need at least one API key depending on which LLM provider you want to use:

#### Option A: Gemini (Free Tier - Recommended)

1. Get free API key: https://makersuite.google.com/app/apikey
2. Set environment variable:

**Linux/WSL:**
```bash
export GEMINI_API_KEY="your-api-key-here"

# Or add to ~/.bashrc for permanent:
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Or use .env file:**
```bash
# Create .env file in project root
echo 'GEMINI_API_KEY=your-api-key-here' > .env
```

#### Option B: OpenAI (Paid)

1. Get API key: https://platform.openai.com/api-keys
2. Set environment variable:
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

#### Option C: Ollama (Free/Local)

```bash
# Install Ollama from https://ollama.ai
# Then pull a model:
ollama pull llama3
ollama serve  # Keep this running
```

### 6. (Optional) Create Configuration File

```bash
python examples/generate_post.py --create-config
```

This creates `config.yaml` with default settings that you can customize.

## Usage

### Quick Start

**Option 1: Google Colab (Easiest - No Setup Required)**
1. Open `notebooks/social_transcribe_colab.ipynb` in Google Colab
2. Add your API key to Colab Secrets (key icon in sidebar)
3. Enable GPU: Runtime → Change runtime type → GPU
4. Run all cells and follow the prompts!

**Option 2: Local Installation**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/WSL
# or
venv\Scripts\activate  # Windows

# Run the script
python examples/generate_post.py
```

The script will:
1. Ask if you want to use saved configuration or customize
2. Prompt for AI provider, model, platform, and style
3. Prompt for video URL
4. Transcribe the video
5. Generate platform-optimized social post
6. Display the result

### Using Configuration File

1. **Create default config:**
   ```bash
   python examples/generate_post.py --create-config
   ```

2. **Edit `config.yaml`** with your preferences:
   ```yaml
   transcription:
     model_size: "base"  # or large-v3-turbo for better quality
     device: "cpu"  # or "cuda" for GPU, "auto" for auto-detect
     compute_type: "int8"
   
   generator:
     provider: "gemini"  # or "openai", "ollama"
     model_name: "gemini-pro"
     temperature: 0.7
   
   post:
     writing_style: "professional"  # See available styles below
     word_count: "medium"
     include_hashtags: true
     include_emoji: false
   ```

3. **Run with saved config:**
   ```bash
   python examples/generate_post.py
   # Choose 'y' when asked to use saved configuration
   ```

### Programmatic Usage

```python
from social_transcribe.core import SocialTranscriber
from social_transcribe.generator import LinkedInGenerator

# Initialize engines
transcriber = SocialTranscriber(
    model_size="base",
    device="cpu",  # or "cuda" for GPU
    compute_type="int8"
)

writer = LinkedInGenerator(
    provider="gemini",  # or "openai", "ollama"
    model_name="gemini-pro"
)

# Transcribe video
result = transcriber.transcribe("https://youtube.com/watch?v=...")
full_text = transcriber.get_full_text(result)

# Generate LinkedIn post with custom options
post = writer.generate_post(
    full_text,
    writing_style="professional",  # See available styles below
    word_count="medium",  # short, medium, long, very-long
    include_hashtags=True,
    include_emoji=False
)

print(post)
```

### Writing Styles

Choose from 6 different writing styles:

1. **professional** - Standard LinkedIn format with hook, body, takeaway, and CTA
2. **casual** - Friendly, conversational tone
3. **storytelling** - Narrative-style with story arc
4. **technical** - Detailed, technical content for professionals
5. **motivational** - Inspiring and uplifting content
6. **question-based** - Engagement-focused with multiple questions

### Word Count Options

- **short**: 100-200 words (concise and impactful)
- **medium**: 200-400 words (good detail, readable)
- **long**: 400-600 words (comprehensive insights)
- **very-long**: 600+ words (in-depth analysis)

### Device Selection

- **cpu**: Use CPU (works everywhere, slower)
- **cuda**: Use GPU (faster, requires CUDA setup)
- **auto**: Automatically detect and use best available

## Configuration

### Transcriber Options

- `model_size`: 
  - `"tiny"` - Fastest, least accurate
  - `"base"` - Fast, good balance (recommended for CPU)
  - `"small"` - Balanced
  - `"medium"` - Better accuracy
  - `"large-v3"` - High accuracy
  - `"large-v3-turbo"` - High accuracy, optimized (recommended for GPU)

- `device`: `"cpu"`, `"cuda"`, or `"auto"`
- `compute_type`: 
  - `"int8"` - Fastest CPU option
  - `"float16"` - Best for GPU
  - `"float32"` - Most compatible
  - `"auto"` - Auto-select based on device

### Generator Options

- `provider`: `"gemini"` (free), `"openai"` (paid), or `"ollama"` (local)
- `model_name`: 
  - Gemini: `"gemini-pro"`, `"gemini-2.5-flash-lite"`, etc.
  - OpenAI: `"gpt-4o"`, `"gpt-3.5-turbo"`, etc.
  - Ollama: `"llama3"`, `"mistral"`, etc.
- `temperature`: `0.0-1.0` (higher = more creative)

### Post Generation Options

- `writing_style`: See Writing Styles section above
- `word_count`: See Word Count Options section above
- `include_hashtags`: `true` or `false`
- `include_emoji`: `true` or `false`

## Project Structure

```
social-transcribe/
│
├── social_transcribe/
│   ├── __init__.py
│   ├── core.py           # Engine 1: Downloads & Transcribes (The Ear)
│   ├── generator.py       # Engine 2: LLM Post Writer (The Brain)
│   ├── platforms.py       # Platform and style definitions
│   ├── config.py          # Configuration loader
│   └── utils.py           # Helper functions
│
├── examples/
│   └── generate_post.py   # Main script to run the whole flow
│
├── notebooks/
│   └── social_transcribe_colab.ipynb  # Ready-to-use Google Colab notebook
│
├── config.yaml            # Configuration file (create with --create-config)
├── requirements.txt
├── setup.py
└── README.md
```

## Troubleshooting

### CUDA/cuDNN Errors

If you get CUDA errors, use CPU instead:

```python
transcriber = SocialTranscriber(
    model_size="base",
    device="cpu",
    compute_type="int8"
)
```

Or set in `config.yaml`:
```yaml
transcription:
  device: "cpu"
  compute_type: "int8"
```

### FFmpeg Not Found

Make sure FFmpeg is installed and in your PATH:
```bash
ffmpeg -version  # Should show version info
```

### API Key Not Found

Make sure your API key is set:
```bash
# Check if set
echo $GEMINI_API_KEY  # Linux/WSL
echo $env:GEMINI_API_KEY  # Windows PowerShell

# Or use .env file
# Create .env in project root with:
# GEMINI_API_KEY=your-key-here
```

### Module Not Found

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/WSL
pip install -r requirements.txt
```

### Externally Managed Environment Error (WSL/Ubuntu)

Use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Google Colab Usage

For quick testing with free GPU, use Google Colab:

### Option 1: Use the Ready-Made Notebook (Recommended)

1. **Open the notebook:**
   - Go to https://colab.research.google.com/
   - Click "File" → "Upload notebook"
   - Upload `notebooks/social_transcribe_colab.ipynb` from this repository
   - Or open directly from GitHub if the repo is public

2. **Set up API keys:**
   - Click the key icon (🔑) in the left sidebar
   - Add `GEMINI_API_KEY` (get free key at https://makersuite.google.com/app/apikey)
   - Or add `OPENAI_API_KEY` if using OpenAI

3. **Enable GPU (recommended):**
   - Runtime → Change runtime type → GPU (T4)

4. **Run the notebook:**
   - Click "Run all" or run cells one by one
   - Follow the interactive prompts to choose your settings
   - Paste your video URL when prompted

### Option 2: Manual Setup

1. Go to https://colab.research.google.com/
2. Enable GPU: Runtime → Change runtime type → GPU (T4)
3. Install dependencies:
   ```python
   !pip install -q yt-dlp faster-whisper google-generativeai python-dotenv pyyaml openai
   !apt-get update -qq && apt-get install -y -qq ffmpeg
   ```
4. Set API key using Colab Secrets (key icon in sidebar)
5. Copy the code from `examples/generate_post.py` and adapt for Colab

## Examples

### Example 1: Quick Professional Post

```python
from social_transcribe.core import SocialTranscriber
from social_transcribe.generator import LinkedInGenerator

transcriber = SocialTranscriber(model_size="base", device="cpu")
writer = LinkedInGenerator(provider="gemini", model_name="gemini-pro")

result = transcriber.transcribe("https://youtube.com/watch?v=...")
post = writer.generate_post(
    transcriber.get_full_text(result),
    writing_style="professional",
    word_count="medium"
)
print(post)
```

### Example 2: Technical Long-Form Post

```python
post = writer.generate_post(
    transcript,
    writing_style="technical",
    word_count="long",
    include_hashtags=True
)
```

### Example 3: Using Configuration File

```python
from social_transcribe.config import load_config
from social_transcribe.core import SocialTranscriber
from social_transcribe.generator import LinkedInGenerator

config = load_config()

transcriber = SocialTranscriber(
    model_size=config['transcription']['model_size'],
    device=config['transcription']['device'],
    compute_type=config['transcription']['compute_type']
)

writer = LinkedInGenerator(
    provider=config['generator']['provider'],
    model_name=config['generator']['model_name']
)

result = transcriber.transcribe(url)
post = writer.generate_post(
    transcriber.get_full_text(result),
    writing_style=config['post']['writing_style'],
    word_count=config['post']['word_count'],
    include_hashtags=config['post']['include_hashtags'],
    include_emoji=config['post']['include_emoji']
)
```

## Why This Architecture Wins

1. **Vendor Agnostic**: Switch between Gemini, OpenAI, and Ollama with one parameter change
2. **Separation of Concerns**: Change prompt styles without breaking transcription
3. **Scalable**: Easy to add summarization, keyword extraction, or other processing steps
4. **Extensible**: Add new content types (Twitter threads, blog posts) via `generate_custom_post()`
5. **Flexible**: Multiple writing styles, word counts, and customization options
6. **User-Friendly**: Configuration file support for easy default settings

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For issues or questions:
- Check the Troubleshooting section above
- Open an issue on GitHub
- Review the configuration options in `config.yaml`
