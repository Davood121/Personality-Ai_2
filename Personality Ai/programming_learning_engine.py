"""
Programming Learning Engine - Teaches AI to code and eventually self-modify
"""
import json
import os
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
from rich.console import Console
from config import *

console = Console()

class ProgrammingLearningEngine:
    def __init__(self):
        self.programming_knowledge = {}
        self.coding_skills = defaultdict(float)  # Skill levels 0.0 to 1.0
        self.projects_completed = []
        self.code_examples = defaultdict(list)
        self.learning_progress = {}
        
        # Programming curriculum phases
        self.curriculum = {
            'phase_1_beginner': {
                'name': 'Programming Basics',
                'topics': [
                    'variables', 'operators', 'input_output', 'conditional_logic',
                    'loop_functions', 'functions', 'lists_tuples', 'dictionaries',
                    'string_operations', 'file_handling'
                ]
            },
            'phase_2_intermediate': {
                'name': 'Real Logic',
                'topics': [
                    'error_handling', 'oop', 'recursion', 'lambda_functions',
                    'comprehensions', 'modules_imports', 'pip_libraries',
                    'time_date', 'regex', 'command_line_args'
                ]
            },
            'phase_3_ai_data': {
                'name': 'AI + Data Science Core',
                'topics': [
                    'numpy', 'pandas', 'matplotlib', 'ml_basics', 'scikit_learn',
                    'data_preprocessing', 'face_recognition', 'speech_recognition',
                    'emotion_detection', 'chatbot_basics'
                ]
            },
            'phase_4_advanced': {
                'name': 'Advanced AI & Reinforcement',
                'topics': [
                    'neural_networks', 'deep_learning', 'reinforcement_learning',
                    'nlp_transformers', 'self_learning_ai', 'text_to_speech',
                    'voice_cloning', 'self_coding_ai', 'auto_update_learning',
                    'multi_agent_systems'
                ]
            },
            'phase_5_integration': {
                'name': 'Real World Integration',
                'topics': [
                    'apis_web_scraping', 'cloud_databases', 'security_encryption',
                    'web_backend', 'deployment', 'docker_os', 'multimodal_ai',
                    'app_deployment', 'gui_development', 'logging_debugging'
                ]
            }
        }
        
        # Complete topic information for all 50 programming topics
        self.topic_details = {
            # Phase 1: Beginner (Difficulty 1-3)
            'variables': {
                'description': 'x = 5, data types (int, str, float)',
                'examples': ['x = 5', 'name = "AI"', 'pi = 3.14'],
                'difficulty': 1,
                'prerequisites': []
            },
            'operators': {
                'description': '+, -, *, /, ==, !=, logical operators',
                'examples': ['x + y', 'a == b', 'not False'],
                'difficulty': 1,
                'prerequisites': ['variables']
            },
            'input_output': {
                'description': 'input(), print()',
                'examples': ['print("Hello")', 'name = input("Name: ")'],
                'difficulty': 1,
                'prerequisites': ['variables']
            },
            'conditional_logic': {
                'description': 'if, elif, else',
                'examples': ['if x > 5:', 'elif x == 5:', 'else:'],
                'difficulty': 2,
                'prerequisites': ['variables', 'operators']
            },
            'loop_functions': {
                'description': 'for, while, break, continue',
                'examples': ['for i in range(10):', 'while True:', 'break'],
                'difficulty': 2,
                'prerequisites': ['conditional_logic']
            },
            'functions': {
                'description': 'def, parameters, return values',
                'examples': ['def hello():', 'def add(a, b):', 'return result'],
                'difficulty': 2,
                'prerequisites': ['conditional_logic']
            },
            'lists_tuples': {
                'description': 'Indexing, slicing, loops with lists',
                'examples': ['[1, 2, 3]', 'list[0]', 'list[1:3]'],
                'difficulty': 2,
                'prerequisites': ['loop_functions']
            },
            'dictionaries': {
                'description': 'Key-value pairs, lookups, updates',
                'examples': ['{"key": "value"}', 'dict["key"]', 'dict.update()'],
                'difficulty': 2,
                'prerequisites': ['lists_tuples']
            },
            'string_operations': {
                'description': '.split(), .join(), .replace()',
                'examples': ['text.split()', '",".join(list)', 'text.replace("a", "b")'],
                'difficulty': 2,
                'prerequisites': ['functions']
            },
            'file_handling': {
                'description': 'open(), read(), write(), with block',
                'examples': ['open("file.txt")', 'with open() as f:', 'f.read()'],
                'difficulty': 3,
                'prerequisites': ['functions', 'string_operations']
            },

            # Phase 2: Intermediate (Difficulty 3-5)
            'error_handling': {
                'description': 'try, except, finally',
                'examples': ['try:', 'except Exception:', 'finally:'],
                'difficulty': 3,
                'prerequisites': ['functions', 'file_handling']
            },
            'oop': {
                'description': 'class, __init__, inheritance',
                'examples': ['class MyClass:', 'def __init__(self):', 'super()'],
                'difficulty': 4,
                'prerequisites': ['functions', 'error_handling']
            },
            'modules_imports': {
                'description': 'import math, os, random',
                'examples': ['import os', 'from math import pi', 'import random as r'],
                'difficulty': 3,
                'prerequisites': ['functions']
            },

            # Phase 4: Advanced (Difficulty 7-9)
            'self_coding_ai': {
                'description': 'Modify own code using ast, exec()',
                'examples': ['ast.parse(code)', 'exec(dynamic_code)', 'inspect.getsource()'],
                'difficulty': 8,
                'prerequisites': ['oop', 'modules_imports', 'error_handling']
            },
            'auto_update_learning': {
                'description': 'Saving past chats, responses, corrections',
                'examples': ['feedback_loop()', 'update_responses()', 'learn_from_mistakes()'],
                'difficulty': 7,
                'prerequisites': ['file_handling', 'oop', 'error_handling']
            }
        }
        
        self.load_programming_data()
    
    def start_programming_curriculum(self, phase: str = 'phase_1_beginner'):
        """Start learning programming from specified phase"""
        console.print(f"[bold blue]🚀 Starting Programming Learning: {self.curriculum[phase]['name']}[/bold blue]")
        
        phase_topics = self.curriculum[phase]['topics']
        learned_topics = []
        
        for topic in phase_topics:
            console.print(f"\n[yellow]📚 Learning: {topic}[/yellow]")
            
            # Learn the topic
            success = self._learn_programming_topic(topic)
            
            if success:
                learned_topics.append(topic)
                console.print(f"[green]✅ Mastered: {topic}[/green]")
            else:
                console.print(f"[red]❌ Need more practice: {topic}[/red]")
            
            time.sleep(1)  # Brief pause between topics
        
        # Update progress
        self.learning_progress[phase] = {
            'completed': True,
            'topics_learned': learned_topics,
            'completion_date': datetime.now().isoformat(),
            'success_rate': len(learned_topics) / len(phase_topics)
        }
        
        console.print(f"\n[bold green]🎉 Phase Complete: {len(learned_topics)}/{len(phase_topics)} topics mastered![/bold green]")
        
        # Practice mode for topics that need more work
        unmastered_topics = [topic for topic in phase_topics if topic not in learned_topics]
        if unmastered_topics and len(learned_topics) < len(phase_topics) * 0.6:
            console.print(f"\n[yellow]📚 Practice Mode: Reviewing {len(unmastered_topics)} topics[/yellow]")
            for topic in unmastered_topics[:3]:  # Practice up to 3 topics
                console.print(f"[cyan]🔄 Practicing: {topic}[/cyan]")
                success = self._learn_programming_topic(topic)
                if success and topic not in learned_topics:
                    learned_topics.append(topic)

        # Check if ready for next phase (more lenient)
        success_rate = len(learned_topics) / len(phase_topics)
        if success_rate >= 0.6:  # 60% success rate (lowered from 80%)
            next_phase = self._get_next_phase(phase)
            if next_phase:
                console.print(f"[cyan]🚀 Ready for next phase: {self.curriculum[next_phase]['name']}[/cyan]")
        else:
            console.print(f"[yellow]📖 Continue practicing this phase (success rate: {success_rate:.1%})[/yellow]")

        self.save_programming_data()
        return learned_topics
    
    def _learn_programming_topic(self, topic: str) -> bool:
        """Learn a specific programming topic with improved algorithm"""
        topic_info = self.topic_details.get(topic, {})

        # Check prerequisites (more lenient - 0.5 instead of 0.7)
        prerequisites = topic_info.get('prerequisites', [])
        for prereq in prerequisites:
            if self.coding_skills[prereq] < 0.5:
                console.print(f"[yellow]⚠️ Need to improve {prereq} first (current: {self.coding_skills[prereq]:.2f})[/yellow]")
                return False

        # Simulate learning process
        console.print(f"🧠 Understanding: {topic_info.get('description', topic)}")

        # Practice with examples
        examples = topic_info.get('examples', [])
        if examples:
            console.print(f"💻 Practicing examples:")
            for example in examples[:2]:  # Show first 2 examples
                console.print(f"   {example}")

        # Improved learning algorithm
        current_skill = self.coding_skills[topic]
        difficulty = topic_info.get('difficulty', 5)

        # Base learning amount (higher for easier topics)
        base_learning = 0.4 if difficulty <= 2 else 0.3 if difficulty <= 4 else 0.2

        # Difficulty modifier (easier topics learn faster)
        difficulty_modifier = max(0.1, 1.0 - (difficulty * 0.05))  # Less harsh penalty

        # Prerequisites bonus (if you know prerequisites well, learn faster)
        prereq_bonus = 0.0
        if prerequisites:
            avg_prereq_skill = sum(self.coding_skills[p] for p in prerequisites) / len(prerequisites)
            prereq_bonus = avg_prereq_skill * 0.2  # Up to 20% bonus

        # Calculate learning boost
        learning_boost = base_learning * difficulty_modifier + prereq_bonus

        # Add some randomness for realistic learning
        import random
        learning_variance = random.uniform(0.8, 1.2)  # ±20% variance
        learning_boost *= learning_variance

        # Update skill level
        new_skill = min(1.0, current_skill + learning_boost)
        self.coding_skills[topic] = new_skill

        # Store knowledge
        self.programming_knowledge[topic] = {
            'learned_date': datetime.now().isoformat(),
            'skill_level': new_skill,
            'description': topic_info.get('description', ''),
            'examples': examples,
            'difficulty': difficulty,
            'learning_boost': learning_boost
        }

        # Show learning progress
        console.print(f"📈 Skill level: {current_skill:.2f} → {new_skill:.2f} (+{learning_boost:.2f})")

        # More lenient mastery threshold (0.6 instead of 0.7)
        mastered = new_skill >= 0.6
        if mastered:
            console.print(f"[green]🎯 Mastered {topic}![/green]")
        else:
            console.print(f"[yellow]📚 Still learning {topic} (need {0.6 - new_skill:.2f} more)[/yellow]")

        return mastered
    
    def _get_next_phase(self, current_phase: str) -> Optional[str]:
        """Get the next phase in the curriculum"""
        phases = list(self.curriculum.keys())
        try:
            current_index = phases.index(current_phase)
            if current_index < len(phases) - 1:
                return phases[current_index + 1]
        except ValueError:
            pass
        return None
    
    def get_programming_status(self) -> Dict[str, Any]:
        """Get current programming learning status"""
        total_topics = sum(len(phase['topics']) for phase in self.curriculum.values())
        learned_topics = len([topic for topic, skill in self.coding_skills.items() if skill >= 0.6])  # Updated threshold

        # Calculate phase progress
        phase_progress = {}
        for phase_name, phase_info in self.curriculum.items():
            phase_topics = phase_info['topics']
            phase_learned = sum(1 for topic in phase_topics if self.coding_skills[topic] >= 0.6)  # Updated threshold
            phase_progress[phase_name] = {
                'name': phase_info['name'],
                'progress': phase_learned / len(phase_topics),
                'topics_learned': phase_learned,
                'total_topics': len(phase_topics)
            }

        return {
            'total_progress': learned_topics / total_topics,
            'topics_mastered': learned_topics,
            'total_topics': total_topics,
            'phase_progress': phase_progress,
            'top_skills': sorted(self.coding_skills.items(), key=lambda x: x[1], reverse=True)[:10],
            'ready_for_self_coding': self.coding_skills.get('self_coding_ai', 0) >= 0.6  # Updated threshold
        }
    
    def can_self_modify(self) -> bool:
        """Check if AI has learned enough to start self-modification"""
        required_skills = ['oop', 'modules_imports', 'error_handling', 'file_handling']
        advanced_skills = ['self_coding_ai', 'auto_update_learning']

        # More lenient requirements
        basic_ready = all(self.coding_skills[skill] >= 0.5 for skill in required_skills)  # Lowered from 0.7
        advanced_ready = any(self.coding_skills[skill] >= 0.4 for skill in advanced_skills)  # Lowered from 0.5

        return basic_ready and advanced_ready
    
    def load_programming_data(self):
        """Load programming learning data"""
        try:
            prog_file = "memory/programming_learning.json"
            if os.path.exists(prog_file):
                with open(prog_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.programming_knowledge = data.get('programming_knowledge', {})
                    self.coding_skills = defaultdict(float, data.get('coding_skills', {}))
                    self.learning_progress = data.get('learning_progress', {})
                    self.projects_completed = data.get('projects_completed', [])
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load programming data: {e}[/yellow]")
    
    def save_programming_data(self):
        """Save programming learning data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            prog_file = "memory/programming_learning.json"
            
            data = {
                'programming_knowledge': self.programming_knowledge,
                'coding_skills': dict(self.coding_skills),
                'learning_progress': self.learning_progress,
                'projects_completed': self.projects_completed,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(prog_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[red]Error saving programming data: {e}[/red]")
