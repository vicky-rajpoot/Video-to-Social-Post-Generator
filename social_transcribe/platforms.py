"""
Platform definitions for social media post generation.
Each platform has specific formatting rules, emoji/hashtag preferences, and token limits.
"""

# Platform Definitions
PLATFORMS = {
    "1": {
        "name": "Twitter/X",
        "formatting_rules": """
1. Keep the entire post under 280 characters.
2. If the content is too long, structure it as a thread with /1, /2, etc.
3. Use short, punchy sentences.
4. Use line breaks for readability.
""",
        "use_emojis": True,
        "use_hashtags": True,
        "hashtag_count": "2-3",
        "max_tokens": 200
    },
    "2": {
        "name": "LinkedIn",
        "formatting_rules": """
1. Use bold for key phrases with **bold**.
2. Use short paragraphs or bullet points.
3. Professional tone.
""",
        "use_emojis": False,
        "use_hashtags": True,
        "hashtag_count": "3-5",
        "max_tokens": 1000
    },
    "3": {
        "name": "Instagram",
        "formatting_rules": """
1. Use engaging, visual language.
2. Short paragraphs with line breaks.
""",
        "use_emojis": True,
        "use_hashtags": True,
        "hashtag_count": "5-10",
        "max_tokens": 800
    },
    "4": {
        "name": "TikTok",
        "formatting_rules": """
1. Fun, energetic tone.
2. Short and snappy.
""",
        "use_emojis": True,
        "use_hashtags": True,
        "hashtag_count": "4-8",
        "max_tokens": 300
    },
    "5": {
        "name": "YouTube",
        "formatting_rules": """
1. This is for video descriptions.
2. Include timestamps if relevant.
3. Keywords for SEO.
4. Longer content is okay.
""",
        "use_emojis": True,
        "use_hashtags": False,
        "hashtag_count": "",
        "max_tokens": 1500
    }
}

# Style Definitions (Persona-Based)
STYLES = {
    "1": {
        "name": "Professional",
        "persona": "You are a highly respected professional with a large following on {platform}. You write in a polished, authoritative, and insightful style."
    },
    "2": {
        "name": "Casual",
        "persona": "You are a friendly and relatable influencer on {platform}. You write in a casual, conversational style that feels like chatting with a friend."
    },
    "3": {
        "name": "Storytelling",
        "persona": "You are a captivating storyteller on {platform}. You weave narratives that engage and inspire your audience."
    },
    "4": {
        "name": "Technical",
        "persona": "You are a technical expert on {platform}. You explain complex concepts clearly and precisely."
    },
    "5": {
        "name": "Motivational",
        "persona": "You are an inspiring motivator on {platform}. You use empowering language to encourage and uplift your followers."
    },
    "6": {
        "name": "Question-based",
        "persona": "You are an engagement expert on {platform}. You craft posts that spark discussions through thoughtful questions."
    }
}

