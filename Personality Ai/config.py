"""
Configuration settings for the AI Personality Learning System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (all optional for free version)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', '')

# Free alternatives enabled by default
USE_FREE_SEARCH = True  # Use free web scraping instead of paid APIs
USE_WIKIPEDIA_ONLY = False  # Set to True to use only Wikipedia (completely free)
ENABLE_OFFLINE_MODE = False  # Set to True for offline learning with pre-loaded data

# File paths
MEMORY_DIR = "memory"
KNOWLEDGE_BASE_FILE = "memory/knowledge_base.json"
PERSONALITY_PROFILE_FILE = "memory/personality_profile.json"
LEARNING_HISTORY_FILE = "memory/learning_history.json"
QUESTIONS_ARCHIVE_FILE = "memory/questions_archive.json"

# AI Personality Settings
PERSONALITY_TRAITS = {
    "curiosity": 0.9,
    "openness": 0.8,
    "analytical": 0.7,
    "empathy": 0.8,
    "creativity": 0.6,
    "persistence": 0.9,
    "social": 0.7,
    "adaptability": 0.8
}

# Learning Parameters
MAX_QUESTIONS_PER_CYCLE = 5
SEARCH_RESULTS_LIMIT = 10
LEARNING_CYCLES_PER_SESSION = 3
KNOWLEDGE_RETENTION_THRESHOLD = 0.7
QUESTION_COMPLEXITY_GROWTH_RATE = 0.1

# Search Settings
SEARCH_DELAY = 3  # seconds between searches (increased for free scraping)
MAX_RETRIES = 3
TIMEOUT = 30

# Free Search Sources (no API keys required)
FREE_SEARCH_SOURCES = [
    "https://en.wikipedia.org",
    "https://www.psychologytoday.com",
    "https://www.verywellmind.com",
    "https://www.simplypsychology.org",
    "https://www.apa.org",
    "https://plato.stanford.edu"  # Stanford Encyclopedia of Philosophy
]

# Free search engines that don't require API keys
FREE_SEARCH_ENGINES = [
    "duckduckgo",  # DuckDuckGo (no API key needed)
    "wikipedia",   # Wikipedia API (free)
    "direct_scraping"  # Direct website scraping
]

# Personality Topics to Focus On
CORE_PERSONALITY_TOPICS = [
    "personality psychology",
    "human behavior patterns",
    "communication styles",
    "emotional intelligence",
    "social interaction",
    "personality development",
    "behavioral psychology",
    "cognitive patterns",
    "interpersonal skills",
    "personality traits"
]

# Advanced Learning Topics (unlocked as AI evolves)
ADVANCED_TOPICS = [
    "personality disorders",
    "cultural personality differences",
    "personality and career success",
    "personality in relationships",
    "personality change over time",
    "personality assessment methods",
    "personality and mental health",
    "personality in leadership",
    "personality and creativity",
    "personality neuroscience"
]
