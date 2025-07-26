"""
Memory and Knowledge Storage System
Manages persistent storage of learned information and experiences
"""
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
try:
    import numpy as np
except ImportError:
    # Fallback for numpy functions
    class NumpyFallback:
        @staticmethod
        def var(data):
            if not data:
                return 0
            mean = sum(data) / len(data)
            return sum((x - mean) ** 2 for x in data) / len(data)
    np = NumpyFallback()
from config import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class MemorySystem:
    def __init__(self):
        self.knowledge_base = {}
        self.episodic_memory = []  # Specific learning experiences
        self.semantic_memory = {}  # General knowledge and concepts
        self.procedural_memory = {}  # How-to knowledge and skills
        self.working_memory = {}  # Current session information
        self.memory_connections = defaultdict(set)  # Connections between concepts
        self.importance_scores = {}  # How important each piece of knowledge is
        self.access_frequency = defaultdict(int)  # How often knowledge is accessed
        self.last_accessed = {}  # When knowledge was last accessed
        self.load_all_memory()
        
    def store_knowledge(self, topic: str, information: Dict[str, Any], source: str = "web_search") -> str:
        """Store new knowledge with metadata"""
        knowledge_id = self._generate_knowledge_id(topic, information)
        
        knowledge_entry = {
            'id': knowledge_id,
            'topic': topic,
            'information': information,
            'source': source,
            'stored_at': datetime.now().isoformat(),
            'importance_score': self._calculate_importance(information),
            'connections': [],
            'tags': self._extract_tags(information),
            'summary': self._create_summary(information),
            'access_count': 0,
            'last_accessed': datetime.now().isoformat()
        }
        
        # Store in appropriate memory systems
        self.knowledge_base[knowledge_id] = knowledge_entry
        self.semantic_memory[topic] = self.semantic_memory.get(topic, []) + [knowledge_id]
        
        # Create connections with existing knowledge
        self._create_connections(knowledge_id, topic, information)
        
        # Store episodic memory of this learning event
        self._store_learning_episode(topic, information, source)
        
        console.print(f"🧠 Stored knowledge about [cyan]{topic}[/cyan] (ID: {knowledge_id[:8]}...)")
        return knowledge_id
        
    def _generate_knowledge_id(self, topic: str, information: Dict[str, Any]) -> str:
        """Generate unique ID for knowledge entry"""
        content = f"{topic}_{str(information)}_{time.time()}"
        return hashlib.md5(content.encode()).hexdigest()
        
    def _calculate_importance(self, information: Dict[str, Any]) -> float:
        """Calculate importance score for information"""
        score = 0.5  # Base score
        
        # More definitions = more important
        if 'definitions' in information:
            score += len(information['definitions']) * 0.1
            
        # More sources = more reliable/important
        if 'sources' in information:
            score += len(information['sources']) * 0.05
            
        # Interesting facts boost importance
        if 'interesting_facts' in information:
            score += len(information['interesting_facts']) * 0.15
            
        # Key concepts add importance
        if 'key_concepts' in information:
            score += len(information['key_concepts']) * 0.08
            
        return min(1.0, score)  # Cap at 1.0
        
    def _extract_tags(self, information: Dict[str, Any]) -> List[str]:
        """Extract tags from information for better organization"""
        tags = []
        
        # Add tags based on content type
        if 'definitions' in information and information['definitions']:
            tags.append('definition')
        if 'examples' in information and information['examples']:
            tags.append('examples')
        if 'interesting_facts' in information and information['interesting_facts']:
            tags.append('research')
        if 'key_concepts' in information and information['key_concepts']:
            tags.append('concepts')
            
        # Extract domain-specific tags
        content_text = str(information).lower()
        domain_tags = {
            'psychology': ['psychology', 'psychological', 'mental', 'cognitive'],
            'social': ['social', 'interpersonal', 'relationship', 'communication'],
            'behavioral': ['behavior', 'behavioral', 'action', 'response'],
            'emotional': ['emotion', 'emotional', 'feeling', 'mood'],
            'developmental': ['development', 'developmental', 'growth', 'change'],
            'clinical': ['clinical', 'therapy', 'treatment', 'disorder']
        }
        
        for tag, keywords in domain_tags.items():
            if any(keyword in content_text for keyword in keywords):
                tags.append(tag)
                
        return list(set(tags))  # Remove duplicates
        
    def _create_summary(self, information: Dict[str, Any]) -> str:
        """Create a concise summary of the information"""
        summary_parts = []
        
        if 'definitions' in information and information['definitions']:
            summary_parts.append(f"Definitions: {len(information['definitions'])} found")
            
        if 'key_concepts' in information and information['key_concepts']:
            summary_parts.append(f"Key concepts: {len(information['key_concepts'])} identified")
            
        if 'interesting_facts' in information and information['interesting_facts']:
            summary_parts.append(f"Research findings: {len(information['interesting_facts'])} facts")
            
        if 'sources' in information and information['sources']:
            summary_parts.append(f"Sources: {len(information['sources'])} references")
            
        return "; ".join(summary_parts) if summary_parts else "General information stored"
        
    def _create_connections(self, knowledge_id: str, topic: str, information: Dict[str, Any]):
        """Create connections between related knowledge"""
        # Connect to existing knowledge about the same topic
        if topic in self.semantic_memory:
            for existing_id in self.semantic_memory[topic]:
                if existing_id != knowledge_id:
                    self.memory_connections[knowledge_id].add(existing_id)
                    self.memory_connections[existing_id].add(knowledge_id)
                    
        # Connect based on shared concepts
        if 'key_concepts' in information:
            for concept in information['key_concepts']:
                concept_lower = concept.lower()
                for existing_id, existing_entry in self.knowledge_base.items():
                    if existing_id != knowledge_id:
                        existing_concepts = existing_entry.get('information', {}).get('key_concepts', [])
                        if any(concept_lower in existing_concept.lower() for existing_concept in existing_concepts):
                            self.memory_connections[knowledge_id].add(existing_id)
                            self.memory_connections[existing_id].add(knowledge_id)
                            
    def _store_learning_episode(self, topic: str, information: Dict[str, Any], source: str):
        """Store episodic memory of learning experience"""
        episode = {
            'timestamp': datetime.now().isoformat(),
            'topic': topic,
            'source': source,
            'information_quality': self._assess_information_quality(information),
            'learning_outcome': 'successful',
            'emotional_state': 'curious',  # Could be enhanced with emotion detection
            'context': f"Learning about {topic} from {source}"
        }
        
        self.episodic_memory.append(episode)
        
        # Keep only recent episodes (last 1000)
        if len(self.episodic_memory) > 1000:
            self.episodic_memory = self.episodic_memory[-1000:]
            
    def _assess_information_quality(self, information: Dict[str, Any]) -> str:
        """Assess the quality of information"""
        score = 0
        
        if information.get('definitions'):
            score += 2
        if information.get('sources'):
            score += len(information['sources'])
        if information.get('interesting_facts'):
            score += 2
        if information.get('examples'):
            score += 1
            
        if score >= 8:
            return 'excellent'
        elif score >= 5:
            return 'good'
        elif score >= 3:
            return 'fair'
        else:
            return 'poor'
            
    def retrieve_knowledge(self, topic: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve knowledge about a topic"""
        relevant_knowledge = []
        
        # Direct topic matches
        if topic in self.semantic_memory:
            for knowledge_id in self.semantic_memory[topic]:
                if knowledge_id in self.knowledge_base:
                    knowledge = self.knowledge_base[knowledge_id]
                    self._update_access_stats(knowledge_id)
                    relevant_knowledge.append(knowledge)
                    
        # Search in all knowledge for partial matches
        topic_lower = topic.lower()
        for knowledge_id, knowledge in self.knowledge_base.items():
            if knowledge_id not in [k['id'] for k in relevant_knowledge]:
                if (topic_lower in knowledge['topic'].lower() or 
                    any(topic_lower in tag.lower() for tag in knowledge.get('tags', []))):
                    self._update_access_stats(knowledge_id)
                    relevant_knowledge.append(knowledge)
                    
        # Sort by importance and recency
        relevant_knowledge.sort(key=lambda x: (
            x.get('importance_score', 0),
            self.access_frequency.get(x['id'], 0),
            x.get('stored_at', '')
        ), reverse=True)
        
        return relevant_knowledge[:limit]
        
    def _update_access_stats(self, knowledge_id: str):
        """Update access statistics for knowledge"""
        self.access_frequency[knowledge_id] += 1
        self.last_accessed[knowledge_id] = datetime.now().isoformat()
        
        if knowledge_id in self.knowledge_base:
            self.knowledge_base[knowledge_id]['access_count'] += 1
            self.knowledge_base[knowledge_id]['last_accessed'] = datetime.now().isoformat()
            
    def get_connected_knowledge(self, knowledge_id: str, depth: int = 1) -> List[Dict[str, Any]]:
        """Get knowledge connected to a specific piece of knowledge"""
        connected = []
        visited = set()
        
        def explore_connections(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return
                
            visited.add(current_id)
            
            for connected_id in self.memory_connections.get(current_id, set()):
                if connected_id in self.knowledge_base and connected_id not in visited:
                    connected.append(self.knowledge_base[connected_id])
                    if current_depth < depth:
                        explore_connections(connected_id, current_depth + 1)
                        
        explore_connections(knowledge_id, 0)
        return connected
        
    def consolidate_memory(self):
        """Consolidate and optimize memory storage"""
        console.print("🔄 Consolidating memory...")
        
        # Remove low-importance, rarely accessed knowledge
        cutoff_date = datetime.now() - timedelta(days=30)
        to_remove = []
        
        for knowledge_id, knowledge in self.knowledge_base.items():
            last_access = datetime.fromisoformat(knowledge.get('last_accessed', knowledge['stored_at']))
            importance = knowledge.get('importance_score', 0)
            access_count = knowledge.get('access_count', 0)
            
            if (last_access < cutoff_date and 
                importance < 0.3 and 
                access_count < 2):
                to_remove.append(knowledge_id)
                
        # Remove identified knowledge
        for knowledge_id in to_remove:
            self._remove_knowledge(knowledge_id)
            
        console.print(f"🗑️ Removed {len(to_remove)} low-value knowledge entries")
        
        # Strengthen important connections
        self._strengthen_connections()
        
    def _remove_knowledge(self, knowledge_id: str):
        """Remove knowledge and clean up references"""
        if knowledge_id in self.knowledge_base:
            topic = self.knowledge_base[knowledge_id]['topic']
            
            # Remove from knowledge base
            del self.knowledge_base[knowledge_id]
            
            # Remove from semantic memory
            if topic in self.semantic_memory:
                self.semantic_memory[topic] = [
                    kid for kid in self.semantic_memory[topic] if kid != knowledge_id
                ]
                
            # Remove connections
            if knowledge_id in self.memory_connections:
                for connected_id in self.memory_connections[knowledge_id]:
                    self.memory_connections[connected_id].discard(knowledge_id)
                del self.memory_connections[knowledge_id]
                
            # Clean up access stats
            self.access_frequency.pop(knowledge_id, None)
            self.last_accessed.pop(knowledge_id, None)
            
    def _strengthen_connections(self):
        """Strengthen connections between frequently accessed knowledge"""
        # This could be enhanced with more sophisticated algorithms
        pass
        
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        total_knowledge = len(self.knowledge_base)
        total_topics = len(self.semantic_memory)
        total_connections = sum(len(connections) for connections in self.memory_connections.values()) // 2
        
        # Calculate average importance
        avg_importance = sum(k.get('importance_score', 0) for k in self.knowledge_base.values()) / total_knowledge if total_knowledge > 0 else 0
        
        # Most accessed knowledge
        most_accessed = sorted(
            self.knowledge_base.items(),
            key=lambda x: x[1].get('access_count', 0),
            reverse=True
        )[:5]
        
        return {
            'total_knowledge_entries': total_knowledge,
            'total_topics': total_topics,
            'total_connections': total_connections,
            'episodic_memories': len(self.episodic_memory),
            'average_importance': avg_importance,
            'most_accessed_topics': [k[1]['topic'] for k in most_accessed],
            'memory_efficiency': self._calculate_memory_efficiency()
        }
        
    def _calculate_memory_efficiency(self) -> float:
        """Calculate how efficiently memory is being used"""
        if not self.knowledge_base:
            return 0.0
            
        # Factors: connection density, access frequency, importance distribution
        connection_density = sum(len(connections) for connections in self.memory_connections.values()) / len(self.knowledge_base)
        avg_access = sum(self.access_frequency.values()) / len(self.knowledge_base)
        importance_variance = np.var([k.get('importance_score', 0) for k in self.knowledge_base.values()])
        
        # Normalize and combine (this is a simplified calculation)
        efficiency = min(1.0, (connection_density * 0.3 + avg_access * 0.4 + (1 - importance_variance) * 0.3))
        return efficiency
        
    def display_memory_status(self):
        """Display current memory status"""
        stats = self.get_memory_statistics()
        
        table = Table(title="🧠 Memory System Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Knowledge Entries", str(stats['total_knowledge_entries']))
        table.add_row("Topics Covered", str(stats['total_topics']))
        table.add_row("Knowledge Connections", str(stats['total_connections']))
        table.add_row("Learning Episodes", str(stats['episodic_memories']))
        table.add_row("Average Importance", f"{stats['average_importance']:.2f}")
        table.add_row("Memory Efficiency", f"{stats['memory_efficiency']:.2f}")
        
        console.print(table)
        
        if stats['most_accessed_topics']:
            console.print("\n📈 Most Accessed Topics:")
            for i, topic in enumerate(stats['most_accessed_topics'], 1):
                console.print(f"  {i}. {topic}")
                
    def save_all_memory(self):
        """Save all memory systems to files"""
        os.makedirs(MEMORY_DIR, exist_ok=True)
        
        try:
            # Save knowledge base
            with open(KNOWLEDGE_BASE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
                
            # Save other memory systems
            memory_data = {
                'episodic_memory': self.episodic_memory,
                'semantic_memory': dict(self.semantic_memory),
                'procedural_memory': self.procedural_memory,
                'memory_connections': {k: list(v) for k, v in self.memory_connections.items()},
                'importance_scores': self.importance_scores,
                'access_frequency': dict(self.access_frequency),
                'last_accessed': self.last_accessed
            }
            
            with open(f"{MEMORY_DIR}/memory_systems.json", 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
                
            console.print("💾 Memory saved successfully")
            
        except Exception as e:
            console.print(f"[red]Error saving memory: {e}[/red]")
            
    def load_all_memory(self):
        """Load all memory systems from files"""
        try:
            # Load knowledge base
            if os.path.exists(KNOWLEDGE_BASE_FILE):
                with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                    
            # Load other memory systems
            memory_file = f"{MEMORY_DIR}/memory_systems.json"
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    
                self.episodic_memory = memory_data.get('episodic_memory', [])
                self.semantic_memory = defaultdict(list, memory_data.get('semantic_memory', {}))
                self.procedural_memory = memory_data.get('procedural_memory', {})
                self.memory_connections = defaultdict(set, {
                    k: set(v) for k, v in memory_data.get('memory_connections', {}).items()
                })
                self.importance_scores = memory_data.get('importance_scores', {})
                self.access_frequency = defaultdict(int, memory_data.get('access_frequency', {}))
                self.last_accessed = memory_data.get('last_accessed', {})
                
        except Exception as e:
            console.print(f"[yellow]Could not load memory files: {e}[/yellow]")
