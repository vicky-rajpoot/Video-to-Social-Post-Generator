"""
Setup script for social-transcribe package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="social-transcribe",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated content engine: Transcribe videos and generate viral LinkedIn posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/social-transcribe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2023.10.13",
        "faster-whisper>=0.10.0",
        "ffmpeg-python>=0.2.0",
        "torch>=2.0.0",
        "openai>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "social-transcribe=examples.generate_post:main",
        ],
    },
)

