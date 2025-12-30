"""
Utility functions for social-transcribe.
"""

import re
from typing import List


def clean_transcript(text: str) -> str:
    """
    Clean up transcript text by removing common filler words and fixing spacing.
    
    Args:
        text: Raw transcript text
        
    Returns:
        Cleaned text
    """
    # Remove common filler words (case-insensitive)
    fillers = ['um', 'uh', 'ah', 'er', 'like', 'you know']
    words = text.split()
    cleaned = [w for w in words if w.lower() not in fillers]
    
    # Fix multiple spaces
    text = ' '.join(cleaned)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def split_into_chunks(text: str, max_length: int = 4000) -> List[str]:
    """
    Split long text into chunks for processing.
    Useful if transcript is too long for LLM context window.
    
    Args:
        text: Text to split
        max_length: Maximum length per chunk
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def format_linkedin_post(post: str) -> str:
    """
    Format LinkedIn post with proper line breaks and spacing.
    
    Args:
        post: Raw post text from LLM
        
    Returns:
        Formatted post
    """
    # Ensure double line breaks between sections
    post = re.sub(r'\n{3,}', '\n\n', post)
    
    # Ensure single line break after periods at end of sentences
    post = re.sub(r'\.\s+([A-Z])', r'.\n\n\1', post)
    
    return post.strip()

