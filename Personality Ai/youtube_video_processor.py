#!/usr/bin/env python3
"""
YouTube Video Processor - Download and analyze real YouTube videos
"""

import sys
import os
import subprocess
import tempfile
import time
from rich.console import Console
from rich.panel import Panel

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

def install_youtube_downloader():
    """Install yt-dlp for YouTube video downloading"""
    console.print("[yellow]📦 Installing YouTube video downloader...[/yellow]")
    
    try:
        # Try to install yt-dlp
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            console.print("[green]✅ yt-dlp installed successfully![/green]")
            return True
        else:
            console.print(f"[red]❌ yt-dlp installation failed: {result.stderr}[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ Installation failed: {e}[/red]")
        return False

def check_youtube_downloader():
    """Check if YouTube downloader is available"""
    try:
        # Check for yt-dlp
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            console.print(f"[green]✅ yt-dlp available: {result.stdout.strip()}[/green]")
            return 'yt-dlp'
    except:
        pass
    
    try:
        # Check for youtube-dl
        result = subprocess.run(['youtube-dl', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            console.print(f"[green]✅ youtube-dl available: {result.stdout.strip()}[/green]")
            return 'youtube-dl'
    except:
        pass
    
    console.print("[yellow]⚠️ No YouTube downloader found[/yellow]")
    return None

def download_youtube_video(youtube_url: str, max_duration: int = 300) -> str:
    """Download a YouTube video for analysis"""
    console.print(f"[bold blue]📺 Downloading YouTube Video[/bold blue]")
    console.print(f"[yellow]URL: {youtube_url}[/yellow]")
    console.print(f"[yellow]Max Duration: {max_duration} seconds[/yellow]")
    
    try:
        # Check for downloader
        downloader = check_youtube_downloader()
        
        if not downloader:
            console.print("[yellow]Installing YouTube downloader...[/yellow]")
            if install_youtube_downloader():
                downloader = 'yt-dlp'
            else:
                console.print("[red]❌ Could not install YouTube downloader[/red]")
                return None
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, 'youtube_%(id)s.%(ext)s')
        
        console.print("[dim]📥 Downloading video...[/dim]")
        
        # Download command
        if downloader == 'yt-dlp':
            cmd = [
                'yt-dlp',
                '--format', 'best[height<=720][duration<=300]',  # Max 720p, 5 minutes
                '--output', output_template,
                '--no-playlist',
                '--extract-flat', 'false',
                youtube_url
            ]
        else:  # youtube-dl
            cmd = [
                'youtube-dl',
                '--format', 'best[height<=720]',
                '--output', output_template,
                '--no-playlist',
                youtube_url
            ]
        
        # Execute download
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Find downloaded file
            for file in os.listdir(temp_dir):
                if file.startswith('youtube_') and any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mkv']):
                    downloaded_path = os.path.join(temp_dir, file)
                    file_size = os.path.getsize(downloaded_path)
                    console.print(f"[green]✅ YouTube video downloaded: {file} ({file_size} bytes)[/green]")
                    return downloaded_path
            
            console.print("[red]❌ Downloaded file not found[/red]")
            return None
        else:
            console.print(f"[red]❌ Download failed: {result.stderr}[/red]")
            return None
            
    except subprocess.TimeoutExpired:
        console.print("[red]❌ Download timed out[/red]")
        return None
    except Exception as e:
        console.print(f"[red]❌ Download failed: {e}[/red]")
        return None

def test_youtube_video_analysis():
    """Test AI video analysis with real YouTube video"""
    console.print("[bold blue]🎥 Testing YouTube Video Analysis[/bold blue]")
    console.print("=" * 60)
    
    # Educational YouTube videos for testing
    test_videos = [
        "https://www.youtube.com/watch?v=aircAruvnKk",  # 3Blue1Brown - Neural Networks
        "https://www.youtube.com/watch?v=IHZwWFHWa-w",  # 3Blue1Brown - What is a neural network?
        "https://www.youtube.com/watch?v=kft1AJ9WVDk",  # Short educational video
    ]
    
    console.print("[yellow]📺 Available test videos:[/yellow]")
    for i, url in enumerate(test_videos, 1):
        console.print(f"  {i}. {url}")
    
    # Let user choose or use first one
    test_url = test_videos[0]
    console.print(f"\n[cyan]Using test video: {test_url}[/cyan]")
    
    try:
        # Download video
        video_path = download_youtube_video(test_url, max_duration=120)  # 2 minutes max
        
        if not video_path:
            console.print("[red]❌ Could not download YouTube video[/red]")
            return False
        
        # Initialize AI
        from main_ai import PersonalityAI
        console.print("[yellow]Initializing AI...[/yellow]")
        ai = PersonalityAI()
        
        # Analyze the video
        console.print(f"\n[cyan]👁️ AI analyzing YouTube video...[/cyan]")
        watch_result = ai.video_vision.watch_video(video_path, duration_limit=120)
        
        if watch_result.get('success', False):
            console.print("[green]✅ YouTube video analysis successful![/green]")
            
            # Show comprehensive results
            frames_analyzed = watch_result.get('frames_analyzed', 0)
            video_duration = watch_result.get('video_duration', 0)
            scenes_detected = len(watch_result.get('scenes_detected', []))
            objects_seen = len(watch_result.get('objects_seen', []))
            text_found = len(watch_result.get('text_found', []))
            motion_events = len(watch_result.get('motion_detected', []))
            comprehension = watch_result.get('comprehension_score', 0)
            
            console.print(f"\n[cyan]📊 YouTube Video Analysis:[/cyan]")
            console.print(f"  🎬 Video Duration: {video_duration:.1f} seconds")
            console.print(f"  📹 Frames Analyzed: {frames_analyzed}")
            console.print(f"  🎭 Scenes Detected: {scenes_detected}")
            console.print(f"  🎯 Objects Seen: {objects_seen}")
            console.print(f"  📝 Text Found: {text_found}")
            console.print(f"  🏃 Motion Events: {motion_events}")
            console.print(f"  🧠 Comprehension Score: {comprehension:.2f}")
            
            # Show what AI understood
            visual_summary = watch_result.get('visual_summary', '')
            if visual_summary:
                console.print(f"\n[cyan]👁️ AI's understanding of YouTube video:[/cyan]")
                console.print(f"  {visual_summary}")
            
            # Show educational assessment
            if comprehension > 0.7:
                console.print(f"\n[green]🎓 High comprehension - AI understood the educational content well![/green]")
            elif comprehension > 0.5:
                console.print(f"\n[yellow]📚 Good comprehension - AI grasped most of the content[/yellow]")
            else:
                console.print(f"\n[red]🤔 Basic comprehension - AI needs more practice with this content type[/red]")
            
            # Clean up
            try:
                os.remove(video_path)
                console.print(f"[dim]🗑️ Cleaned up downloaded video[/dim]")
            except:
                pass
            
            return True
            
        else:
            error_msg = watch_result.get('error', 'Unknown error')
            console.print(f"[red]❌ YouTube video analysis failed: {error_msg}[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ Test failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    console.print("[bold green]🧪 YouTube Video Analysis Test[/bold green]")
    console.print("Testing AI's ability to download and analyze real YouTube videos")
    console.print("=" * 60)
    
    # Check system requirements
    console.print("[yellow]🔧 Checking system requirements...[/yellow]")
    
    downloader = check_youtube_downloader()
    if not downloader:
        console.print("[yellow]📦 Installing YouTube downloader...[/yellow]")
        if not install_youtube_downloader():
            console.print("[red]❌ Could not install YouTube downloader[/red]")
            console.print("\n[yellow]💡 Manual installation:[/yellow]")
            console.print("  pip install yt-dlp")
            console.print("  or")
            console.print("  pip install youtube-dl")
            return
    
    # Run test
    success = test_youtube_video_analysis()
    
    if success:
        console.print("\n[bold green]🎉 SUCCESS: YouTube Video Analysis Working![/bold green]")
        console.print("\n[cyan]Your AI can now:[/cyan]")
        console.print("  📺 Download real YouTube videos automatically")
        console.print("  👁️ Watch and analyze educational content")
        console.print("  🎬 Understand video scenes and transitions")
        console.print("  📝 Read text and graphics in videos")
        console.print("  🏃 Analyze motion and visual dynamics")
        console.print("  🧠 Generate comprehension scores for real content")
        console.print("  📚 Learn from actual educational videos")
        
        console.print("\n[bold yellow]🎯 Try with any YouTube video:[/bold yellow]")
        console.print("  python main_ai.py interactive")
        console.print("  Then use: watch_video https://youtube.com/watch?v=...")
        
    else:
        console.print("\n[bold red]❌ FAILED: YouTube video analysis had issues[/bold red]")

if __name__ == "__main__":
    main()
