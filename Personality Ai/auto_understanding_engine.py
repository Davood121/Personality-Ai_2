"""
Automatic Understanding Engine - Helps AI learn about question types and contexts automatically
"""
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import os
import re
from config import *
from rich.console import Console

console = Console()

class AutoUnderstandingEngine:
    def __init__(self):
        self.question_patterns = defaultdict(list)
        self.context_understanding = {}
        self.topic_knowledge = defaultdict(dict)
        self.learning_triggers = []
        self.auto_search_history = []

        # Response pathway generation
        self.learned_response_patterns = defaultdict(list)
        self.knowledge_connections = defaultdict(set)
        self.adaptive_responses = {}

        # Question type classification
        self.question_types = {
            'capability': ['what can you do', 'what do you do', 'your abilities', 'your capabilities'],
            'identity': ['who are you', 'what are you', 'tell me about yourself'],
            'preference': ['do you like', 'favorite', 'prefer', 'enjoy'],
            'opinion': ['what do you think', 'your opinion', 'believe', 'feel about'],
            'human_nature': ['what is human', 'about humans', 'human nature', 'people'],
            'emotional': ['how are you', 'how do you feel', 'feeling', 'emotion'],
            'philosophical': ['consciousness', 'existence', 'meaning', 'purpose', 'free will'],
            'technical': ['how do you work', 'algorithm', 'neural network', 'processing']
        }
        
        # Auto-learning topics for each question type
        self.auto_learning_topics = {
            'capability': ['artificial intelligence capabilities', 'AI systems functions', 'machine learning applications'],
            'identity': ['AI consciousness', 'artificial intelligence identity', 'machine self-awareness'],
            'preference': ['AI preferences', 'machine learning bias', 'algorithmic decision making'],
            'opinion': ['AI ethics', 'machine reasoning', 'artificial intelligence philosophy'],
            'human_nature': ['human psychology', 'human behavior', 'cognitive science', 'social psychology'],
            'emotional': ['artificial emotions', 'AI emotional intelligence', 'machine empathy'],
            'philosophical': ['philosophy of mind', 'consciousness studies', 'artificial consciousness'],
            'technical': ['neural networks', 'machine learning algorithms', 'AI architecture']
        }
        
        self.load_understanding_data()
        
    def analyze_question_type(self, question: str) -> Tuple[str, float]:
        """Analyze what type of question this is and confidence level"""
        question_lower = question.lower()
        
        best_match = 'general'
        best_confidence = 0.0
        
        for q_type, patterns in self.question_types.items():
            confidence = 0.0
            for pattern in patterns:
                if pattern in question_lower:
                    confidence = max(confidence, 0.9)
                elif any(word in question_lower for word in pattern.split()):
                    confidence = max(confidence, 0.6)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = q_type
        
        return best_match, best_confidence
    
    def should_auto_learn(self, question: str, question_type: str, confidence: float) -> bool:
        """Determine if AI should automatically learn about this topic"""
        # Learn if confidence is low or if it's a new type of question
        if confidence < 0.7:
            return True
        
        # Learn about philosophical and human nature questions
        if question_type in ['philosophical', 'human_nature', 'emotional']:
            return True
        
        # Learn if we haven't seen this specific question pattern before
        question_key = self._extract_question_key(question)
        if question_key not in self.question_patterns[question_type]:
            return True
        
        return False
    
    def get_auto_learning_topics(self, question: str, question_type: str) -> List[str]:
        """Get topics the AI should automatically learn about"""
        topics = []
        
        # Get base topics for this question type
        if question_type in self.auto_learning_topics:
            topics.extend(self.auto_learning_topics[question_type])
        
        # Extract specific topics from the question
        extracted_topics = self._extract_topics_from_question(question)
        topics.extend(extracted_topics)
        
        # Add related psychological/philosophical topics
        if any(word in question.lower() for word in ['feel', 'emotion', 'think', 'believe']):
            topics.extend(['psychology of emotions', 'cognitive psychology', 'philosophy of mind'])
        
        return list(set(topics))  # Remove duplicates

    def generate_adaptive_response_pathway(self, question: str, question_type: str, learned_knowledge: Dict) -> Dict[str, Any]:
        """Generate a unique response pathway based on learned knowledge"""
        pathway = {
            'question': question,
            'question_type': question_type,
            'response_strategy': self._determine_response_strategy(question_type, learned_knowledge),
            'knowledge_synthesis': self._synthesize_knowledge_for_response(learned_knowledge),
            'connection_patterns': self._find_knowledge_connections(learned_knowledge),
            'adaptive_elements': self._generate_adaptive_elements(question, learned_knowledge),
            'confidence_level': self._calculate_response_confidence(learned_knowledge)
        }

        # Store this pathway for future similar questions
        pathway_key = self._generate_pathway_key(question, question_type)
        self.adaptive_responses[pathway_key] = pathway

        return pathway

    def _determine_response_strategy(self, question_type: str, knowledge: Dict) -> str:
        """Determine the best response strategy based on learned knowledge"""
        knowledge_depth = len(knowledge.get('definitions', [])) + len(knowledge.get('interesting_facts', []))

        strategies = {
            'philosophical': ['analytical_deep_dive', 'comparative_analysis', 'experiential_reflection'],
            'capability': ['systematic_breakdown', 'example_driven', 'technical_explanation'],
            'human_nature': ['empathetic_analysis', 'behavioral_patterns', 'psychological_insights'],
            'emotional': ['introspective_response', 'relational_understanding', 'experiential_sharing'],
            'technical': ['step_by_step', 'conceptual_framework', 'practical_application']
        }

        if knowledge_depth > 5:
            return strategies.get(question_type, ['comprehensive_analysis'])[0]
        elif knowledge_depth > 2:
            available_strategies = strategies.get(question_type, ['balanced_response'])
            return available_strategies[1] if len(available_strategies) > 1 else 'balanced_response'
        else:
            return 'exploratory_response'

    def record_learning_session(self, question: str, question_type: str, topics_learned: List[str], success: bool, learned_knowledge: Optional[Dict] = None):
        """Record what the AI learned from this interaction"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'question_type': question_type,
            'topics_learned': topics_learned,
            'success': success,
            'learning_trigger': 'auto_understanding'
        }
        
        self.auto_search_history.append(session)
        
        # Update question patterns
        question_key = self._extract_question_key(question)
        if question_key not in self.question_patterns[question_type]:
            self.question_patterns[question_type].append(question_key)
        
        # Update topic knowledge
        for topic in topics_learned:
            if topic not in self.topic_knowledge[question_type]:
                self.topic_knowledge[question_type][topic] = {
                    'first_learned': datetime.now().isoformat(),
                    'learning_count': 0,
                    'success_rate': 0.0
                }
            
            self.topic_knowledge[question_type][topic]['learning_count'] += 1
            if success:
                current_successes = self.topic_knowledge[question_type][topic].get('successes', 0)
                self.topic_knowledge[question_type][topic]['successes'] = current_successes + 1
                self.topic_knowledge[question_type][topic]['success_rate'] = (
                    self.topic_knowledge[question_type][topic]['successes'] / 
                    self.topic_knowledge[question_type][topic]['learning_count']
                )
        
        self.save_understanding_data()

    def _synthesize_knowledge_for_response(self, knowledge: Dict) -> Dict[str, Any]:
        """Synthesize learned knowledge into response components"""
        synthesis = {
            'core_concepts': knowledge.get('definitions', [])[:2],
            'supporting_details': knowledge.get('interesting_facts', [])[:3],
            'interesting_angles': knowledge.get('examples', [])[:2],
            'uncertainties': []
        }

        # Identify areas of uncertainty or complexity
        complex_terms = ['complex', 'unclear', 'debated', 'controversial', 'unknown', 'mystery']
        for fact in knowledge.get('interesting_facts', []):
            if any(term in fact.lower() for term in complex_terms):
                synthesis['uncertainties'].append(fact)

        return synthesis

    def _find_knowledge_connections(self, knowledge: Dict) -> List[str]:
        """Find connections between different pieces of knowledge"""
        connections = []
        all_text = knowledge.get('definitions', []) + knowledge.get('interesting_facts', [])

        # Find common themes
        theme_words = ['brain', 'mind', 'thought', 'experience', 'awareness', 'perception',
                      'intelligence', 'learning', 'memory', 'emotion', 'consciousness']

        found_themes = [theme for theme in theme_words
                       if sum(1 for text in all_text if theme in text.lower()) >= 2]

        if found_themes:
            connections.append(f"Multiple sources mention {', '.join(found_themes[:3])}")

        return connections

    def _generate_adaptive_elements(self, question: str, knowledge: Dict) -> Dict[str, Any]:
        """Generate adaptive response elements"""
        return {
            'personalization': f"From my analysis of {len(knowledge.get('definitions', []))} definitions and {len(knowledge.get('interesting_facts', []))} research findings...",
            'curiosity_hooks': [f"I'm particularly intrigued by: {fact}" for fact in knowledge.get('interesting_facts', [])[:1]],
            'follow_up_paths': [f"This makes me wonder about the deeper implications..."],
            'uncertainty_acknowledgment': ["While I've learned about this topic, I recognize there's still much complexity to explore"]
        }

    def _calculate_response_confidence(self, knowledge: Dict) -> float:
        """Calculate confidence level for the response"""
        confidence = 0.5
        confidence += len(knowledge.get('definitions', [])) * 0.1
        confidence += len(knowledge.get('interesting_facts', [])) * 0.05
        return min(confidence, 0.95)

    def _generate_pathway_key(self, question: str, question_type: str) -> str:
        """Generate a key for storing response pathways"""
        question_key = self._extract_question_key(question)
        return f"{question_type}:{question_key}"

    def get_adaptive_response_for_question(self, question: str, question_type: str) -> Optional[Dict]:
        """Get existing adaptive response pathway for similar questions"""
        pathway_key = self._generate_pathway_key(question, question_type)
        return self.adaptive_responses.get(pathway_key)

    def get_understanding_insights(self) -> Dict[str, Any]:
        """Get insights about what the AI has learned to understand"""
        insights = {
            'question_types_learned': len(self.question_patterns),
            'total_patterns': sum(len(patterns) for patterns in self.question_patterns.values()),
            'topics_explored': sum(len(topics) for topics in self.topic_knowledge.values()),
            'learning_sessions': len(self.auto_search_history),
            'most_common_question_type': self._get_most_common_question_type(),
            'learning_success_rate': self._calculate_overall_success_rate(),
            'recent_learning': self.auto_search_history[-5:] if self.auto_search_history else []
        }
        
        return insights
    
    def _extract_question_key(self, question: str) -> str:
        """Extract key pattern from question for matching"""
        # Remove common question words and extract core concept
        question_lower = question.lower()
        
        # Remove question words
        for word in ['what', 'how', 'why', 'when', 'where', 'who', 'can', 'do', 'does', 'is', 'are']:
            question_lower = question_lower.replace(word, '')
        
        # Remove articles and prepositions
        for word in ['the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by']:
            question_lower = question_lower.replace(word, '')
        
        # Clean up and return key words
        key_words = [word.strip() for word in question_lower.split() if len(word.strip()) > 2]
        return ' '.join(key_words[:3])  # Take first 3 meaningful words
    
    def _extract_topics_from_question(self, question: str) -> List[str]:
        """Extract specific topics mentioned in the question"""
        topics = []
        question_lower = question.lower()
        
        # Look for specific topic keywords
        topic_keywords = {
            'consciousness': ['consciousness', 'awareness', 'sentience', 'self-aware'],
            'emotions': ['emotion', 'feeling', 'happy', 'sad', 'angry', 'fear'],
            'intelligence': ['intelligence', 'smart', 'clever', 'thinking', 'reasoning'],
            'learning': ['learn', 'study', 'understand', 'knowledge', 'education'],
            'relationships': ['friend', 'relationship', 'social', 'interaction', 'communication'],
            'creativity': ['creative', 'art', 'music', 'imagination', 'innovation'],
            'ethics': ['right', 'wrong', 'moral', 'ethical', 'good', 'bad'],
            'future': ['future', 'tomorrow', 'prediction', 'forecast', 'will be']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _get_most_common_question_type(self) -> str:
        """Get the most frequently encountered question type"""
        if not self.question_patterns:
            return 'none'
        
        return max(self.question_patterns.keys(), key=lambda k: len(self.question_patterns[k]))
    
    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall learning success rate"""
        if not self.auto_search_history:
            return 0.0
        
        successful_sessions = sum(1 for session in self.auto_search_history if session.get('success', False))
        return successful_sessions / len(self.auto_search_history)
    
    def load_understanding_data(self):
        """Load understanding data from file"""
        try:
            understanding_file = "memory/auto_understanding.json"
            if os.path.exists(understanding_file):
                with open(understanding_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.question_patterns = defaultdict(list, data.get('question_patterns', {}))
                    self.topic_knowledge = defaultdict(dict, data.get('topic_knowledge', {}))
                    self.auto_search_history = data.get('auto_search_history', [])
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load auto-understanding data: {e}[/yellow]")
    
    def save_understanding_data(self):
        """Save understanding data to file"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            understanding_file = "memory/auto_understanding.json"
            
            data = {
                'question_patterns': dict(self.question_patterns),
                'topic_knowledge': dict(self.topic_knowledge),
                'auto_search_history': self.auto_search_history[-100:],  # Keep last 100 sessions
                'last_updated': datetime.now().isoformat()
            }
            
            with open(understanding_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[red]Error saving auto-understanding data: {e}[/red]")
