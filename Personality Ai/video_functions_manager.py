#!/usr/bin/env python3
"""
Video Functions Manager - Complete video and vision capabilities management
Real implementation for production use
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class VideoFunctionsManager:
    """Real video functions manager for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.video_capabilities = {
            'video_search': True,
            'video_vision': True,
            'youtube_learning': True,
            'image_vision': True
        }
        self.performance_metrics = {
            'total_videos_processed': 0,
            'total_searches_performed': 0,
            'total_learning_sessions': 0,
            'average_comprehension': 0.0,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_all_video_capabilities(self) -> Dict[str, Any]:
        """Get comprehensive video and vision capabilities status"""
        
        if not self.ai:
            return {'error': 'AI instance not provided'}
        
        try:
            capabilities = {
                'video_search': self._get_video_search_status(),
                'video_vision': self._get_video_vision_status(),
                'youtube_learning': self._get_youtube_learning_status(),
                'image_vision': self._get_image_vision_status(),
                'performance_metrics': self.performance_metrics,
                'overall_status': 'operational',
                'timestamp': datetime.now().isoformat()
            }
            
            return capabilities
            
        except Exception as e:
            return {'error': str(e), 'overall_status': 'error'}
    
    def _get_video_search_status(self) -> Dict[str, Any]:
        """Get video search capabilities status"""
        try:
            status = self.ai.video.get_video_status()
            return {
                'available': True,
                'videos_found': status.get('videos_watched', 0),
                'platforms': ['YouTube', 'Vimeo', 'Dailymotion'],
                'searches_performed': status.get('searches_performed', 0),
                'capabilities': list(status.get('video_skills', {}).keys()),
                'overall_intelligence': status.get('overall_video_intelligence', 0)
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def _get_video_vision_status(self) -> Dict[str, Any]:
        """Get video vision capabilities status"""
        try:
            status = self.ai.video_vision.get_video_vision_status()
            return {
                'available': True,
                'videos_watched': status.get('videos_watched', 0),
                'scenes_analyzed': status.get('scenes_analyzed', 0),
                'objects_tracked': status.get('objects_tracked', 0),
                'text_instances': status.get('text_instannces', 0),
                'comprehension_average': status.get('comprehension_average', 0),
                'capabilities': list(status.get('video_vision_skills', {}).keys()),
                'overall_vision': status.get('overall_video_vision', 0)
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def _get_youtube_learning_status(self) -> Dict[str, Any]:
        """Get YouTube learning capabilities status"""
        try:
            status = self.ai.youtube_learning.get_youtube_learning_status()
            return {
                'available': True,
                'videos_learned_from': status.get('videos_learned_from', 0),
                'concepts_discovered': status.get('concepts_discovered', 0),
                'learning_topics': status.get('learning_topics', 0),
                'autonomous_searches': status.get('autonomous_searches', 0),
                'cycle_count': status.get('cycle_count', 0),
                'capabilities': list(status.get('learning_skills', {}).keys()),
                'overall_capability': status.get('overall_learning_capability', 0),
                'next_autonomous_learning': status.get('next_autonomous_learning', False)
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def _get_image_vision_status(self) -> Dict[str, Any]:
        """Get image vision capabilities status"""
        try:
            status = self.ai.vision.get_vision_status()
            return {
                'available': True,
                'images_analyzed': status.get('images_analyzed', 0),
                'objects_learned': status.get('objects_learned', 0),
                'colors_learned': status.get('colors_learned', 0),
                'capabilities': list(status.get('vision_skills', {}).keys()),
                'overall_capability': status.get('overall_vision_capability', 0)
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def execute_video_search(self, query: str, platform: str = 'all', max_results: int = 10) -> Dict[str, Any]:
        """Execute real video search across platforms"""
        try:
            if not self.ai:
                return {'success': False, 'error': 'AI instance not available'}
            
            console.print(f"[yellow]🔍 Searching videos: {query}[/yellow]")
            
            # Execute real video search
            search_result = self.ai.video.search_videos(query, platform=platform, max_results=max_results)
            
            if search_result.get('success', False):
                videos_found = len(search_result.get('videos_found', []))
                self.performance_metrics['total_searches_performed'] += 1
                
                console.print(f"[green]✅ Found {videos_found} videos[/green]")
                
                return {
                    'success': True,
                    'videos_found': videos_found,
                    'videos': search_result.get('videos_found', []),
                    'platform_results': search_result.get('platform_results', {}),
                    'query': query
                }
            else:
                return {'success': False, 'error': 'Search failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_video_vision(self, video_path: str) -> Dict[str, Any]:
        """Execute real video vision analysis"""
        try:
            if not self.ai:
                return {'success': False, 'error': 'AI instance not available'}
            
            console.print(f"[yellow]👁️ Analyzing video: {video_path}[/yellow]")
            
            # Execute real video vision
            vision_result = self.ai.video_vision.watch_video(video_path)
            
            if vision_result.get('success', False):
                self.performance_metrics['total_videos_processed'] += 1
                comprehension = vision_result.get('comprehension_score', 0)
                
                # Update average comprehension
                total_videos = self.performance_metrics['total_videos_processed']
                current_avg = self.performance_metrics['average_comprehension']
                new_avg = ((current_avg * (total_videos - 1)) + comprehension) / total_videos
                self.performance_metrics['average_comprehension'] = new_avg
                
                console.print(f"[green]✅ Video analysis complete! Comprehension: {comprehension:.2f}[/green]")
                
                return {
                    'success': True,
                    'comprehension_score': comprehension,
                    'frames_analyzed': vision_result.get('frames_analyzed', 0),
                    'text_found': vision_result.get('text_found', []),
                    'objects_detected': vision_result.get('objects_detected', []),
                    'visual_summary': vision_result.get('visual_summary', ''),
                    'video_path': video_path
                }
            else:
                return {'success': False, 'error': 'Video analysis failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_youtube_learning(self, youtube_url: str) -> Dict[str, Any]:
        """Execute real YouTube learning"""
        try:
            if not self.ai:
                return {'success': False, 'error': 'AI instance not available'}
            
            console.print(f"[yellow]📺 Learning from YouTube: {youtube_url}[/yellow]")
            
            # Execute real YouTube learning
            learning_result = self.ai.youtube_learning.process_youtube_link(
                youtube_url,
                video_vision_engine=self.ai.video_vision,
                searcher=self.ai.searcher
            )
            
            if learning_result.get('success', False):
                self.performance_metrics['total_learning_sessions'] += 1
                concepts_learned = len(learning_result.get('concepts_learned', []))
                
                console.print(f"[green]✅ YouTube learning complete! Concepts learned: {concepts_learned}[/green]")
                
                return {
                    'success': True,
                    'concepts_learned': learning_result.get('concepts_learned', []),
                    'knowledge_gained': learning_result.get('knowledge_gained', []),
                    'comprehension_score': learning_result.get('comprehension_score', 0),
                    'learning_value': learning_result.get('learning_value', 0),
                    'video_info': learning_result.get('video_info', {}),
                    'youtube_url': youtube_url
                }
            else:
                return {'success': False, 'error': 'YouTube learning failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_autonomous_youtube_learning(self) -> Dict[str, Any]:
        """Execute autonomous YouTube learning"""
        try:
            if not self.ai:
                return {'success': False, 'error': 'AI instance not available'}
            
            console.print("[yellow]🤖 Triggering autonomous YouTube learning...[/yellow]")
            
            # Execute autonomous learning
            autonomous_result = self.ai.youtube_learning.autonomous_youtube_learning(
                video_vision_engine=self.ai.video_vision,
                searcher=self.ai.searcher
            )
            
            if autonomous_result.get('success', False):
                learning_outcome = autonomous_result.get('learning_outcome', {})
                
                console.print("[green]✅ Autonomous learning complete![/green]")
                
                return {
                    'success': True,
                    'search_query': autonomous_result.get('search_query', ''),
                    'video_selected': autonomous_result.get('video_selected', {}),
                    'learning_outcome': learning_outcome,
                    'cycle': autonomous_result.get('cycle', 0)
                }
            else:
                return {'success': False, 'error': 'Autonomous learning failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_image_analysis(self, image_path: str) -> Dict[str, Any]:
        """Execute real image analysis"""
        try:
            if not self.ai:
                return {'success': False, 'error': 'AI instance not available'}
            
            console.print(f"[yellow]👁️ Analyzing image: {image_path}[/yellow]")
            
            # Execute real image analysis
            analysis_result = self.ai.vision.analyze_image(
                image_path,
                searcher=self.ai.searcher,
                memory=self.ai.memory
            )
            
            if analysis_result.get('success', False):
                console.print("[green]✅ Image analysis complete![/green]")
                
                return {
                    'success': True,
                    'objects_detected': analysis_result.get('objects_detected', []),
                    'colors_detected': analysis_result.get('colors_detected', []),
                    'text_found': analysis_result.get('text_found', ''),
                    'web_research': analysis_result.get('web_research', {}),
                    'visual_summary': analysis_result.get('visual_summary', ''),
                    'image_path': image_path
                }
            else:
                return {'success': False, 'error': 'Image analysis failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        try:
            capabilities = self.get_all_video_capabilities()
            
            report = {
                'performance_summary': self.performance_metrics,
                'capabilities_status': capabilities,
                'recommendations': self._generate_recommendations(capabilities),
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_recommendations(self, capabilities: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on current capabilities"""
        recommendations = []
        
        # Check video search performance
        video_search = capabilities.get('video_search', {})
        if video_search.get('searches_performed', 0) < 10:
            recommendations.append("Try more video searches to improve discovery capabilities")
        
        # Check video vision performance
        video_vision = capabilities.get('video_vision', {})
        if video_vision.get('videos_watched', 0) < 5:
            recommendations.append("Watch more videos to enhance vision analysis skills")
        
        # Check YouTube learning
        youtube_learning = capabilities.get('youtube_learning', {})
        if youtube_learning.get('videos_learned_from', 0) < 3:
            recommendations.append("Learn from more YouTube videos to build knowledge base")
        
        # Check autonomous learning
        if not youtube_learning.get('next_autonomous_learning', False):
            recommendations.append("Autonomous learning will trigger in next few cycles")
        
        return recommendations
    
    def save_performance_data(self, filepath: str = "memory/video_performance.json"):
        """Save performance data to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            data = {
                'performance_metrics': self.performance_metrics,
                'video_capabilities': self.video_capabilities,
                'last_saved': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving performance data: {e}[/red]")
            return False
    
    def load_performance_data(self, filepath: str = "memory/video_performance.json"):
        """Load performance data from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.performance_metrics = data.get('performance_metrics', self.performance_metrics)
                self.video_capabilities = data.get('video_capabilities', self.video_capabilities)
                
                return True
            
        except Exception as e:
            console.print(f"[red]Error loading performance data: {e}[/red]")
            
        return False


def main():
    """Main function for standalone usage"""
    console.print("[bold green]🎬 Video Functions Manager[/bold green]")
    console.print("Real video and vision capabilities management system")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        manager = VideoFunctionsManager(ai)
        manager.load_performance_data()
        
        console.print("[green]✅ Video Functions Manager ready![/green]")
        
        # Get capabilities report
        capabilities = manager.get_all_video_capabilities()
        
        console.print("\n[cyan]📊 Current Capabilities:[/cyan]")
        for capability, status in capabilities.items():
            if isinstance(status, dict) and 'available' in status:
                available = "✅" if status['available'] else "❌"
                console.print(f"  {available} {capability.replace('_', ' ').title()}")
        
        # Get performance report
        report = manager.get_performance_report()
        
        console.print("\n[cyan]📈 Performance Summary:[/cyan]")
        metrics = report.get('performance_summary', {})
        for metric, value in metrics.items():
            if metric != 'last_updated':
                console.print(f"  • {metric.replace('_', ' ').title()}: {value}")
        
        # Show recommendations
        recommendations = report.get('recommendations', [])
        if recommendations:
            console.print("\n[cyan]💡 Recommendations:[/cyan]")
            for rec in recommendations:
                console.print(f"  • {rec}")
        
        manager.save_performance_data()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
