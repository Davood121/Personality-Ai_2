#!/usr/bin/env python3
"""
YouTube Learning Interface - Real autonomous YouTube learning interface
Production-ready YouTube learning capabilities
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import re

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class YouTubeLearningInterface:
    """Real YouTube learning interface for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.learning_history = []
        self.autonomous_sessions = []
        
    def learn_from_youtube_url(self, youtube_url: str) -> Dict[str, Any]:
        """Learn from a specific YouTube video URL"""
        
        if not self.ai:
            return {'success': False, 'error': 'AI instance not available'}
        
        # Validate YouTube URL
        if not self._is_valid_youtube_url(youtube_url):
            return {'success': False, 'error': 'Invalid YouTube URL'}
        
        console.print(f"[yellow]📺 AI learning from YouTube video...[/yellow]")
        console.print(f"[dim]URL: {youtube_url}[/dim]")
        
        try:
            # Execute real YouTube learning
            learning_result = self.ai.youtube_learning.process_youtube_link(
                youtube_url,
                video_vision_engine=self.ai.video_vision,
                searcher=self.ai.searcher
            )
            
            if learning_result.get('success', False):
                # Store in history
                self.learning_history.append({
                    'youtube_url': youtube_url,
                    'timestamp': datetime.now().isoformat(),
                    'result': learning_result
                })
                
                console.print("[green]✅ YouTube learning complete![/green]")
                
                # Display results
                self._display_learning_results(learning_result, youtube_url)
                
                return learning_result
            else:
                error_msg = learning_result.get('error', 'Unknown error')
                console.print(f"[red]❌ YouTube learning failed: {error_msg}[/red]")
                return learning_result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            console.print(f"[red]❌ YouTube learning error: {e}[/red]")
            return error_result
    
    def trigger_autonomous_learning(self) -> Dict[str, Any]:
        """Trigger autonomous YouTube learning session"""
        
        if not self.ai:
            return {'success': False, 'error': 'AI instance not available'}
        
        console.print("[yellow]🤖 Triggering autonomous YouTube learning...[/yellow]")
        
        try:
            # Execute autonomous learning
            autonomous_result = self.ai.youtube_learning.autonomous_youtube_learning(
                video_vision_engine=self.ai.video_vision,
                searcher=self.ai.searcher
            )
            
            if autonomous_result.get('success', False):
                # Store in autonomous sessions
                self.autonomous_sessions.append({
                    'timestamp': datetime.now().isoformat(),
                    'result': autonomous_result
                })
                
                console.print("[green]✅ Autonomous learning complete![/green]")
                
                # Display results
                self._display_autonomous_results(autonomous_result)
                
                return autonomous_result
            else:
                error_msg = autonomous_result.get('error', 'Unknown error')
                console.print(f"[red]❌ Autonomous learning failed: {error_msg}[/red]")
                return autonomous_result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            console.print(f"[red]❌ Autonomous learning error: {e}[/red]")
            return error_result
    
    def _display_learning_results(self, result: Dict[str, Any], youtube_url: str):
        """Display YouTube learning results"""
        
        console.print(f"\n[bold cyan]📺 YouTube Learning Results[/bold cyan]")
        console.print(f"[dim]URL: {youtube_url}[/dim]")
        
        # Video information
        video_info = result.get('video_info', {})
        if video_info:
            console.print(f"\n[cyan]📹 Video Information:[/cyan]")
            console.print(f"  📝 Title: {video_info.get('title', 'Unknown')}")
            console.print(f"  📂 Category: {video_info.get('category', 'general').title()}")
            console.print(f"  📺 Channel: {video_info.get('channel', 'Unknown')}")
        
        # Learning metrics
        table = Table(title="Learning Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Comprehension Score", f"{result.get('comprehension_score', 0):.2f}")
        table.add_row("Learning Value", f"{result.get('learning_value', 0):.2f}")
        table.add_row("Concepts Learned", str(len(result.get('concepts_learned', []))))
        table.add_row("Knowledge Gained", str(len(result.get('knowledge_gained', []))))
        
        console.print(table)
        
        # Concepts learned
        concepts_learned = result.get('concepts_learned', [])
        if concepts_learned:
            console.print(f"\n[cyan]💡 Concepts Learned ({len(concepts_learned)}):[/cyan]")
            for concept in concepts_learned[:10]:  # Show first 10
                console.print(f"  • {concept}")
            
            if len(concepts_learned) > 10:
                console.print(f"  ... and {len(concepts_learned) - 10} more")
        
        # Knowledge gained
        knowledge_gained = result.get('knowledge_gained', [])
        if knowledge_gained:
            console.print(f"\n[cyan]📚 Knowledge Gained ({len(knowledge_gained)}):[/cyan]")
            for knowledge in knowledge_gained[:5]:  # Show first 5
                console.print(f"  • {knowledge}")
            
            if len(knowledge_gained) > 5:
                console.print(f"  ... and {len(knowledge_gained) - 5} more")
        
        # Topic research
        topic_research = result.get('topic_research', {})
        if topic_research:
            console.print(f"\n[cyan]🌐 Additional Research:[/cyan]")
            console.print(f"  📖 Definitions Found: {topic_research.get('definitions_found', 0)}")
            console.print(f"  🎓 Academic Sources: {topic_research.get('academic_sources', 0)}")
            console.print(f"  🎯 Confidence Score: {topic_research.get('confidence_score', 0):.2f}")
        
        # Learning assessment
        comprehension = result.get('comprehension_score', 0)
        if comprehension > 0.7:
            console.print(f"\n[green]🎓 Excellent learning! AI understood the video very well.[/green]")
        elif comprehension > 0.5:
            console.print(f"\n[yellow]📚 Good learning! AI grasped most of the content.[/yellow]")
        else:
            console.print(f"\n[red]🤔 Basic learning. AI needs more practice with this content type.[/red]")
    
    def _display_autonomous_results(self, result: Dict[str, Any]):
        """Display autonomous learning results"""
        
        console.print(f"\n[bold cyan]🤖 Autonomous Learning Results[/bold cyan]")
        
        # Search information
        search_query = result.get('search_query', '')
        video_selected = result.get('video_selected', {})
        
        console.print(f"\n[cyan]🔍 Autonomous Search:[/cyan]")
        console.print(f"  🎯 Search Query: {search_query}")
        console.print(f"  📺 Video Selected: {video_selected.get('title', 'Unknown')}")
        console.print(f"  🔗 Video URL: {video_selected.get('url', 'Unknown')}")
        
        # Learning outcome
        learning_outcome = result.get('learning_outcome', {})
        if learning_outcome:
            console.print(f"\n[cyan]📚 Learning Outcome:[/cyan]")
            console.print(f"  🧠 Comprehension: {learning_outcome.get('comprehension_score', 0):.2f}")
            console.print(f"  📈 Learning Value: {learning_outcome.get('learning_value', 0):.2f}")
            
            concepts = learning_outcome.get('concepts_learned', [])
            if concepts:
                console.print(f"  💡 Concepts Discovered: {', '.join(concepts[:5])}")
                if len(concepts) > 5:
                    console.print(f"      ... and {len(concepts) - 5} more")
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get current YouTube learning status"""
        
        if not self.ai:
            return {'error': 'AI instance not available'}
        
        try:
            status = self.ai.youtube_learning.get_youtube_learning_status()
            
            # Add interface-specific data
            status['manual_learning_sessions'] = len(self.learning_history)
            status['autonomous_sessions'] = len(self.autonomous_sessions)
            status['interface_ready'] = True
            
            return status
            
        except Exception as e:
            return {'error': str(e), 'interface_ready': False}
    
    def show_learning_history(self, limit: int = 10):
        """Show recent YouTube learning history"""
        
        if not self.learning_history:
            console.print("[yellow]No YouTube learning history available[/yellow]")
            return
        
        console.print(f"[bold cyan]📺 Recent YouTube Learning History (last {limit})[/bold cyan]")
        
        table = Table()
        table.add_column("Time", style="dim")
        table.add_column("Video Title", style="cyan")
        table.add_column("Comprehension", style="green")
        table.add_column("Concepts", style="yellow")
        table.add_column("Learning Value", style="blue")
        
        for entry in self.learning_history[-limit:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            result = entry['result']
            
            video_info = result.get('video_info', {})
            title = video_info.get('title', 'Unknown Video')
            
            # Truncate long titles
            if len(title) > 40:
                title = title[:37] + "..."
            
            comprehension = f"{result.get('comprehension_score', 0):.2f}"
            concepts = str(len(result.get('concepts_learned', [])))
            learning_value = f"{result.get('learning_value', 0):.2f}"
            
            table.add_row(timestamp, title, comprehension, concepts, learning_value)
        
        console.print(table)
    
    def show_autonomous_sessions(self, limit: int = 10):
        """Show recent autonomous learning sessions"""
        
        if not self.autonomous_sessions:
            console.print("[yellow]No autonomous learning sessions available[/yellow]")
            return
        
        console.print(f"[bold cyan]🤖 Recent Autonomous Sessions (last {limit})[/bold cyan]")
        
        table = Table()
        table.add_column("Time", style="dim")
        table.add_column("Search Query", style="cyan")
        table.add_column("Video Found", style="green")
        table.add_column("Success", style="yellow")
        
        for entry in self.autonomous_sessions[-limit:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            result = entry['result']
            
            search_query = result.get('search_query', 'Unknown')
            video_selected = result.get('video_selected', {})
            video_title = video_selected.get('title', 'None')
            success = "✅" if result.get('success', False) else "❌"
            
            # Truncate long queries and titles
            if len(search_query) > 30:
                search_query = search_query[:27] + "..."
            if len(video_title) > 30:
                video_title = video_title[:27] + "..."
            
            table.add_row(timestamp, search_query, video_title, success)
        
        console.print(table)
    
    def get_learning_analytics(self) -> Dict[str, Any]:
        """Get comprehensive learning analytics"""
        
        analytics = {
            'total_manual_sessions': len(self.learning_history),
            'total_autonomous_sessions': len(self.autonomous_sessions),
            'success_rate': 0.0,
            'average_comprehension': 0.0,
            'top_concepts': [],
            'learning_trends': {},
            'generated_at': datetime.now().isoformat()
        }
        
        # Calculate success rate
        successful_sessions = sum(1 for entry in self.learning_history if entry['result'].get('success', False))
        if self.learning_history:
            analytics['success_rate'] = successful_sessions / len(self.learning_history)
        
        # Calculate average comprehension
        comprehension_scores = [entry['result'].get('comprehension_score', 0) for entry in self.learning_history if entry['result'].get('success', False)]
        if comprehension_scores:
            analytics['average_comprehension'] = sum(comprehension_scores) / len(comprehension_scores)
        
        # Extract top concepts
        all_concepts = []
        for entry in self.learning_history:
            concepts = entry['result'].get('concepts_learned', [])
            all_concepts.extend(concepts)
        
        # Count concept frequency
        concept_counts = {}
        for concept in all_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Get top concepts
        analytics['top_concepts'] = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return analytics
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Validate YouTube URL format"""
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/v/[\w-]+'
        ]
        
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    def batch_learn_from_urls(self, youtube_urls: List[str]) -> Dict[str, Any]:
        """Learn from multiple YouTube URLs in batch"""
        
        results = {
            'total_urls': len(youtube_urls),
            'successful_learning': 0,
            'failed_learning': 0,
            'results': [],
            'summary': {}
        }
        
        console.print(f"[yellow]📺 Batch learning from {len(youtube_urls)} YouTube videos...[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Learning from videos...", total=len(youtube_urls))
            
            for i, url in enumerate(youtube_urls, 1):
                progress.update(task, description=f"Processing video {i}/{len(youtube_urls)}")
                
                result = self.learn_from_youtube_url(url)
                
                if result.get('success', False):
                    results['successful_learning'] += 1
                else:
                    results['failed_learning'] += 1
                
                results['results'].append({
                    'youtube_url': url,
                    'result': result
                })
                
                progress.advance(task)
        
        # Generate summary
        if results['successful_learning'] > 0:
            total_concepts = sum(len(r['result'].get('concepts_learned', [])) for r in results['results'] if r['result'].get('success'))
            avg_comprehension = sum(r['result'].get('comprehension_score', 0) for r in results['results'] if r['result'].get('success')) / results['successful_learning']
            
            results['summary'] = {
                'total_concepts_learned': total_concepts,
                'average_comprehension': avg_comprehension,
                'success_rate': results['successful_learning'] / results['total_urls']
            }
        
        console.print(f"\n[green]✅ Batch learning complete![/green]")
        console.print(f"[cyan]Success: {results['successful_learning']}/{results['total_urls']}[/cyan]")
        
        return results
    
    def save_learning_data(self, filepath: str = "memory/youtube_learning_interface.json"):
        """Save learning data to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            data = {
                'learning_history': self.learning_history,
                'autonomous_sessions': self.autonomous_sessions,
                'analytics': self.get_learning_analytics(),
                'last_saved': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            console.print(f"[green]💾 Learning data saved to {filepath}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving learning data: {e}[/red]")
            return False
    
    def load_learning_data(self, filepath: str = "memory/youtube_learning_interface.json"):
        """Load learning data from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.learning_history = data.get('learning_history', [])
                self.autonomous_sessions = data.get('autonomous_sessions', [])
                
                console.print(f"[green]📂 Learning data loaded from {filepath}[/green]")
                return True
            
        except Exception as e:
            console.print(f"[red]Error loading learning data: {e}[/red]")
            
        return False


