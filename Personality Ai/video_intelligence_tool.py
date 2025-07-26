#!/usr/bin/env python3
"""
Video Intelligence Tool - Real video search and discovery tool
Production-ready video intelligence capabilities
"""

import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class VideoIntelligenceTool:
    """Real video intelligence tool for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.search_history = []
        self.discovered_channels = {}
        self.video_database = {}
        
    def search_videos_comprehensive(self, query: str, platform: str = 'all', max_results: int = 20) -> Dict[str, Any]:
        """Comprehensive video search across multiple platforms"""
        
        if not self.ai:
            return {'success': False, 'error': 'AI instance not available'}
        
        console.print(f"[yellow]🔍 Searching videos: {query}[/yellow]")
        console.print(f"[dim]Platform: {platform.title()}, Max Results: {max_results}[/dim]")
        
        try:
            # Execute real video search
            search_result = self.ai.video.search_videos(query, platform=platform, max_results=max_results)
            
            if search_result.get('success', False):
                # Store in search history
                self.search_history.append({
                    'query': query,
                    'platform': platform,
                    'timestamp': datetime.now().isoformat(),
                    'result': search_result
                })
                
                # Update video database
                videos_found = search_result.get('videos_found', [])
                for video in videos_found:
                    video_id = video.get('url', '') + video.get('title', '')
                    self.video_database[video_id] = {
                        'video': video,
                        'discovered_at': datetime.now().isoformat(),
                        'search_query': query
                    }
                
                # Update discovered channels
                for video in videos_found:
                    channel = video.get('channel', 'Unknown')
                    if channel != 'Unknown':
                        if channel not in self.discovered_channels:
                            self.discovered_channels[channel] = {
                                'videos_found': 0,
                                'first_discovered': datetime.now().isoformat(),
                                'categories': set()
                            }
                        
                        self.discovered_channels[channel]['videos_found'] += 1
                        self.discovered_channels[channel]['categories'].add(video.get('category', 'general'))
                
                console.print(f"[green]✅ Found {len(videos_found)} videos across platforms[/green]")
                
                # Display results
                self._display_search_results(search_result, query)
                
                return search_result
            else:
                error_msg = search_result.get('error', 'Unknown error')
                console.print(f"[red]❌ Video search failed: {error_msg}[/red]")
                return search_result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            console.print(f"[red]❌ Video search error: {e}[/red]")
            return error_result
    
    def _display_search_results(self, result: Dict[str, Any], query: str):
        """Display video search results"""
        
        console.print(f"\n[bold cyan]🎥 Video Search Results for: {query}[/bold cyan]")
        
        # Platform breakdown
        platform_results = result.get('platform_results', {})
        if platform_results:
            console.print(f"\n[cyan]📊 Platform Breakdown:[/cyan]")
            for platform, count in platform_results.items():
                console.print(f"  📺 {platform.title()}: {count} videos")
        
        # Video results table
        videos_found = result.get('videos_found', [])
        if videos_found:
            table = Table(title=f"Top {min(10, len(videos_found))} Videos Found")
            table.add_column("Platform", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Channel", style="yellow")
            table.add_column("Category", style="blue")
            
            for video in videos_found[:10]:  # Show top 10
                platform = video.get('platform', 'Unknown').title()
                title = video.get('title', 'Unknown')
                channel = video.get('channel', 'Unknown')
                category = video.get('category', 'general').title()
                
                # Truncate long titles
                if len(title) > 50:
                    title = title[:47] + "..."
                
                table.add_row(platform, title, channel, category)
            
            console.print(table)
        
        # Educational content analysis
        educational_videos = [v for v in videos_found if v.get('category') == 'educational']
        if educational_videos:
            console.print(f"\n[cyan]🎓 Educational Content: {len(educational_videos)} videos[/cyan]")
    
    def analyze_video_trends(self, queries: List[str]) -> Dict[str, Any]:
        """Analyze video trends across multiple search queries"""
        
        console.print(f"[yellow]📈 Analyzing video trends for {len(queries)} queries...[/yellow]")
        
        trends_analysis = {
            'queries_analyzed': len(queries),
            'total_videos_found': 0,
            'platform_distribution': {},
            'category_distribution': {},
            'channel_popularity': {},
            'trending_topics': [],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing trends...", total=len(queries))
            
            for query in queries:
                progress.update(task, description=f"Searching: {query}")
                
                search_result = self.search_videos_comprehensive(query, max_results=15)
                
                if search_result.get('success', False):
                    videos = search_result.get('videos_found', [])
                    trends_analysis['total_videos_found'] += len(videos)
                    
                    # Platform distribution
                    for video in videos:
                        platform = video.get('platform', 'unknown')
                        trends_analysis['platform_distribution'][platform] = trends_analysis['platform_distribution'].get(platform, 0) + 1
                    
                    # Category distribution
                    for video in videos:
                        category = video.get('category', 'general')
                        trends_analysis['category_distribution'][category] = trends_analysis['category_distribution'].get(category, 0) + 1
                    
                    # Channel popularity
                    for video in videos:
                        channel = video.get('channel', 'Unknown')
                        if channel != 'Unknown':
                            trends_analysis['channel_popularity'][channel] = trends_analysis['channel_popularity'].get(channel, 0) + 1
                
                progress.advance(task)
        
        # Generate trending topics
        trends_analysis['trending_topics'] = self._extract_trending_topics(queries, trends_analysis)
        
        console.print(f"[green]✅ Trends analysis complete![/green]")
        self._display_trends_analysis(trends_analysis)
        
        return trends_analysis
    
    def _extract_trending_topics(self, queries: List[str], analysis: Dict[str, Any]) -> List[str]:
        """Extract trending topics from analysis"""
        
        # Simple topic extraction based on query frequency and results
        topic_scores = {}
        
        for query in queries:
            words = query.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    topic_scores[word] = topic_scores.get(word, 0) + 1
        
        # Sort by frequency
        trending = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, score in trending[:10]]
    
    def _display_trends_analysis(self, analysis: Dict[str, Any]):
        """Display trends analysis results"""
        
        console.print(f"\n[bold cyan]📈 Video Trends Analysis[/bold cyan]")
        
        # Summary metrics
        console.print(f"\n[cyan]📊 Summary:[/cyan]")
        console.print(f"  🔍 Queries Analyzed: {analysis['queries_analyzed']}")
        console.print(f"  🎥 Total Videos Found: {analysis['total_videos_found']}")
        console.print(f"  📺 Platforms Covered: {len(analysis['platform_distribution'])}")
        console.print(f"  📂 Categories Found: {len(analysis['category_distribution'])}")
        
        # Platform distribution
        platform_dist = analysis['platform_distribution']
        if platform_dist:
            console.print(f"\n[cyan]📺 Platform Distribution:[/cyan]")
            for platform, count in sorted(platform_dist.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / analysis['total_videos_found']) * 100
                console.print(f"  • {platform.title()}: {count} videos ({percentage:.1f}%)")
        
        # Top categories
        category_dist = analysis['category_distribution']
        if category_dist:
            console.print(f"\n[cyan]📂 Top Categories:[/cyan]")
            for category, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True)[:5]:
                console.print(f"  • {category.title()}: {count} videos")
        
        # Trending topics
        trending_topics = analysis['trending_topics']
        if trending_topics:
            console.print(f"\n[cyan]🔥 Trending Topics:[/cyan]")
            console.print(f"  {', '.join(trending_topics[:8])}")
    
    def get_intelligence_status(self) -> Dict[str, Any]:
        """Get current video intelligence status"""
        
        if not self.ai:
            return {'error': 'AI instance not available'}
        
        try:
            status = self.ai.video.get_video_status()
            
            # Add tool-specific data
            status['search_history_count'] = len(self.search_history)
            status['discovered_channels_count'] = len(self.discovered_channels)
            status['video_database_size'] = len(self.video_database)
            status['tool_ready'] = True
            
            return status
            
        except Exception as e:
            return {'error': str(e), 'tool_ready': False}
    
    def show_search_history(self, limit: int = 10):
        """Show recent search history"""
        
        if not self.search_history:
            console.print("[yellow]No search history available[/yellow]")
            return
        
        console.print(f"[bold cyan]🔍 Recent Search History (last {limit})[/bold cyan]")
        
        table = Table()
        table.add_column("Time", style="dim")
        table.add_column("Query", style="cyan")
        table.add_column("Platform", style="green")
        table.add_column("Videos Found", style="yellow")
        
        for entry in self.search_history[-limit:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            query = entry['query']
            platform = entry['platform'].title()
            videos_found = len(entry['result'].get('videos_found', []))
            
            # Truncate long queries
            if len(query) > 30:
                query = query[:27] + "..."
            
            table.add_row(timestamp, query, platform, str(videos_found))
        
        console.print(table)
    
    def show_discovered_channels(self, limit: int = 15):
        """Show discovered channels"""
        
        if not self.discovered_channels:
            console.print("[yellow]No channels discovered yet[/yellow]")
            return
        
        console.print(f"[bold cyan]📺 Discovered Channels (top {limit})[/bold cyan]")
        
        table = Table()
        table.add_column("Channel", style="cyan")
        table.add_column("Videos Found", style="green")
        table.add_column("Categories", style="yellow")
        table.add_column("First Discovered", style="dim")
        
        # Sort by videos found
        sorted_channels = sorted(
            self.discovered_channels.items(),
            key=lambda x: x[1]['videos_found'],
            reverse=True
        )
        
        for channel, data in sorted_channels[:limit]:
            videos_count = str(data['videos_found'])
            categories = ', '.join(list(data['categories'])[:3])
            first_discovered = data['first_discovered'][:10]  # Date only
            
            # Truncate long channel names
            if len(channel) > 25:
                channel = channel[:22] + "..."
            
            table.add_row(channel, videos_count, categories, first_discovered)
        
        console.print(table)
    
    def export_video_database(self, filepath: str = "memory/video_database.json"):
        """Export video database to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            export_data = {
                'video_database': self.video_database,
                'discovered_channels': {k: {**v, 'categories': list(v['categories'])} for k, v in self.discovered_channels.items()},
                'search_history': self.search_history,
                'export_timestamp': datetime.now().isoformat(),
                'total_videos': len(self.video_database),
                'total_channels': len(self.discovered_channels)
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
                
            console.print(f"[green]💾 Video database exported to {filepath}[/green]")
            console.print(f"[dim]Exported {len(self.video_database)} videos and {len(self.discovered_channels)} channels[/dim]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error exporting video database: {e}[/red]")
            return False
    
    def import_video_database(self, filepath: str = "memory/video_database.json"):
        """Import video database from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.video_database = data.get('video_database', {})
                
                # Convert categories back to sets
                channels_data = data.get('discovered_channels', {})
                self.discovered_channels = {
                    k: {**v, 'categories': set(v.get('categories', []))}
                    for k, v in channels_data.items()
                }
                
                self.search_history = data.get('search_history', [])
                
                console.print(f"[green]📂 Video database imported from {filepath}[/green]")
                console.print(f"[dim]Imported {len(self.video_database)} videos and {len(self.discovered_channels)} channels[/dim]")
                return True
            
        except Exception as e:
            console.print(f"[red]Error importing video database: {e}[/red]")
            
        return False
    
    def search_local_database(self, query: str) -> List[Dict[str, Any]]:
        """Search through local video database"""
        
        query_lower = query.lower()
        matching_videos = []
        
        for video_id, video_data in self.video_database.items():
            video = video_data['video']
            title = video.get('title', '').lower()
            channel = video.get('channel', '').lower()
            category = video.get('category', '').lower()
            
            if (query_lower in title or 
                query_lower in channel or 
                query_lower in category):
                matching_videos.append(video_data)
        
        console.print(f"[green]🔍 Found {len(matching_videos)} matching videos in local database[/green]")
        
        if matching_videos:
            table = Table(title=f"Local Database Search: {query}")
            table.add_column("Title", style="cyan")
            table.add_column("Channel", style="green")
            table.add_column("Platform", style="yellow")
            table.add_column("Discovered", style="dim")
            
            for video_data in matching_videos[:10]:  # Show top 10
                video = video_data['video']
                title = video.get('title', 'Unknown')
                channel = video.get('channel', 'Unknown')
                platform = video.get('platform', 'Unknown').title()
                discovered = video_data['discovered_at'][:10]
                
                # Truncate long titles
                if len(title) > 40:
                    title = title[:37] + "..."
                
                table.add_row(title, channel, platform, discovered)
            
            console.print(table)
        
        return matching_videos


def main():
    """Main function for standalone usage"""
    console.print("[bold green]🎥 Video Intelligence Tool[/bold green]")
    console.print("Real video search and discovery tool")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        tool = VideoIntelligenceTool(ai)
        tool.import_video_database()
        
        console.print("[green]✅ Video Intelligence Tool ready![/green]")
        
        # Show current status
        status = tool.get_intelligence_status()
        
        console.print("\n[cyan]📊 Current Status:[/cyan]")
        console.print(f"  🎥 Videos Watched: {status.get('videos_watched', 0)}")
        console.print(f"  📂 Topics Explored: {status.get('topics_explored', 0)}")
        console.print(f"  📺 Channels Discovered: {status.get('channels_discovered', 0)}")
        console.print(f"  🔍 Searches Performed: {status.get('searches_performed', 0)}")
        console.print(f"  🧠 Overall Intelligence: {status.get('overall_video_intelligence', 0):.3f}")
        
        # Show tool-specific data
        console.print(f"  📚 Local Database: {status.get('video_database_size', 0)} videos")
        console.print(f"  🔍 Search History: {status.get('search_history_count', 0)} searches")
        
        # Show recent activity
        if tool.search_history:
            tool.show_search_history(5)
        
        if tool.discovered_channels:
            tool.show_discovered_channels(8)
        
        tool.export_video_database()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
