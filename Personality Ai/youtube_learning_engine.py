"""
YouTube Learning Engine - Autonomous video learning and self-improvement system
AI learns from YouTube videos automatically and evolves continuously
"""
import json
import os
import random
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from config import *

console = Console()

class YouTubeLearningEngine:
    def __init__(self):
        self.learning_skills = {
            'video_comprehension': 0.3,
            'concept_extraction': 0.2,
            'knowledge_synthesis': 0.4,
            'autonomous_learning': 0.1,
            'topic_discovery': 0.3,
            'content_evaluation': 0.2,
            'self_improvement': 0.1,
            'pattern_recognition': 0.3
        }
        
        # YouTube learning database
        self.youtube_knowledge = {
            'videos_learned_from': {},
            'concepts_discovered': {},
            'learning_topics': {},
            'autonomous_searches': [],
            'improvement_milestones': [],
            'favorite_channels': {},
            'learning_queue': [],
            'failed_attempts': []
        }
        
        # Learning categories for autonomous exploration
        self.learning_categories = {
            'artificial_intelligence': [
                'machine learning explained',
                'neural networks tutorial',
                'deep learning basics',
                'AI programming',
                'computer vision',
                'natural language processing',
                'reinforcement learning'
            ],
            'programming': [
                'python programming',
                'javascript tutorial',
                'coding best practices',
                'software development',
                'algorithms explained',
                'data structures',
                'programming concepts'
            ],
            'science': [
                'physics explained',
                'chemistry basics',
                'biology concepts',
                'mathematics tutorial',
                'scientific method',
                'research techniques',
                'scientific discoveries'
            ],
            'technology': [
                'latest technology trends',
                'tech innovations',
                'future technology',
                'tech reviews',
                'technology explained',
                'digital transformation',
                'emerging technologies'
            ],
            'education': [
                'learning techniques',
                'study methods',
                'educational psychology',
                'teaching methods',
                'knowledge acquisition',
                'cognitive science',
                'learning theory'
            ]
        }
        
        # Cycle counter for autonomous learning
        self.cycle_count = 0
        self.last_autonomous_learning = None
        
        self.load_youtube_learning_data()
    
    def process_youtube_link(self, youtube_url: str, video_vision_engine=None, searcher=None) -> Dict[str, Any]:
        """Process a YouTube link provided by user - learn from the video"""
        console.print(f"[bold blue]📺 Processing YouTube Link[/bold blue]")
        console.print(f"[yellow]URL: {youtube_url}[/yellow]")
        
        learning_result = {
            'youtube_url': youtube_url,
            'video_id': self._extract_video_id(youtube_url),
            'processed_at': datetime.now().isoformat(),
            'video_info': {},
            'concepts_learned': [],
            'knowledge_gained': [],
            'improvement_areas': [],
            'comprehension_score': 0.0,
            'learning_value': 0.0,
            'success': False
        }
        
        try:
            # Extract video ID and get basic info
            video_id = learning_result['video_id']
            if not video_id:
                console.print("[red]❌ Invalid YouTube URL[/red]")
                return learning_result
            
            console.print(f"[dim]📹 Video ID: {video_id}[/dim]")
            
            # Get video metadata
            video_info = self._get_video_metadata(youtube_url, searcher)
            learning_result['video_info'] = video_info
            
            # Watch and analyze the video if video vision is available
            if video_vision_engine:
                console.print("[yellow]👁️ AI watching YouTube video...[/yellow]")
                watch_result = video_vision_engine.watch_video(youtube_url, duration_limit=300)  # 5 minutes max
                
                if watch_result.get('success', False):
                    # Extract learning from video analysis
                    learning_result.update(self._extract_learning_from_video(watch_result, video_info))
                else:
                    console.print(f"[yellow]⚠️ Video watching failed, using metadata only[/yellow]")
            
            # Research video topic for additional learning
            if searcher and video_info.get('title'):
                console.print("[dim]🌐 Researching video topic...[/dim]")
                topic_research = self._research_video_topic(video_info['title'], searcher)
                learning_result['topic_research'] = topic_research
            
            # Process and store learning
            self._process_video_learning(learning_result)
            
            # Update learning skills
            self._update_learning_skills(learning_result)
            
            learning_result['success'] = True
            console.print("[green]✅ YouTube video learning complete![/green]")
            
        except Exception as e:
            console.print(f"[red]❌ YouTube learning failed: {e}[/red]")
            learning_result['error'] = str(e)
            self.youtube_knowledge['failed_attempts'].append({
                'url': youtube_url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        self.save_youtube_learning_data()
        return learning_result
    
    def autonomous_youtube_learning(self, video_vision_engine=None, searcher=None) -> Dict[str, Any]:
        """Autonomous YouTube learning - AI picks random educational videos"""
        console.print(f"[bold cyan]🤖 Autonomous YouTube Learning (Cycle {self.cycle_count})[/bold cyan]")
        
        autonomous_result = {
            'cycle': self.cycle_count,
            'timestamp': datetime.now().isoformat(),
            'search_query': '',
            'videos_found': [],
            'video_selected': {},
            'learning_outcome': {},
            'success': False
        }
        
        try:
            # Select random learning category and topic
            category = random.choice(list(self.learning_categories.keys()))
            topic = random.choice(self.learning_categories[category])
            
            # Add some randomness and evolution to search terms
            evolved_topic = self._evolve_search_topic(topic, category)
            autonomous_result['search_query'] = evolved_topic
            
            console.print(f"[yellow]🎯 Learning focus: {category.replace('_', ' ').title()}[/yellow]")
            console.print(f"[yellow]📚 Search topic: {evolved_topic}[/yellow]")
            
            # Search for educational videos
            if searcher:
                search_result = searcher.comprehensive_search(f"{evolved_topic} tutorial educational", 'educational')
                
                # Extract YouTube video links from search results
                youtube_links = self._extract_youtube_links_from_search(search_result)
                autonomous_result['videos_found'] = youtube_links
                
                if youtube_links:
                    # Select best video for learning
                    selected_video = self._select_best_learning_video(youtube_links)
                    autonomous_result['video_selected'] = selected_video
                    
                    console.print(f"[green]🎥 Selected video: {selected_video.get('title', 'Unknown')}[/green]")
                    console.print(f"[dim]🔗 URL: {selected_video.get('url', '')}[/dim]")
                    
                    # Learn from the selected video
                    learning_result = self.process_youtube_link(
                        selected_video['url'], 
                        video_vision_engine, 
                        searcher
                    )
                    
                    autonomous_result['learning_outcome'] = learning_result
                    autonomous_result['success'] = learning_result.get('success', False)
                    
                    # Store autonomous learning record
                    self.youtube_knowledge['autonomous_searches'].append({
                        'cycle': self.cycle_count,
                        'category': category,
                        'topic': evolved_topic,
                        'video_url': selected_video['url'],
                        'learning_success': learning_result.get('success', False),
                        'comprehension_score': learning_result.get('comprehension_score', 0),
                        'timestamp': datetime.now().isoformat()
                    })
                    
                else:
                    console.print("[yellow]⚠️ No YouTube videos found in search results[/yellow]")
            
            else:
                console.print("[yellow]⚠️ No searcher available for autonomous learning[/yellow]")
            
            self.last_autonomous_learning = datetime.now()
            
        except Exception as e:
            console.print(f"[red]❌ Autonomous learning failed: {e}[/red]")
            autonomous_result['error'] = str(e)
        
        self.save_youtube_learning_data()
        return autonomous_result
    
    def should_trigger_autonomous_learning(self) -> bool:
        """Check if autonomous learning should be triggered (every 3 cycles)"""
        return self.cycle_count % 3 == 0 and self.cycle_count > 0
    
    def increment_cycle(self):
        """Increment the learning cycle counter"""
        self.cycle_count += 1
        console.print(f"[dim]🔄 Learning cycle: {self.cycle_count}[/dim]")
    
    def _extract_video_id(self, youtube_url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        try:
            parsed_url = urlparse(youtube_url)
            
            if 'youtube.com' in parsed_url.netloc:
                if 'watch' in parsed_url.path:
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                elif '/embed/' in parsed_url.path:
                    return parsed_url.path.split('/embed/')[1].split('?')[0]
            elif 'youtu.be' in parsed_url.netloc:
                return parsed_url.path[1:].split('?')[0]
            
            return None
        except:
            return None
    
    def _get_video_metadata(self, youtube_url: str, searcher=None) -> Dict[str, Any]:
        """Get video metadata and basic information"""
        video_info = {
            'url': youtube_url,
            'title': 'Unknown Video',
            'description': '',
            'channel': 'Unknown Channel',
            'duration': 'Unknown',
            'category': 'educational'
        }
        
        try:
            # Try to get video info from search if available
            if searcher:
                search_result = searcher.comprehensive_search(f"site:youtube.com {youtube_url}", 'general')
                
                if search_result.get('total_sources', 0) > 0:
                    # Extract title and info from search results
                    for source_name, source_data in search_result.get('sources', {}).items():
                        if source_data.get('success') and source_data.get('results'):
                            for result in source_data['results'][:1]:
                                if result.get('title'):
                                    video_info['title'] = result['title']
                                if result.get('snippet'):
                                    video_info['description'] = result['snippet'][:200]
                                break
            
            # Categorize video based on title
            title_lower = video_info['title'].lower()
            for category, keywords in self.learning_categories.items():
                if any(keyword.lower() in title_lower for keyword in keywords):
                    video_info['category'] = category
                    break
            
        except Exception as e:
            console.print(f"[dim red]Metadata extraction failed: {e}[/dim red]")
        
        return video_info
    
    def _extract_learning_from_video(self, watch_result: Dict[str, Any], video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract learning insights from video analysis"""
        learning_data = {
            'concepts_learned': [],
            'knowledge_gained': [],
            'improvement_areas': [],
            'comprehension_score': watch_result.get('comprehension_score', 0),
            'learning_value': 0.0
        }
        
        try:
            # Extract concepts from video content
            visual_summary = watch_result.get('visual_summary', '')
            text_found = watch_result.get('text_found', [])
            
            # Analyze text content for concepts
            all_text = ' '.join([t.get('text', '') for t in text_found])
            concepts = self._extract_concepts_from_text(all_text + ' ' + visual_summary)
            learning_data['concepts_learned'] = concepts
            
            # Determine knowledge gained
            category = video_info.get('category', 'general')
            knowledge_gained = [
                f"Visual understanding of {category} content",
                f"Exposure to {len(text_found)} text elements",
                f"Motion pattern analysis in educational context"
            ]
            
            if watch_result.get('scenes_detected'):
                knowledge_gained.append(f"Scene structure in {category} videos")
            
            learning_data['knowledge_gained'] = knowledge_gained
            
            # Calculate learning value
            comprehension = watch_result.get('comprehension_score', 0)
            text_richness = min(len(text_found) / 10, 1.0)  # Normalize text content
            learning_value = (comprehension + text_richness) / 2
            learning_data['learning_value'] = learning_value
            
            # Identify improvement areas
            if comprehension < 0.5:
                learning_data['improvement_areas'].append("Video comprehension needs improvement")
            if len(text_found) < 5:
                learning_data['improvement_areas'].append("Text recognition could be enhanced")
            
        except Exception as e:
            console.print(f"[dim red]Learning extraction failed: {e}[/dim red]")
        
        return learning_data
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract key concepts from text content"""
        concepts = []
        
        # Common educational/technical terms
        concept_keywords = [
            'algorithm', 'function', 'variable', 'method', 'class', 'object',
            'neural', 'network', 'learning', 'training', 'model', 'data',
            'programming', 'code', 'software', 'development', 'system',
            'artificial', 'intelligence', 'machine', 'deep', 'computer',
            'science', 'technology', 'digital', 'analysis', 'process'
        ]
        
        text_lower = text.lower()
        for keyword in concept_keywords:
            if keyword in text_lower:
                concepts.append(keyword.title())
        
        return list(set(concepts))[:10]  # Return unique concepts, max 10
    
    def _research_video_topic(self, video_title: str, searcher) -> Dict[str, Any]:
        """Research the video topic for additional learning"""
        research_result = {}
        
        try:
            # Extract key terms from title
            key_terms = video_title.split()[:5]  # First 5 words
            search_query = ' '.join(key_terms) + ' explanation tutorial'
            
            search_result = searcher.comprehensive_search(search_query, 'educational')
            
            if search_result.get('total_sources', 0) > 0:
                synthesized = search_result.get('synthesized_results', {})
                
                research_result = {
                    'definitions_found': len(synthesized.get('definitions', [])),
                    'academic_sources': len(synthesized.get('academic_insights', [])),
                    'confidence_score': search_result.get('confidence_score', 0),
                    'related_topics': self._extract_related_topics(synthesized)
                }
        
        except Exception as e:
            console.print(f"[dim red]Topic research failed: {e}[/dim red]")
        
        return research_result
    
    def _extract_related_topics(self, synthesized_results: Dict[str, Any]) -> List[str]:
        """Extract related topics from search results"""
        topics = []
        
        for definition in synthesized_results.get('definitions', []):
            text = definition.get('text', '').lower()
            # Simple topic extraction
            topic_words = [word for word in text.split() if len(word) > 4]
            topics.extend(topic_words[:3])
        
        return list(set(topics))[:8]  # Return unique topics, max 8

    def _evolve_search_topic(self, base_topic: str, category: str) -> str:
        """Evolve search topics based on previous learning"""
        evolved_topic = base_topic

        try:
            # Add complexity based on learning progress
            skill_level = self.learning_skills.get('concept_extraction', 0)

            if skill_level > 0.5:
                # Advanced topics
                advanced_modifiers = ['advanced', 'deep dive', 'comprehensive', 'expert level']
                evolved_topic = f"{random.choice(advanced_modifiers)} {base_topic}"
            elif skill_level > 0.3:
                # Intermediate topics
                intermediate_modifiers = ['detailed', 'complete', 'thorough']
                evolved_topic = f"{random.choice(intermediate_modifiers)} {base_topic}"

            # Add current year for recent content
            current_year = datetime.now().year
            if random.random() < 0.3:  # 30% chance
                evolved_topic += f" {current_year}"

            # Add learning-focused terms
            learning_terms = ['tutorial', 'explained', 'guide', 'course', 'lesson']
            if random.random() < 0.5:  # 50% chance
                evolved_topic += f" {random.choice(learning_terms)}"

        except Exception as e:
            console.print(f"[dim red]Topic evolution failed: {e}[/dim red]")

        return evolved_topic

    def _extract_youtube_links_from_search(self, search_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract YouTube video links from search results"""
        youtube_links = []

        try:
            for source_name, source_data in search_result.get('sources', {}).items():
                if source_data.get('success') and source_data.get('results'):
                    for result in source_data['results']:
                        url = result.get('url', '')
                        if 'youtube.com/watch' in url or 'youtu.be/' in url:
                            youtube_links.append({
                                'url': url,
                                'title': result.get('title', 'Unknown'),
                                'snippet': result.get('snippet', ''),
                                'source': source_name
                            })

        except Exception as e:
            console.print(f"[dim red]YouTube link extraction failed: {e}[/dim red]")

        return youtube_links[:10]  # Return max 10 videos

    def _select_best_learning_video(self, youtube_links: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best video for learning based on various criteria"""
        if not youtube_links:
            return {}

        # Score videos based on learning potential
        scored_videos = []

        for video in youtube_links:
            score = 0
            title = video.get('title', '').lower()
            snippet = video.get('snippet', '').lower()

            # Educational keywords boost score
            educational_keywords = [
                'tutorial', 'explained', 'guide', 'course', 'lesson', 'learn',
                'beginner', 'introduction', 'basics', 'fundamentals', 'complete'
            ]

            for keyword in educational_keywords:
                if keyword in title:
                    score += 2
                if keyword in snippet:
                    score += 1

            # Technical/scientific content boost
            technical_keywords = [
                'algorithm', 'programming', 'science', 'technology', 'ai',
                'machine learning', 'neural network', 'data', 'analysis'
            ]

            for keyword in technical_keywords:
                if keyword in title:
                    score += 3
                if keyword in snippet:
                    score += 1

            # Avoid low-quality indicators
            low_quality_indicators = [
                'clickbait', 'reaction', 'funny', 'meme', 'prank', 'gossip'
            ]

            for indicator in low_quality_indicators:
                if indicator in title or indicator in snippet:
                    score -= 5

            scored_videos.append((video, score))

        # Sort by score and return best video
        scored_videos.sort(key=lambda x: x[1], reverse=True)
        return scored_videos[0][0] if scored_videos else youtube_links[0]

    def _process_video_learning(self, learning_result: Dict[str, Any]):
        """Process and store learning from video"""
        try:
            video_id = learning_result.get('video_id', '')
            if not video_id:
                return

            # Store video learning record
            self.youtube_knowledge['videos_learned_from'][video_id] = {
                'url': learning_result.get('youtube_url', ''),
                'title': learning_result.get('video_info', {}).get('title', ''),
                'learned_at': learning_result.get('processed_at', ''),
                'concepts_learned': learning_result.get('concepts_learned', []),
                'knowledge_gained': learning_result.get('knowledge_gained', []),
                'comprehension_score': learning_result.get('comprehension_score', 0),
                'learning_value': learning_result.get('learning_value', 0),
                'category': learning_result.get('video_info', {}).get('category', 'general')
            }

            # Update concepts database
            for concept in learning_result.get('concepts_learned', []):
                if concept not in self.youtube_knowledge['concepts_discovered']:
                    self.youtube_knowledge['concepts_discovered'][concept] = {
                        'first_discovered': datetime.now().isoformat(),
                        'videos_seen_in': [],
                        'learning_strength': 0.0
                    }

                concept_data = self.youtube_knowledge['concepts_discovered'][concept]
                concept_data['videos_seen_in'].append(video_id)
                concept_data['learning_strength'] = min(1.0, concept_data['learning_strength'] + 0.1)

            # Update learning topics
            category = learning_result.get('video_info', {}).get('category', 'general')
            if category not in self.youtube_knowledge['learning_topics']:
                self.youtube_knowledge['learning_topics'][category] = {
                    'videos_watched': 0,
                    'total_comprehension': 0.0,
                    'concepts_learned': [],
                    'last_updated': datetime.now().isoformat()
                }

            topic_data = self.youtube_knowledge['learning_topics'][category]
            topic_data['videos_watched'] += 1
            topic_data['total_comprehension'] += learning_result.get('comprehension_score', 0)
            topic_data['concepts_learned'].extend(learning_result.get('concepts_learned', []))
            topic_data['concepts_learned'] = list(set(topic_data['concepts_learned']))  # Remove duplicates
            topic_data['last_updated'] = datetime.now().isoformat()

        except Exception as e:
            console.print(f"[dim red]Learning processing failed: {e}[/dim red]")

    def _update_learning_skills(self, learning_result: Dict[str, Any]):
        """Update learning skills based on video learning outcome"""
        try:
            comprehension = learning_result.get('comprehension_score', 0)
            learning_value = learning_result.get('learning_value', 0)
            concepts_count = len(learning_result.get('concepts_learned', []))

            # Update skills based on performance
            if comprehension > 0.5:
                self.learning_skills['video_comprehension'] = min(1.0, self.learning_skills['video_comprehension'] + 0.02)

            if concepts_count > 3:
                self.learning_skills['concept_extraction'] = min(1.0, self.learning_skills['concept_extraction'] + 0.03)

            if learning_value > 0.6:
                self.learning_skills['knowledge_synthesis'] = min(1.0, self.learning_skills['knowledge_synthesis'] + 0.02)

            # Always improve autonomous learning
            self.learning_skills['autonomous_learning'] = min(1.0, self.learning_skills['autonomous_learning'] + 0.01)

            # Improve self-improvement skill
            self.learning_skills['self_improvement'] = min(1.0, self.learning_skills['self_improvement'] + 0.01)

        except Exception as e:
            console.print(f"[dim red]Skill update failed: {e}[/dim red]")

    def get_youtube_learning_status(self) -> Dict[str, Any]:
        """Get current YouTube learning status and progress"""
        return {
            'learning_skills': self.learning_skills,
            'videos_learned_from': len(self.youtube_knowledge['videos_learned_from']),
            'concepts_discovered': len(self.youtube_knowledge['concepts_discovered']),
            'learning_topics': len(self.youtube_knowledge['learning_topics']),
            'autonomous_searches': len(self.youtube_knowledge['autonomous_searches']),
            'cycle_count': self.cycle_count,
            'overall_learning_capability': sum(self.learning_skills.values()) / len(self.learning_skills),
            'top_concepts': self._get_top_concepts(),
            'favorite_topics': self._get_favorite_topics(),
            'recent_learning': self._get_recent_learning(),
            'next_autonomous_learning': self.cycle_count % 3 == 2  # Next cycle will trigger
        }

    def _get_top_concepts(self) -> List[Dict[str, Any]]:
        """Get most learned concepts"""
        concepts = []
        for concept, data in self.youtube_knowledge['concepts_discovered'].items():
            concepts.append({
                'concept': concept,
                'strength': data['learning_strength'],
                'videos': len(data['videos_seen_in'])
            })

        return sorted(concepts, key=lambda x: x['strength'], reverse=True)[:10]

    def _get_favorite_topics(self) -> List[Dict[str, Any]]:
        """Get most studied topics"""
        topics = []
        for topic, data in self.youtube_knowledge['learning_topics'].items():
            avg_comprehension = data['total_comprehension'] / data['videos_watched'] if data['videos_watched'] > 0 else 0
            topics.append({
                'topic': topic,
                'videos_watched': data['videos_watched'],
                'avg_comprehension': avg_comprehension,
                'concepts_learned': len(data['concepts_learned'])
            })

        return sorted(topics, key=lambda x: x['videos_watched'], reverse=True)[:5]

    def _get_recent_learning(self) -> List[Dict[str, Any]]:
        """Get recent learning activities"""
        recent = []

        # Recent autonomous searches
        for search in self.youtube_knowledge['autonomous_searches'][-5:]:
            recent.append({
                'type': 'autonomous_search',
                'topic': search['topic'],
                'success': search['learning_success'],
                'timestamp': search['timestamp']
            })

        # Recent video learning
        videos = list(self.youtube_knowledge['videos_learned_from'].values())
        for video in sorted(videos, key=lambda x: x['learned_at'], reverse=True)[:3]:
            recent.append({
                'type': 'video_learning',
                'title': video['title'][:50] + '...' if len(video['title']) > 50 else video['title'],
                'comprehension': video['comprehension_score'],
                'timestamp': video['learned_at']
            })

        return sorted(recent, key=lambda x: x['timestamp'], reverse=True)[:8]

    def load_youtube_learning_data(self):
        """Load YouTube learning data from storage"""
        try:
            learning_file = "memory/youtube_learning.json"
            if os.path.exists(learning_file):
                with open(learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learning_skills = data.get('learning_skills', self.learning_skills)
                    self.youtube_knowledge = data.get('youtube_knowledge', self.youtube_knowledge)
                    self.cycle_count = data.get('cycle_count', 0)
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load YouTube learning data: {e}[/dim yellow]")

    def save_youtube_learning_data(self):
        """Save YouTube learning data to storage"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            learning_file = "memory/youtube_learning.json"

            data = {
                'learning_skills': self.learning_skills,
                'youtube_knowledge': self.youtube_knowledge,
                'cycle_count': self.cycle_count,
                'last_updated': datetime.now().isoformat()
            }

            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            console.print(f"[dim red]Error saving YouTube learning data: {e}[/dim red]")