def main():
    """Main function for standalone usage"""
    console.print("[bold green]📺 YouTube Learning Interface[/bold green]")
    console.print("Real autonomous YouTube learning interface")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        interface = YouTubeLearningInterface(ai)
        interface.load_learning_data()
        
        console.print("[green]✅ YouTube Learning Interface ready![/green]")
        
        # Show current status
        status = interface.get_learning_status()
        
        console.print("\n[cyan]📊 Current Status:[/cyan]")
        console.print(f"  📺 Videos Learned From: {status.get('videos_learned_from', 0)}")
        console.print(f"  💡 Concepts Discovered: {status.get('concepts_discovered', 0)}")
        console.print(f"  📂 Learning Topics: {status.get('learning_topics', 0)}")
        console.print(f"  🤖 Autonomous Searches: {status.get('autonomous_searches', 0)}")
        console.print(f"  🔄 Current Cycle: {status.get('cycle_count', 0)}")
        console.print(f"  🧠 Learning Capability: {status.get('overall_learning_capability', 0):.3f}")
        
        # Show learning analytics
        analytics = interface.get_learning_analytics()
        
        console.print(f"\n[cyan]📈 Learning Analytics:[/cyan]")
        console.print(f"  📺 Manual Sessions: {analytics['total_manual_sessions']}")
        console.print(f"  🤖 Autonomous Sessions: {analytics['total_autonomous_sessions']}")
        console.print(f"  ✅ Success Rate: {analytics['success_rate']:.2%}")
        console.print(f"  🧠 Avg Comprehension: {analytics['average_comprehension']:.2f}")
        
        # Show recent history
        if interface.learning_history:
            interface.show_learning_history(5)
        
        if interface.autonomous_sessions:
            interface.show_autonomous_sessions(3)
        
        interface.save_learning_data()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
