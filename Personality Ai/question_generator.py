"""
Intelligent Question Generation System
Creates infinite, progressively advanced questions about personality topics
"""
import random
import json
import time
from typing import List, Dict, Any, Set
from datetime import datetime
from config import *
from rich.console import Console

console = Console()

class QuestionGenerator:
    def __init__(self):
        self.question_templates = self._initialize_templates()
        self.used_questions = set()
        self.complexity_modifiers = self._initialize_complexity_modifiers()
        self.topic_connections = {}
        self.question_history = []
        self.load_question_archive()
        
    def _initialize_templates(self) -> Dict[str, List[str]]:
        """Initialize question templates by category and complexity"""
        return {
            'basic_definition': [
                "What is {topic}?",
                "How would you define {topic}?",
                "What does {topic} mean in psychology?",
                "Can you explain {topic} in simple terms?",
                "What are the key characteristics of {topic}?"
            ],
            'mechanisms': [
                "How does {topic} work?",
                "What causes {topic}?",
                "What are the underlying mechanisms of {topic}?",
                "How is {topic} formed or developed?",
                "What processes are involved in {topic}?"
            ],
            'applications': [
                "How is {topic} used in real life?",
                "What are practical applications of {topic}?",
                "How can understanding {topic} help people?",
                "Where do we see {topic} in everyday situations?",
                "How is {topic} applied in therapy or counseling?"
            ],
            'relationships': [
                "How does {topic} relate to {related_topic}?",
                "What is the connection between {topic} and {related_topic}?",
                "How do {topic} and {related_topic} influence each other?",
                "What are the similarities between {topic} and {related_topic}?",
                "How does {topic} interact with {related_topic}?"
            ],
            'development': [
                "How does {topic} develop over time?",
                "What factors influence the development of {topic}?",
                "How does {topic} change throughout life?",
                "What role does age play in {topic}?",
                "How do childhood experiences affect {topic}?"
            ],
            'measurement': [
                "How is {topic} measured or assessed?",
                "What tools are used to evaluate {topic}?",
                "How can we test for {topic}?",
                "What are reliable ways to measure {topic}?",
                "How do psychologists assess {topic}?"
            ],
            'cultural_differences': [
                "How does {topic} vary across cultures?",
                "What cultural factors influence {topic}?",
                "How do different societies view {topic}?",
                "Are there universal aspects of {topic}?",
                "How does culture shape {topic}?"
            ],
            'research': [
                "What does recent research say about {topic}?",
                "What are the latest findings on {topic}?",
                "What research methods are used to study {topic}?",
                "What are the current debates about {topic}?",
                "What gaps exist in {topic} research?"
            ],
            'advanced_analysis': [
                "What are the neurobiological bases of {topic}?",
                "How does {topic} relate to brain structure and function?",
                "What genetic factors contribute to {topic}?",
                "How do environmental and genetic factors interact in {topic}?",
                "What are the evolutionary perspectives on {topic}?"
            ],
            'philosophical': [
                "What are the ethical implications of {topic}?",
                "How does {topic} relate to human nature?",
                "What philosophical questions does {topic} raise?",
                "How does {topic} challenge our understanding of humanity?",
                "What are the moral considerations of {topic}?"
            ]
        }
        
    def _initialize_complexity_modifiers(self) -> Dict[float, List[str]]:
        """Initialize complexity modifiers for different levels"""
        return {
            1.0: ["basic", "simple", "fundamental", "core"],
            1.5: ["intermediate", "detailed", "comprehensive", "thorough"],
            2.0: ["advanced", "complex", "sophisticated", "nuanced"],
            2.5: ["expert-level", "cutting-edge", "theoretical", "research-based"],
            3.0: ["groundbreaking", "revolutionary", "paradigm-shifting", "interdisciplinary"]
        }
        
    def generate_questions(self, topic: str, complexity_level: float = 1.0, count: int = 5) -> List[Dict[str, Any]]:
        """Generate questions about a topic with specified complexity"""
        questions = []
        
        # Determine which question categories to use based on complexity
        available_categories = self._get_categories_for_complexity(complexity_level)
        
        for _ in range(count):
            category = random.choice(available_categories)
            template = random.choice(self.question_templates[category])
            
            # Generate related topics for relationship questions
            related_topic = self._get_related_topic(topic) if '{related_topic}' in template else None
            
            # Format the question
            if related_topic:
                question_text = template.format(topic=topic, related_topic=related_topic)
            else:
                question_text = template.format(topic=topic)
                
            # Add complexity modifiers
            question_text = self._add_complexity_modifiers(question_text, complexity_level)
            
            # Avoid duplicates
            if question_text not in self.used_questions:
                question_data = {
                    'question': question_text,
                    'topic': topic,
                    'category': category,
                    'complexity': complexity_level,
                    'related_topic': related_topic,
                    'generated_at': datetime.now().isoformat(),
                    'answered': False
                }
                
                questions.append(question_data)
                self.used_questions.add(question_text)
                self.question_history.append(question_data)
                
        console.print(f"🤔 Generated {len(questions)} questions about [cyan]{topic}[/cyan] (complexity: {complexity_level})")
        return questions
        
    def _get_categories_for_complexity(self, complexity_level: float) -> List[str]:
        """Get appropriate question categories for complexity level"""
        if complexity_level <= 1.0:
            return ['basic_definition', 'mechanisms', 'applications']
        elif complexity_level <= 1.5:
            return ['basic_definition', 'mechanisms', 'applications', 'relationships', 'development']
        elif complexity_level <= 2.0:
            return ['mechanisms', 'applications', 'relationships', 'development', 'measurement', 'cultural_differences']
        elif complexity_level <= 2.5:
            return ['relationships', 'development', 'measurement', 'cultural_differences', 'research', 'advanced_analysis']
        else:
            return ['research', 'advanced_analysis', 'philosophical', 'cultural_differences']
            
    def _get_related_topic(self, topic: str) -> str:
        """Get a related topic for relationship questions"""
        # Define topic relationships
        topic_relationships = {
            'personality': ['behavior', 'emotions', 'cognition', 'social skills', 'mental health'],
            'behavior': ['personality', 'motivation', 'learning', 'environment', 'genetics'],
            'emotions': ['personality', 'cognition', 'behavior', 'relationships', 'mental health'],
            'communication': ['personality', 'social skills', 'relationships', 'culture', 'psychology'],
            'social skills': ['personality', 'communication', 'relationships', 'emotional intelligence'],
            'mental health': ['personality', 'emotions', 'behavior', 'stress', 'relationships'],
            'motivation': ['personality', 'behavior', 'goals', 'emotions', 'success'],
            'leadership': ['personality', 'communication', 'social skills', 'influence', 'management']
        }
        
        # Find related topics
        topic_lower = topic.lower()
        for key, related_list in topic_relationships.items():
            if key in topic_lower or topic_lower in key:
                return random.choice(related_list)
                
        # Default related topics
        default_related = ['human behavior', 'psychology', 'social interaction', 'personal development', 'mental processes']
        return random.choice(default_related)
        
    def _add_complexity_modifiers(self, question: str, complexity_level: float) -> str:
        """Add complexity modifiers to questions"""
        if complexity_level <= 1.0:
            return question
            
        # Find appropriate modifiers
        modifier_level = min(3.0, complexity_level)
        available_modifiers = []
        
        for level, modifiers in self.complexity_modifiers.items():
            if level <= modifier_level:
                available_modifiers.extend(modifiers)
                
        if available_modifiers and random.random() < 0.3:  # 30% chance to add modifier
            modifier = random.choice(available_modifiers)
            
            # Insert modifier appropriately
            if question.startswith("What"):
                question = question.replace("What", f"What {modifier}")
            elif question.startswith("How"):
                question = question.replace("How", f"How {modifier}")
            else:
                question = f"From a {modifier} perspective, {question.lower()}"
                
        return question
        
    def generate_follow_up_questions(self, answered_question: Dict[str, Any], learned_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate follow-up questions based on what was learned"""
        follow_ups = []
        topic = answered_question['topic']
        complexity = answered_question['complexity'] + 0.2  # Increase complexity slightly
        
        # Generate questions based on what was learned
        if 'key_concepts' in learned_info:
            for concept in learned_info['key_concepts'][:2]:  # Take first 2 concepts
                concept_questions = self.generate_questions(concept, complexity, 1)
                follow_ups.extend(concept_questions)
                
        if 'interesting_facts' in learned_info:
            # Generate deeper questions about interesting facts
            for fact in learned_info['interesting_facts'][:1]:  # Take one fact
                fact_questions = [
                    f"What are the implications of the fact that {fact[:50]}...?",
                    f"How does the finding that {fact[:50]}... affect our understanding?",
                    f"What further research is needed on {fact[:50]}...?"
                ]
                for q in fact_questions[:1]:  # Take one fact question
                    follow_ups.append({
                        'question': q,
                        'topic': topic,
                        'category': 'research',
                        'complexity': complexity,
                        'generated_at': datetime.now().isoformat(),
                        'answered': False,
                        'is_follow_up': True
                    })
                
        return follow_ups
        
    def get_next_learning_topics(self, current_knowledge: Dict[str, Any], complexity_level: float) -> List[str]:
        """Suggest next topics to learn about based on current knowledge"""
        learned_topics = set(current_knowledge.keys())
        
        # Start with core topics if just beginning
        if complexity_level < 1.5:
            remaining_core = [topic for topic in CORE_PERSONALITY_TOPICS if topic not in learned_topics]
            if remaining_core:
                return random.sample(remaining_core, min(3, len(remaining_core)))
                
        # Move to advanced topics
        remaining_advanced = [topic for topic in ADVANCED_TOPICS if topic not in learned_topics]
        if remaining_advanced:
            return random.sample(remaining_advanced, min(3, len(remaining_advanced)))
            
        # Generate new topic combinations
        base_topics = ['personality', 'behavior', 'psychology', 'communication', 'emotions']
        modifiers = ['advanced', 'clinical', 'social', 'cognitive', 'developmental', 'cultural']
        
        new_topics = []
        for _ in range(3):
            base = random.choice(base_topics)
            modifier = random.choice(modifiers)
            new_topics.append(f"{modifier} {base}")
            
        return new_topics
        
    def save_question_archive(self):
        """Save question history to file"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            with open(QUESTIONS_ARCHIVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.question_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Error saving question archive: {e}[/red]")
            
    def load_question_archive(self):
        """Load question history from file"""
        try:
            if os.path.exists(QUESTIONS_ARCHIVE_FILE):
                with open(QUESTIONS_ARCHIVE_FILE, 'r', encoding='utf-8') as f:
                    self.question_history = json.load(f)
                    # Rebuild used questions set
                    self.used_questions = {q['question'] for q in self.question_history}
        except Exception as e:
            console.print(f"[yellow]Could not load question archive: {e}[/yellow]")
            
    def get_question_stats(self) -> Dict[str, Any]:
        """Get statistics about generated questions"""
        if not self.question_history:
            return {'total_questions': 0}
            
        answered_count = sum(1 for q in self.question_history if q.get('answered', False))
        categories = {}
        complexity_levels = {}
        
        for q in self.question_history:
            cat = q.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            comp = q.get('complexity', 1.0)
            comp_range = f"{comp:.1f}-{comp+0.4:.1f}"
            complexity_levels[comp_range] = complexity_levels.get(comp_range, 0) + 1
            
        return {
            'total_questions': len(self.question_history),
            'answered_questions': answered_count,
            'unanswered_questions': len(self.question_history) - answered_count,
            'categories': categories,
            'complexity_distribution': complexity_levels,
            'average_complexity': sum(q.get('complexity', 1.0) for q in self.question_history) / len(self.question_history)
        }
