#!/usr/bin/env python3
"""
Video Vision Interface - Real video watching and analysis interface
Production-ready video vision capabilities
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class VideoVisionInterface:
    """Real video vision interface for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.vision_history = []
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.webm', '.flv']
        
    def watch_video_file(self, video_path: str, duration_limit: int = 300) -> Dict[str, Any]:
        """Watch and analyze a real video file"""
        
        if not self.ai:
            return {'success': False, 'error': 'AI instance not available'}
        
        if not os.path.exists(video_path):
            return {'success': False, 'error': f'Video file not found: {video_path}'}
        
        # Check file format
        file_ext = os.path.splitext(video_path)[1].lower()
        if file_ext not in self.supported_formats:
            return {'success': False, 'error': f'Unsupported format: {file_ext}'}
        
        console.print(f"[yellow]👁️ AI watching video: {video_path}[/yellow]")
        console.print(f"[dim]Duration limit: {duration_limit} seconds[/dim]")
        
        try:
            # Execute real video vision
            vision_result = self.ai.video_vision.watch_video(video_path, duration_limit=duration_limit)
            
            if vision_result.get('success', False):
                # Store in history
                self.vision_history.append({
                    'video_path': video_path,
                    'timestamp': datetime.now().isoformat(),
                    'result': vision_result
                })
                
                console.print("[green]✅ Video analysis complete![/green]")
                
                # Display results
                self._display_vision_results(vision_result, video_path)
                
                return vision_result
            else:
                error_msg = vision_result.get('error', 'Unknown error')
                console.print(f"[red]❌ Video analysis failed: {error_msg}[/red]")
                return vision_result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            console.print(f"[red]❌ Video vision error: {e}[/red]")
            return error_result
    
    def watch_youtube_video(self, youtube_url: str, duration_limit: int = 300) -> Dict[str, Any]:
        """Watch and analyze a YouTube video"""
        
        if not self.ai:
            return {'success': False, 'error': 'AI instance not available'}
        
        console.print(f"[yellow]📺 AI watching YouTube video: {youtube_url}[/yellow]")
        console.print(f"[dim]Duration limit: {duration_limit} seconds[/dim]")
        
        try:
            # Execute real YouTube video vision
            vision_result = self.ai.video_vision.watch_video(youtube_url, duration_limit=duration_limit)
            
            if vision_result.get('success', False):
                # Store in history
                self.vision_history.append({
                    'video_url': youtube_url,
                    'timestamp': datetime.now().isoformat(),
                    'result': vision_result
                })
                
                console.print("[green]✅ YouTube video analysis complete![/green]")
                
                # Display results
                self._display_vision_results(vision_result, youtube_url)
                
                return vision_result
            else:
                error_msg = vision_result.get('error', 'Unknown error')
                console.print(f"[red]❌ YouTube video analysis failed: {error_msg}[/red]")
                return vision_result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            console.print(f"[red]❌ YouTube video vision error: {e}[/red]")
            return error_result
    
    def _display_vision_results(self, result: Dict[str, Any], video_source: str):
        """Display video vision analysis results"""
        
        console.print(f"\n[bold cyan]👁️ Video Vision Analysis Results[/bold cyan]")
        console.print(f"[dim]Source: {video_source}[/dim]")
        
        # Basic metrics
        table = Table(title="Analysis Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Frames Analyzed", str(result.get('frames_analyzed', 0)))
        table.add_row("Comprehension Score", f"{result.get('comprehension_score', 0):.2f}")
        table.add_row("Processing Time", f"{result.get('processing_time', 0):.1f}s")
        table.add_row("Video Duration", f"{result.get('video_duration', 0):.1f}s")
        
        console.print(table)
        
        # Text found in video
        text_found = result.get('text_found', [])
        if text_found:
            console.print(f"\n[cyan]📝 Text Found in Video ({len(text_found)} instances):[/cyan]")
            for i, text_item in enumerate(text_found[:10], 1):  # Show first 10
                text_content = text_item.get('text', 'Unknown')
                confidence = text_item.get('confidence', 0)
                console.print(f"  {i}. {text_content} (confidence: {confidence:.2f})")
            
            if len(text_found) > 10:
                console.print(f"  ... and {len(text_found) - 10} more")
        
        # Objects detected
        objects_detected = result.get('objects_detected', [])
        if objects_detected:
            console.print(f"\n[cyan]🎯 Objects Detected ({len(objects_detected)} types):[/cyan]")
            for obj in objects_detected[:8]:  # Show first 8
                obj_name = obj.get('name', 'Unknown')
                confidence = obj.get('confidence', 0)
                console.print(f"  • {obj_name} (confidence: {confidence:.2f})")
        
        # Motion analysis
        motion_events = result.get('motion_events', [])
        if motion_events:
            console.print(f"\n[cyan]🏃 Motion Analysis ({len(motion_events)} events):[/cyan]")
            for event in motion_events[:5]:  # Show first 5
                intensity = event.get('intensity', 0)
                timestamp = event.get('timestamp', 0)
                console.print(f"  • Motion at {timestamp:.1f}s (intensity: {intensity:.2f})")
        
        # Visual summary
        visual_summary = result.get('visual_summary', '')
        if visual_summary:
            console.print(f"\n[cyan]📊 Visual Summary:[/cyan]")
            console.print(f"  {visual_summary}")
        
        # Assessment
        assessment = result.get('assessment', '')
        if assessment:
            console.print(f"\n[cyan]🧠 AI Assessment:[/cyan]")
            console.print(f"  {assessment}")
    
    def get_vision_status(self) -> Dict[str, Any]:
        """Get current video vision status"""
        
        if not self.ai:
            return {'error': 'AI instance not available'}
        
        try:
            status = self.ai.video_vision.get_video_vision_status()
            
            # Add interface-specific data
            status['vision_history_count'] = len(self.vision_history)
            status['supported_formats'] = self.supported_formats
            status['interface_ready'] = True
            
            return status
            
        except Exception as e:
            return {'error': str(e), 'interface_ready': False}
    
    def show_vision_history(self, limit: int = 10):
        """Show recent video vision history"""
        
        if not self.vision_history:
            console.print("[yellow]No video vision history available[/yellow]")
            return
        
        console.print(f"[bold cyan]📹 Recent Video Vision History (last {limit})[/bold cyan]")
        
        table = Table()
        table.add_column("Time", style="dim")
        table.add_column("Source", style="cyan")
        table.add_column("Comprehension", style="green")
        table.add_column("Frames", style="yellow")
        table.add_column("Text Found", style="blue")
        
        for entry in self.vision_history[-limit:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            source = entry.get('video_path', entry.get('video_url', 'Unknown'))
            
            # Truncate long paths
            if len(source) > 40:
                source = "..." + source[-37:]
            
            result = entry['result']
            comprehension = f"{result.get('comprehension_score', 0):.2f}"
            frames = str(result.get('frames_analyzed', 0))
            text_count = str(len(result.get('text_found', [])))
            
            table.add_row(timestamp, source, comprehension, frames, text_count)
        
        console.print(table)
    
    def analyze_video_batch(self, video_paths: List[str], duration_limit: int = 300) -> Dict[str, Any]:
        """Analyze multiple videos in batch"""
        
        results = {
            'total_videos': len(video_paths),
            'successful_analyses': 0,
            'failed_analyses': 0,
            'results': [],
            'summary': {}
        }
        
        console.print(f"[yellow]🎬 Batch analyzing {len(video_paths)} videos...[/yellow]")
        
        for i, video_path in enumerate(video_paths, 1):
            console.print(f"\n[dim]Processing {i}/{len(video_paths)}: {video_path}[/dim]")
            
            result = self.watch_video_file(video_path, duration_limit)
            
            if result.get('success', False):
                results['successful_analyses'] += 1
            else:
                results['failed_analyses'] += 1
            
            results['results'].append({
                'video_path': video_path,
                'result': result
            })
        
        # Generate summary
        if results['successful_analyses'] > 0:
            total_frames = sum(r['result'].get('frames_analyzed', 0) for r in results['results'] if r['result'].get('success'))
            avg_comprehension = sum(r['result'].get('comprehension_score', 0) for r in results['results'] if r['result'].get('success')) / results['successful_analyses']
            
            results['summary'] = {
                'total_frames_analyzed': total_frames,
                'average_comprehension': avg_comprehension,
                'success_rate': results['successful_analyses'] / results['total_videos']
            }
        
        console.print(f"\n[green]✅ Batch analysis complete![/green]")
        console.print(f"[cyan]Success: {results['successful_analyses']}/{results['total_videos']}[/cyan]")
        
        return results
    
    def save_vision_history(self, filepath: str = "memory/video_vision_history.json"):
        """Save vision history to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            data = {
                'vision_history': self.vision_history,
                'supported_formats': self.supported_formats,
                'last_saved': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            console.print(f"[green]💾 Vision history saved to {filepath}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving vision history: {e}[/red]")
            return False
    
    def load_vision_history(self, filepath: str = "memory/video_vision_history.json"):
        """Load vision history from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.vision_history = data.get('vision_history', [])
                
                console.print(f"[green]📂 Vision history loaded from {filepath}[/green]")
                return True
            
        except Exception as e:
            console.print(f"[red]Error loading vision history: {e}[/red]")
            
        return False


def main():
    """Main function for standalone usage"""
    console.print("[bold green]👁️ Video Vision Interface[/bold green]")
    console.print("Real video watching and analysis interface")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        interface = VideoVisionInterface(ai)
        interface.load_vision_history()
        
        console.print("[green]✅ Video Vision Interface ready![/green]")
        
        # Show current status
        status = interface.get_vision_status()
        
        console.print("\n[cyan]📊 Current Status:[/cyan]")
        console.print(f"  👁️ Videos Watched: {status.get('videos_watched', 0)}")
        console.print(f"  🎬 Scenes Analyzed: {status.get('scenes_analyzed', 0)}")
        console.print(f"  📝 Text Instances: {status.get('text_instannces', 0)}")
        console.print(f"  🧠 Overall Vision: {status.get('overall_video_vision', 0):.3f}")
        console.print(f"  📈 Avg Comprehension: {status.get('comprehension_average', 0):.3f}")
        
        # Show supported formats
        console.print(f"\n[cyan]📁 Supported Formats:[/cyan]")
        console.print(f"  {', '.join(interface.supported_formats)}")
        
        # Show recent history
        if interface.vision_history:
            interface.show_vision_history(5)
        
        interface.save_vision_history()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
