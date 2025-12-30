"""
The Brain: LLM-powered social media post generator.
Supports multiple platforms (Twitter/X, LinkedIn, Instagram, TikTok, YouTube) and multiple LLM providers.
"""

import os
from typing import Optional, Dict

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use environment variables only

# Import OpenAI (for OpenAI and Ollama)
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Import Gemini
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Import platform definitions
from .platforms import PLATFORMS, STYLES


class SocialPostGenerator:
    """
    Generates optimized social media posts from video transcripts using LLMs.
    Supports multiple platforms and multiple LLM providers (OpenAI, Gemini, Ollama).
    """
    
    def __init__(
        self,
        provider: str = "gemini",
        model_name: str = "gemini-1.5-flash",
        api_key: Optional[str] = None
    ):
        """
        Initialize the social post generator.
        
        Args:
            provider: 'openai' (paid), 'gemini' (free tier), or 'ollama' (free/local)
            model_name: Model name (e.g., 'gpt-4o' for OpenAI, 'gemini-1.5-flash' for Gemini, 'llama3' for Ollama)
            api_key: API key (if None, uses GEMINI_API_KEY or OPENAI_API_KEY env var)
        """
        self.provider = provider
        self.model_name = model_name
        
        if provider == "openai":
            if OpenAI is None:
                raise ImportError("openai package not installed. Run: pip install openai")
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key parameter."
                )
            self.client = OpenAI(api_key=api_key)
            self.model = None
            
        elif provider == "gemini":
            if genai is None:
                raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
            api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError(
                    "Gemini API key required. Set GEMINI_API_KEY env var or pass api_key parameter.\n"
                    "Get free API key at: https://makersuite.google.com/app/apikey"
                )
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            self.client = None  # Gemini doesn't use OpenAI client
            
        elif provider == "ollama":
            if OpenAI is None:
                raise ImportError("openai package not installed. Run: pip install openai")
            # Ollama mimics OpenAI's API structure locally
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"  # required but unused
            )
            self.model = None
            print("💡 Using Ollama (local). Make sure Ollama is running: ollama serve")
            
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'gemini', or 'ollama'")
    
    def generate_post(
        self,
        transcript: str,
        platform: Dict,
        style: Dict,
        temperature: float = 0.7
    ) -> str:
        """
        Sends transcript to LLM and returns a formatted social post.
        
        Args:
            transcript: Raw transcript text from video
            platform: Platform dictionary from platforms.PLATFORMS
            style: Style dictionary from platforms.STYLES
            temperature: Sampling temperature (0.0-1.0, higher = more creative)
            
        Returns:
            Formatted social post text
        """
        print(f"🧠 Generating post using {self.provider} ({self.model_name})...")
        print(f"   Platform: {platform['name']}, Style: {style['name']}")

        platform_name = platform["name"]
        persona = style["persona"].format(platform=platform_name)
        formatting_rules = platform["formatting_rules"]
        use_emojis = platform["use_emojis"]
        use_hashtags = platform["use_hashtags"]
        hashtag_count = platform["hashtag_count"]
        max_tokens = platform["max_tokens"]

        system_prompt = f"""{persona}

Your goal is to take a raw video transcript and turn it into a viral post for {platform_name}.

Follow these strict formatting rules:
{formatting_rules}

Start with a strong hook.
Use clean formatting.
End with a call to action.
Remove "umms", "ahhs", and rambling from the transcript. Keep it authentic but polished.
"""

        if use_emojis:
            system_prompt += "\nUse emojis sparingly and appropriately to enhance engagement."
        if use_hashtags:
            system_prompt += f"\nInclude {hashtag_count} relevant hashtags at the end."

        system_prompt += "\n\nOutput only the post content, no meta-commentary."

        user_prompt = f"""Here is the transcript of a video. Write a post based on this:

{transcript}"""

        try:
            if self.provider == "gemini":
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                return response.text.strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            if self.provider == "ollama":
                error_msg = (
                    f"Failed to connect to Ollama. Make sure:\n"
                    f"  1. Ollama is installed: https://ollama.ai\n"
                    f"  2. Ollama is running: ollama serve\n"
                    f"  3. Model is pulled: ollama pull {self.model_name}\n"
                    f"Original error: {str(e)}"
                )
            elif self.provider == "gemini":
                error_msg = f"Gemini API error: {str(e)}\nGet free API key at: https://makersuite.google.com/app/apikey"
            else:
                error_msg = f"OpenAI API error: {str(e)}"
            
            raise Exception(error_msg)
    
    def generate_custom_post(
        self,
        transcript: str,
        custom_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a post with a custom prompt (e.g., Twitter thread, blog post, etc.)
        
        Args:
            transcript: Raw transcript text from video
            custom_prompt: Custom system prompt for different content types
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response (None = model default)
            
        Returns:
            Generated content text
        """
        print(f"🧠 Generating custom content using {self.provider} ({self.model_name})...")
        
        user_prompt = f"""Here is the transcript of a video:

{transcript}"""

        try:
            if self.provider == "gemini":
                full_prompt = f"{custom_prompt}\n\n{user_prompt}"
                config = {"temperature": temperature}
                if max_tokens:
                    config["max_output_tokens"] = max_tokens
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(**config)
                )
                return response.text.strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": custom_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            if self.provider == "ollama":
                error_msg = (
                    f"Failed to connect to Ollama. Make sure Ollama is running.\n"
                    f"Original error: {str(e)}"
                )
            elif self.provider == "gemini":
                error_msg = f"Gemini API error: {str(e)}"
            else:
                error_msg = f"API error: {str(e)}"
            
            raise Exception(error_msg)
    
    @staticmethod
    def list_platforms():
        """List all available platforms."""
        return PLATFORMS
    
    @staticmethod
    def list_styles():
        """List all available writing styles."""
        return STYLES


# Backward compatibility: Keep LinkedInGenerator as an alias
class LinkedInGenerator(SocialPostGenerator):
    """
    Backward compatibility alias for SocialPostGenerator.
    Use SocialPostGenerator for new code.
    """
    
    def generate_post(
        self,
        transcript: str,
        writing_style: str = "professional",
        word_count: str = "medium",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        include_hashtags: bool = True,
        include_emoji: bool = False
    ) -> str:
        """
        Legacy method for LinkedIn-only generation.
        Maps old parameters to new platform-based system.
        """
        # Use LinkedIn platform (platform "2")
        platform = PLATFORMS["2"]
        
        # Map writing style to new style system
        style_map = {
            "professional": "1",
            "casual": "2",
            "storytelling": "3",
            "technical": "4",
            "motivational": "5",
            "question-based": "6"
        }
        style_key = style_map.get(writing_style, "1")
        style = STYLES[style_key]
        
        # Override platform settings based on old parameters
        if not include_hashtags:
            platform = platform.copy()
            platform["use_hashtags"] = False
        if include_emoji:
            platform = platform.copy()
            platform["use_emojis"] = True
        
        # Adjust max_tokens based on word_count if provided
        if max_tokens is None:
            word_count_map = {
                "short": 300,
                "medium": 600,
                "long": 900,
                "very-long": 1500
            }
            max_tokens = word_count_map.get(word_count, 600)
        
        # Temporarily override max_tokens
        original_max_tokens = platform["max_tokens"]
        platform = platform.copy()
        platform["max_tokens"] = max_tokens
        
        result = super().generate_post(transcript, platform, style, temperature)
        
        return result
