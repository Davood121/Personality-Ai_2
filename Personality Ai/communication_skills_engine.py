"""
Communication Skills Engine - Advanced English learning and real-time generation
"""
import json
import os
import re
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Generator
from rich.console import Console
from rich.live import Live
from rich.text import Text
from config import *

console = Console()

class CommunicationSkillsEngine:
    def __init__(self):
        self.communication_skills = {
            'vocabulary': 0.6,
            'grammar': 0.5,
            'fluency': 0.4,
            'pronunciation': 0.3,
            'conversation': 0.5,
            'storytelling': 0.4,
            'persuasion': 0.3,
            'empathy': 0.7,
            'clarity': 0.5,
            'engagement': 0.6
        }
        
        # English language components
        self.vocabulary_bank = {
            'basic': [],
            'intermediate': [],
            'advanced': [],
            'technical': [],
            'emotional': [],
            'descriptive': []
        }
        
        self.grammar_patterns = {
            'sentence_structures': [],
            'tenses': [],
            'connectors': [],
            'modifiers': [],
            'question_forms': []
        }
        
        self.conversation_templates = {
            'greetings': [],
            'questions': [],
            'responses': [],
            'transitions': [],
            'conclusions': []
        }
        
        # Real-time generation settings
        self.generation_speed = 0.1  # Seconds between words
        self.thinking_pauses = True
        self.natural_hesitations = True
        
        self.load_communication_data()
        self._initialize_language_components()
    
    def _initialize_language_components(self):
        """Initialize English language components"""
        
        # Basic vocabulary
        self.vocabulary_bank['basic'] = [
            'hello', 'goodbye', 'please', 'thank', 'yes', 'no', 'good', 'bad',
            'big', 'small', 'happy', 'sad', 'love', 'like', 'want', 'need',
            'go', 'come', 'see', 'hear', 'think', 'know', 'understand', 'learn'
        ]
        
        # Intermediate vocabulary
        self.vocabulary_bank['intermediate'] = [
            'fascinating', 'intriguing', 'remarkable', 'significant', 'essential',
            'comprehensive', 'elaborate', 'demonstrate', 'analyze', 'evaluate',
            'perspective', 'approach', 'methodology', 'framework', 'concept'
        ]
        
        # Advanced vocabulary
        self.vocabulary_bank['advanced'] = [
            'sophisticated', 'nuanced', 'paradigm', 'synthesis', 'articulate',
            'eloquent', 'profound', 'intricate', 'multifaceted', 'comprehensive',
            'substantiate', 'corroborate', 'exemplify', 'elucidate', 'illuminate'
        ]
        
        # Emotional vocabulary
        self.vocabulary_bank['emotional'] = [
            'excited', 'curious', 'concerned', 'delighted', 'frustrated',
            'amazed', 'puzzled', 'confident', 'uncertain', 'enthusiastic',
            'empathetic', 'compassionate', 'understanding', 'supportive', 'encouraging'
        ]
        
        # Sentence connectors
        self.grammar_patterns['connectors'] = [
            'however', 'furthermore', 'moreover', 'nevertheless', 'consequently',
            'therefore', 'meanwhile', 'additionally', 'specifically', 'particularly',
            'for instance', 'in other words', 'as a result', 'on the other hand'
        ]
        
        # Conversation starters
        self.conversation_templates['greetings'] = [
            "Hello! How can I help you today?",
            "Hi there! What would you like to discuss?",
            "Good to see you! What's on your mind?",
            "Welcome! I'm excited to chat with you.",
            "Hey! What interesting topic shall we explore?"
        ]
        
        # Question patterns
        self.conversation_templates['questions'] = [
            "What do you think about {topic}?",
            "How would you approach {situation}?",
            "Can you tell me more about {subject}?",
            "What's your experience with {area}?",
            "How do you feel about {concept}?"
        ]
    
    def learn_communication_skills(self, searcher=None, memory=None) -> Dict[str, Any]:
        """Learn and improve communication skills from web and memory"""
        console.print("[bold blue]🗣️ Learning Communication Skills from Web & Memory[/bold blue]")

        learning_session = {
            'timestamp': datetime.now().isoformat(),
            'skills_improved': [],
            'new_vocabulary': [],
            'grammar_patterns_learned': [],
            'conversation_practice': [],
            'web_sources_used': [],
            'memory_insights_used': []
        }

        # Learn from web sources
        if searcher:
            console.print("[cyan]🌐 Learning from web sources...[/cyan]")
            web_learning = self._learn_from_web(searcher)
            learning_session['web_sources_used'] = web_learning['sources_used']
            learning_session['new_vocabulary'].extend(web_learning['vocabulary_learned'])
            learning_session['grammar_patterns_learned'].extend(web_learning['patterns_learned'])

        # Learn from memory
        if memory:
            console.print("[cyan]🧠 Learning from memory and past conversations...[/cyan]")
            memory_learning = self._learn_from_memory(memory)
            learning_session['memory_insights_used'] = memory_learning['insights_used']
            learning_session['new_vocabulary'].extend(memory_learning['vocabulary_learned'])
            learning_session['conversation_practice'].extend(memory_learning['conversation_patterns'])

        # Practice different communication aspects
        skills_to_practice = ['vocabulary', 'grammar', 'fluency', 'conversation']

        for skill in skills_to_practice:
            console.print(f"[yellow]📚 Practicing {skill}...[/yellow]")

            if skill == 'vocabulary':
                new_words = self._practice_vocabulary()
                learning_session['new_vocabulary'].extend(new_words)
                self.communication_skills['vocabulary'] = min(1.0, self.communication_skills['vocabulary'] + 0.05)

            elif skill == 'grammar':
                patterns = self._practice_grammar()
                learning_session['grammar_patterns_learned'].extend(patterns)
                self.communication_skills['grammar'] = min(1.0, self.communication_skills['grammar'] + 0.04)

            elif skill == 'fluency':
                self._practice_fluency()
                self.communication_skills['fluency'] = min(1.0, self.communication_skills['fluency'] + 0.03)

            elif skill == 'conversation':
                practice = self._practice_conversation()
                learning_session['conversation_practice'].append(practice)
                self.communication_skills['conversation'] = min(1.0, self.communication_skills['conversation'] + 0.04)

            learning_session['skills_improved'].append(skill)
            time.sleep(0.5)

        console.print("[green]✅ Communication skills learning complete![/green]")
        self.save_communication_data()
        return learning_session
    
    def _practice_vocabulary(self) -> List[str]:
        """Practice and expand vocabulary"""
        new_words = []
        
        # Learn new words from different categories
        categories = ['intermediate', 'advanced', 'emotional', 'descriptive']
        
        for category in categories:
            if category not in self.vocabulary_bank:
                self.vocabulary_bank[category] = []
            
            # Add new words to vocabulary
            sample_words = [
                f"new_{category}_word_{i}" for i in range(1, 4)
            ]
            
            self.vocabulary_bank[category].extend(sample_words)
            new_words.extend(sample_words)
        
        return new_words
    
    def _practice_grammar(self) -> List[str]:
        """Practice grammar patterns"""
        patterns = [
            "Complex sentence with subordinate clause",
            "Conditional statements (if-then)",
            "Passive voice constructions",
            "Comparative and superlative forms"
        ]
        
        self.grammar_patterns['sentence_structures'].extend(patterns)
        return patterns

    def _learn_from_web(self, searcher) -> Dict[str, Any]:
        """Learn communication skills from web sources"""
        web_learning = {
            'sources_used': [],
            'vocabulary_learned': [],
            'patterns_learned': []
        }

        # Search for communication and language learning topics
        communication_topics = [
            "advanced English vocabulary",
            "effective communication skills",
            "professional writing techniques",
            "conversation skills improvement",
            "grammar patterns English"
        ]

        for topic in communication_topics[:2]:  # Limit to 2 topics per session
            try:
                console.print(f"[dim]  Searching: {topic}[/dim]")
                search_result = searcher.comprehensive_search(topic, 'general')

                if search_result.get('total_sources', 0) > 0:
                    web_learning['sources_used'].append(topic)

                    # Extract vocabulary from search results
                    vocabulary = self._extract_vocabulary_from_search(search_result)
                    web_learning['vocabulary_learned'].extend(vocabulary)

                    # Extract communication patterns
                    patterns = self._extract_patterns_from_search(search_result)
                    web_learning['patterns_learned'].extend(patterns)

                    # Update skills based on web learning
                    self.communication_skills['vocabulary'] = min(1.0, self.communication_skills['vocabulary'] + 0.02)
                    self.communication_skills['clarity'] = min(1.0, self.communication_skills['clarity'] + 0.01)

            except Exception as e:
                console.print(f"[dim red]Web learning failed for {topic}: {e}[/dim red]")

        return web_learning

    def _learn_from_memory(self, memory) -> Dict[str, Any]:
        """Learn communication skills from memory and past conversations"""
        memory_learning = {
            'insights_used': [],
            'vocabulary_learned': [],
            'conversation_patterns': []
        }

        try:
            # Get memory statistics to understand what's available
            memory_stats = memory.get_memory_statistics()
            total_knowledge = memory_stats.get('total_knowledge', 0)

            if total_knowledge > 0:
                console.print(f"[dim]  Analyzing {total_knowledge} memory entries[/dim]")

                # Search for communication-related topics
                communication_topics = [
                    'communication', 'language', 'conversation', 'speaking',
                    'vocabulary', 'grammar', 'english', 'writing'
                ]

                for topic in communication_topics:
                    try:
                        # Retrieve knowledge about communication topics
                        knowledge_entries = memory.retrieve_knowledge(topic, limit=3)

                        for entry in knowledge_entries:
                            # Extract vocabulary from definitions
                            definitions = entry.get('definitions', [])
                            for definition in definitions:
                                words = self._extract_advanced_words(definition)
                                memory_learning['vocabulary_learned'].extend(words)

                            # Extract conversation patterns from examples
                            examples = entry.get('examples', [])
                            for example in examples:
                                pattern = self._extract_conversation_pattern(example)
                                if pattern:
                                    memory_learning['conversation_patterns'].append(pattern)

                            # Extract vocabulary from interesting facts
                            facts = entry.get('interesting_facts', [])
                            for fact in facts:
                                words = self._extract_advanced_words(fact)
                                memory_learning['vocabulary_learned'].extend(words)

                            memory_learning['insights_used'].append(entry.get('topic', topic))

                    except Exception as e:
                        console.print(f"[dim red]Failed to retrieve knowledge for {topic}: {e}[/dim red]")

                # Remove duplicates from vocabulary
                memory_learning['vocabulary_learned'] = list(set(memory_learning['vocabulary_learned']))

                # Update skills based on memory learning
                if memory_learning['vocabulary_learned']:
                    self.communication_skills['vocabulary'] = min(1.0, self.communication_skills['vocabulary'] + 0.02)
                    console.print(f"[dim green]📚 Learned {len(memory_learning['vocabulary_learned'])} words from memory[/dim green]")

                if memory_learning['conversation_patterns']:
                    self.communication_skills['conversation'] = min(1.0, self.communication_skills['conversation'] + 0.01)
                    console.print(f"[dim green]💬 Learned {len(memory_learning['conversation_patterns'])} conversation patterns[/dim green]")

            else:
                console.print("[dim]  No memory entries found to learn from[/dim]")

        except Exception as e:
            console.print(f"[dim red]Memory learning failed: {e}[/dim red]")

        return memory_learning

    def _extract_vocabulary_from_search(self, search_result: Dict[str, Any]) -> List[str]:
        """Extract advanced vocabulary from search results"""
        vocabulary = []

        synthesized = search_result.get('synthesized_results', {})

        # Extract from definitions
        for definition in synthesized.get('definitions', []):
            text = definition.get('text', '')
            words = self._extract_advanced_words(text)
            vocabulary.extend(words)

        # Extract from academic insights
        for insight in synthesized.get('academic_insights', []):
            text = insight.get('text', '')
            words = self._extract_advanced_words(text)
            vocabulary.extend(words)

        # Remove duplicates and limit
        return list(set(vocabulary))[:10]

    def _extract_patterns_from_search(self, search_result: Dict[str, Any]) -> List[str]:
        """Extract communication patterns from search results"""
        patterns = []

        synthesized = search_result.get('synthesized_results', {})

        # Extract patterns from definitions
        for definition in synthesized.get('definitions', []):
            text = definition.get('text', '')
            pattern = self._identify_communication_pattern(text)
            if pattern:
                patterns.append(pattern)

        return patterns[:5]  # Limit to 5 patterns

    def _extract_advanced_words(self, text: str) -> List[str]:
        """Extract advanced vocabulary words from text"""
        if not text:
            return []

        # Simple word extraction - look for longer, sophisticated words
        words = re.findall(r'\b[a-zA-Z]{6,}\b', text.lower())

        # Filter for advanced vocabulary (exclude common words)
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
        }

        advanced_words = [
            word for word in words
            if word not in common_words and len(word) >= 6
        ]

        return advanced_words[:5]  # Limit to 5 words per text

    def _identify_communication_pattern(self, text: str) -> Optional[str]:
        """Identify communication patterns in text"""
        if not text:
            return None

        # Look for communication-related patterns
        if 'effective' in text.lower() and 'communication' in text.lower():
            return "Effective communication techniques"
        elif 'conversation' in text.lower() and ('start' in text.lower() or 'begin' in text.lower()):
            return "Conversation starter patterns"
        elif 'question' in text.lower() and 'response' in text.lower():
            return "Question-response patterns"
        elif 'professional' in text.lower() and ('speak' in text.lower() or 'talk' in text.lower()):
            return "Professional speaking patterns"

        return None

    def _extract_conversation_pattern(self, example: str) -> Optional[Dict[str, Any]]:
        """Extract conversation patterns from examples"""
        if not example or len(example) < 10:
            return None

        # Simple pattern extraction
        if '?' in example:
            return {
                'type': 'question_pattern',
                'example': example[:100],
                'pattern': 'Interrogative structure'
            }
        elif any(word in example.lower() for word in ['however', 'therefore', 'moreover', 'furthermore']):
            return {
                'type': 'transition_pattern',
                'example': example[:100],
                'pattern': 'Logical transition'
            }

        return None

    def _practice_fluency(self):
        """Practice speaking fluency"""
        # Simulate fluency practice
        console.print("[dim]  Practicing natural speech rhythm...[/dim]")
        console.print("[dim]  Working on smooth transitions...[/dim]")
        console.print("[dim]  Reducing hesitations and fillers...[/dim]")
    
    def _practice_conversation(self) -> Dict[str, Any]:
        """Practice conversation skills"""
        return {
            'topic': 'General conversation practice',
            'skills_practiced': ['active listening', 'question asking', 'topic transitions'],
            'improvement_areas': ['natural flow', 'engagement techniques']
        }
    
    def generate_real_time_response(self, prompt: str, style: str = 'natural') -> Generator[str, None, None]:
        """Generate response word by word in real-time"""
        
        # Generate the complete response first
        full_response = self._generate_complete_response(prompt, style)
        
        # Split into words
        words = full_response.split()
        
        # Generate word by word with natural timing
        for i, word in enumerate(words):
            # Add natural pauses
            if self.thinking_pauses and i > 0:
                # Pause after punctuation
                if words[i-1].endswith(('.', '!', '?')):
                    time.sleep(self.generation_speed * 3)
                # Pause after commas
                elif words[i-1].endswith(','):
                    time.sleep(self.generation_speed * 2)
                # Normal pause between words
                else:
                    time.sleep(self.generation_speed)
            
            # Add natural hesitations occasionally
            if self.natural_hesitations and random.random() < 0.05:
                yield "um..."
                time.sleep(self.generation_speed * 2)
            
            yield word
    
    def _generate_complete_response(self, prompt: str, style: str) -> str:
        """Generate a complete response based on communication skills"""
        
        # Analyze prompt to determine response type
        response_type = self._analyze_prompt_type(prompt)
        
        # Select vocabulary level based on skills
        vocab_level = self._select_vocabulary_level()
        
        # Generate response based on type and style
        if response_type == 'question':
            response = self._generate_question_response(prompt, vocab_level, style)
        elif response_type == 'explanation':
            response = self._generate_explanation_response(prompt, vocab_level, style)
        elif response_type == 'conversation':
            response = self._generate_conversation_response(prompt, vocab_level, style)
        else:
            response = self._generate_general_response(prompt, vocab_level, style)
        
        return response
    
    def _analyze_prompt_type(self, prompt: str) -> str:
        """Analyze what type of response is needed"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['what', 'how', 'why', 'when', 'where', '?']):
            return 'question'
        elif any(word in prompt_lower for word in ['explain', 'describe', 'tell me about']):
            return 'explanation'
        elif any(word in prompt_lower for word in ['hello', 'hi', 'chat', 'talk']):
            return 'conversation'
        else:
            return 'general'
    
    def _select_vocabulary_level(self) -> str:
        """Select appropriate vocabulary level based on skills"""
        vocab_skill = self.communication_skills['vocabulary']
        
        if vocab_skill >= 0.8:
            return 'advanced'
        elif vocab_skill >= 0.6:
            return 'intermediate'
        else:
            return 'basic'
    
    def _generate_question_response(self, prompt: str, vocab_level: str, style: str) -> str:
        """Generate response to a question"""
        responses = {
            'basic': [
                "That's a good question. Let me think about it.",
                "I understand what you're asking. Here's what I think.",
                "That's interesting. I can help you with that."
            ],
            'intermediate': [
                "That's a fascinating question that deserves a thoughtful response.",
                "I appreciate your curiosity about this topic. Let me elaborate.",
                "Your question touches on some important concepts I'd like to explore."
            ],
            'advanced': [
                "Your inquiry presents a multifaceted challenge that warrants comprehensive analysis.",
                "This question illuminates several interconnected concepts that I find particularly intriguing.",
                "The complexity of your question allows me to explore various nuanced perspectives."
            ]
        }
        
        base_response = random.choice(responses.get(vocab_level, responses['basic']))
        
        # Add specific content based on the prompt
        if 'artificial intelligence' in prompt.lower():
            base_response += " Artificial intelligence represents a fascinating intersection of technology and human cognition."
        elif 'learning' in prompt.lower():
            base_response += " Learning is a dynamic process that involves continuous adaptation and growth."
        else:
            base_response += " This topic offers many interesting angles to consider."
        
        return base_response
    
    def _generate_explanation_response(self, prompt: str, vocab_level: str, style: str) -> str:
        """Generate an explanatory response"""
        starters = {
            'basic': ["Let me explain this simply.", "Here's how it works.", "I'll break this down for you."],
            'intermediate': ["Allow me to elaborate on this concept.", "I'll provide a comprehensive explanation.", "Let me walk you through this systematically."],
            'advanced': ["I'll elucidate this complex topic through a structured analysis.", "Allow me to articulate the nuanced aspects of this subject.", "I'll provide a sophisticated examination of this phenomenon."]
        }
        
        starter = random.choice(starters.get(vocab_level, starters['basic']))
        
        # Add explanation content
        explanation = " This involves several key components that work together in an integrated system. Each element contributes to the overall functionality and effectiveness of the process."
        
        return starter + explanation
    
    def _generate_conversation_response(self, prompt: str, vocab_level: str, style: str) -> str:
        """Generate a conversational response"""
        greetings = random.choice(self.conversation_templates['greetings'])
        
        follow_up = " I'm here to engage in meaningful dialogue and help you explore any topics that interest you. What would you like to discuss today?"
        
        return greetings + follow_up
    
    def _generate_general_response(self, prompt: str, vocab_level: str, style: str) -> str:
        """Generate a general response"""
        return "I understand your message and I'm ready to provide a thoughtful response. Let me consider the best way to address your point while maintaining clear and effective communication."
    
    def demonstrate_real_time_generation(self, prompt: str):
        """Demonstrate real-time word generation"""
        console.print(f"[bold blue]🗣️ Real-Time Response Generation[/bold blue]")
        console.print(f"[yellow]Prompt: {prompt}[/yellow]")
        console.print("[cyan]AI Response:[/cyan]")
        
        # Create a live display for real-time generation
        response_text = Text()
        
        with Live(response_text, refresh_per_second=10) as live:
            for word in self.generate_real_time_response(prompt):
                response_text.append(word + " ")
                live.update(response_text)
        
        console.print("\n[green]✅ Real-time generation complete![/green]")
    
    def get_communication_status(self) -> Dict[str, Any]:
        """Get current communication skills status"""
        return {
            'communication_skills': self.communication_skills,
            'vocabulary_size': {
                category: len(words) for category, words in self.vocabulary_bank.items()
            },
            'total_vocabulary': sum(len(words) for words in self.vocabulary_bank.values()),
            'grammar_patterns': len(self.grammar_patterns.get('sentence_structures', [])),
            'conversation_templates': len(self.conversation_templates.get('greetings', [])),
            'generation_settings': {
                'speed': self.generation_speed,
                'thinking_pauses': self.thinking_pauses,
                'natural_hesitations': self.natural_hesitations
            },
            'overall_fluency': sum(self.communication_skills.values()) / len(self.communication_skills)
        }
    
    def adjust_generation_speed(self, speed: float):
        """Adjust real-time generation speed"""
        self.generation_speed = max(0.01, min(1.0, speed))
        console.print(f"[green]✅ Generation speed set to {self.generation_speed:.2f} seconds per word[/green]")
    
    def toggle_natural_features(self, thinking_pauses: bool = None, hesitations: bool = None):
        """Toggle natural speech features"""
        if thinking_pauses is not None:
            self.thinking_pauses = thinking_pauses
        if hesitations is not None:
            self.natural_hesitations = hesitations

        console.print(f"[green]✅ Natural features updated: Pauses={self.thinking_pauses}, Hesitations={self.natural_hesitations}[/green]")

    def learn_from_conversation(self, user_input: str, ai_response: str):
        """Learn communication skills from ongoing conversations"""
        try:
            # Extract vocabulary from user input
            user_words = self._extract_advanced_words(user_input)
            if user_words:
                # Add new words to vocabulary bank
                for word in user_words[:3]:  # Limit to 3 words per conversation
                    if word not in self.vocabulary_bank['intermediate']:
                        self.vocabulary_bank['intermediate'].append(word)
                        console.print(f"[dim green]📚 Learned new word: {word}[/dim green]")

            # Analyze conversation patterns
            if '?' in user_input:
                # User asked a question - learn question patterns
                self.conversation_templates['questions'].append(user_input[:100])
                self.communication_skills['conversation'] = min(1.0, self.communication_skills['conversation'] + 0.001)

            # Learn from successful responses
            if len(ai_response) > 50:  # Substantial response
                # Extract sophisticated words from AI's own response
                ai_words = self._extract_advanced_words(ai_response)
                for word in ai_words[:2]:
                    if word not in self.vocabulary_bank['advanced']:
                        self.vocabulary_bank['advanced'].append(word)

                # Improve fluency based on response length and complexity
                self.communication_skills['fluency'] = min(1.0, self.communication_skills['fluency'] + 0.001)
                self.communication_skills['clarity'] = min(1.0, self.communication_skills['clarity'] + 0.001)

        except Exception as e:
            console.print(f"[dim red]Conversation learning failed: {e}[/dim red]")

    def adaptive_vocabulary_expansion(self, topic: str, searcher=None):
        """Adaptively expand vocabulary based on current conversation topic"""
        if not searcher or not topic:
            return

        try:
            console.print(f"[dim]🔍 Expanding vocabulary for topic: {topic}[/dim]")

            # Search for topic-specific vocabulary
            search_query = f"{topic} advanced vocabulary terminology"
            search_result = searcher.comprehensive_search(search_query, 'general')

            if search_result.get('total_sources', 0) > 0:
                # Extract specialized vocabulary
                new_vocabulary = self._extract_vocabulary_from_search(search_result)

                # Add to technical vocabulary
                for word in new_vocabulary[:5]:
                    if word not in self.vocabulary_bank['technical']:
                        self.vocabulary_bank['technical'].append(word)
                        console.print(f"[dim green]🔧 Added technical term: {word}[/dim green]")

                # Improve vocabulary skill
                self.communication_skills['vocabulary'] = min(1.0, self.communication_skills['vocabulary'] + 0.01)

        except Exception as e:
            console.print(f"[dim red]Adaptive vocabulary expansion failed: {e}[/dim red]")

    def analyze_communication_effectiveness(self, response: str, user_feedback: str = None) -> Dict[str, Any]:
        """Analyze the effectiveness of AI's communication"""
        analysis = {
            'word_count': len(response.split()),
            'sentence_count': len([s for s in response.split('.') if s.strip()]),
            'vocabulary_level': 'basic',
            'clarity_score': 0.5,
            'engagement_score': 0.5,
            'improvement_suggestions': []
        }

        # Analyze vocabulary level
        advanced_words = self._extract_advanced_words(response)
        if len(advanced_words) >= 3:
            analysis['vocabulary_level'] = 'advanced'
            analysis['clarity_score'] += 0.2
        elif len(advanced_words) >= 1:
            analysis['vocabulary_level'] = 'intermediate'
            analysis['clarity_score'] += 0.1

        # Analyze engagement
        if '?' in response:
            analysis['engagement_score'] += 0.2
        if any(word in response.lower() for word in ['interesting', 'fascinating', 'exciting', 'amazing']):
            analysis['engagement_score'] += 0.1

        # Generate improvement suggestions
        if analysis['word_count'] < 20:
            analysis['improvement_suggestions'].append("Consider providing more detailed responses")
        if analysis['vocabulary_level'] == 'basic':
            analysis['improvement_suggestions'].append("Try using more sophisticated vocabulary")
        if '?' not in response:
            analysis['improvement_suggestions'].append("Consider asking engaging questions")

        # Learn from analysis
        if analysis['clarity_score'] > 0.7:
            self.communication_skills['clarity'] = min(1.0, self.communication_skills['clarity'] + 0.005)
        if analysis['engagement_score'] > 0.7:
            self.communication_skills['engagement'] = min(1.0, self.communication_skills['engagement'] + 0.005)

        return analysis
    
    def load_communication_data(self):
        """Load communication skills data"""
        try:
            comm_file = "memory/communication_skills.json"
            if os.path.exists(comm_file):
                with open(comm_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.communication_skills = data.get('communication_skills', self.communication_skills)
                    self.vocabulary_bank = data.get('vocabulary_bank', self.vocabulary_bank)
                    self.grammar_patterns = data.get('grammar_patterns', self.grammar_patterns)
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load communication data: {e}[/dim yellow]")
    
    def save_communication_data(self):
        """Save communication skills data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            comm_file = "memory/communication_skills.json"
            
            data = {
                'communication_skills': self.communication_skills,
                'vocabulary_bank': self.vocabulary_bank,
                'grammar_patterns': self.grammar_patterns,
                'conversation_templates': self.conversation_templates,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(comm_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[dim red]Error saving communication data: {e}[/dim red]")
