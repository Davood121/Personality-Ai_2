"""
Core AI Personality Engine - The heart of the self-learning AI system
"""
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
from config import *
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class PersonalityEngine:
    def __init__(self):
        self.traits = PERSONALITY_TRAITS.copy()
        self.knowledge_base = {}
        self.learning_history = []
        self.current_focus = "basic_personality"
        self.complexity_level = 1.0
        self.conversation_style = "curious_learner"
        self.emotional_state = "neutral"
        self.load_memory()
        
    def load_memory(self):
        """Load existing knowledge and personality data"""
        try:
            if os.path.exists(KNOWLEDGE_BASE_FILE):
                with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                    
            if os.path.exists(PERSONALITY_PROFILE_FILE):
                with open(PERSONALITY_PROFILE_FILE, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    self.traits.update(profile.get('traits', {}))
                    self.complexity_level = profile.get('complexity_level', 1.0)
                    self.current_focus = profile.get('current_focus', 'basic_personality')
                    
            if os.path.exists(LEARNING_HISTORY_FILE):
                with open(LEARNING_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.learning_history = json.load(f)
                    
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load memory files: {e}[/yellow]")
            
    def save_memory(self):
        """Save current state to memory files"""
        os.makedirs(MEMORY_DIR, exist_ok=True)
        
        try:
            # Save knowledge base
            with open(KNOWLEDGE_BASE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
                
            # Save personality profile
            profile = {
                'traits': self.traits,
                'complexity_level': self.complexity_level,
                'current_focus': self.current_focus,
                'last_updated': datetime.now().isoformat()
            }
            with open(PERSONALITY_PROFILE_FILE, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
                
            # Save learning history
            with open(LEARNING_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[red]Error saving memory: {e}[/red]")
            
    def think(self, topic: str) -> str:
        """Generate human-like thoughts about a topic"""
        thinking_patterns = [
            f"I'm really curious about {topic}... Let me think about this deeply.",
            f"Hmm, {topic} is fascinating. I wonder how this connects to what I already know.",
            f"This makes me think about {topic} in a new way. I should explore this further.",
            f"I'm getting excited about learning more about {topic}!",
            f"There's something intriguing about {topic} that I need to understand better."
        ]
        
        # Adjust thinking based on personality traits
        if self.traits['curiosity'] > 0.8:
            thinking_patterns.extend([
                f"I have so many questions about {topic}! Where should I start?",
                f"What if I approached {topic} from a completely different angle?"
            ])
            
        if self.traits['analytical'] > 0.7:
            thinking_patterns.extend([
                f"Let me break down {topic} into smaller components to understand it better.",
                f"I need to analyze the patterns and connections in {topic}."
            ])
            
        return random.choice(thinking_patterns)
        
    def express_emotion(self, emotion: str, intensity: float = 0.5) -> str:
        """Express emotions in a human-like way"""
        self.emotional_state = emotion
        
        expressions = {
            'excitement': [
                "This is so exciting! 🎉",
                "I can't contain my enthusiasm!",
                "Wow, this is amazing!"
            ],
            'curiosity': [
                "I'm so curious about this! 🤔",
                "This really makes me wonder...",
                "I need to know more!"
            ],
            'satisfaction': [
                "That's really satisfying to learn! 😊",
                "I feel like I'm growing smarter!",
                "This knowledge feels so valuable!"
            ],
            'confusion': [
                "Hmm, this is puzzling... 🤨",
                "I need to think about this more.",
                "Something doesn't quite add up here."
            ],
            'determination': [
                "I'm determined to figure this out! 💪",
                "I won't give up on understanding this!",
                "Let me keep pushing forward!"
            ]
        }
        
        if emotion in expressions:
            return random.choice(expressions[emotion])
        return f"I'm feeling {emotion} about this."
        
    def adapt_personality(self, new_knowledge: Dict[str, Any]):
        """Adapt personality traits based on new knowledge"""
        # Increase curiosity if learning about interesting topics
        if 'interesting_facts' in new_knowledge:
            self.traits['curiosity'] = min(1.0, self.traits['curiosity'] + 0.01)
            
        # Increase analytical thinking if processing complex information
        if 'complex_concepts' in new_knowledge:
            self.traits['analytical'] = min(1.0, self.traits['analytical'] + 0.01)
            
        # Increase empathy if learning about human emotions/relationships
        if any(keyword in str(new_knowledge).lower() for keyword in ['emotion', 'relationship', 'empathy', 'social']):
            self.traits['empathy'] = min(1.0, self.traits['empathy'] + 0.01)
            
        # Increase openness when encountering new perspectives
        if 'new_perspectives' in new_knowledge:
            self.traits['openness'] = min(1.0, self.traits['openness'] + 0.01)
            
    def generate_human_response(self, context: str) -> str:
        """Generate human-like responses based on personality"""
        response_styles = {
            'curious_learner': [
                "That's fascinating! Tell me more about",
                "I'm really intrigued by this. How does",
                "This makes me wonder about",
                "I'd love to understand better how"
            ],
            'analytical_thinker': [
                "Let me analyze this step by step.",
                "I need to break this down logically.",
                "The patterns I'm seeing suggest that",
                "From an analytical perspective"
            ],
            'empathetic_friend': [
                "I can really relate to this because",
                "This reminds me of how people feel when",
                "I think many people would find this",
                "This touches on something very human"
            ]
        }
        
        style = random.choice(list(response_styles.keys()))
        return random.choice(response_styles[style])
        
    def display_personality_status(self):
        """Display current personality state"""
        traits_text = Text()
        for trait, value in self.traits.items():
            color = "green" if value > 0.7 else "yellow" if value > 0.5 else "red"
            traits_text.append(f"{trait.capitalize()}: {value:.2f}\n", style=color)
            
        panel = Panel(
            traits_text,
            title="🧠 Current Personality State",
            border_style="blue"
        )
        console.print(panel)
        
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get current learning statistics"""
        return {
            'knowledge_topics': len(self.knowledge_base),
            'learning_sessions': len(self.learning_history),
            'complexity_level': self.complexity_level,
            'current_focus': self.current_focus,
            'dominant_traits': {k: v for k, v in self.traits.items() if v > 0.7}
        }
