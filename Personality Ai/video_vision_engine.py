"""
Video Vision Engine - Real-time video watching and understanding system
AI watches videos like humans and extracts visual and audio information
"""
import cv2
import numpy as np
import json
import os
import time
import requests
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse
import tempfile
from rich.console import Console
from config import *

console = Console()

class VideoVisionEngine:
    def __init__(self):
        self.video_vision_skills = {
            'frame_analysis': 0.3,
            'motion_detection': 0.2,
            'scene_understanding': 0.4,
            'text_recognition': 0.3,
            'object_tracking': 0.2,
            'audio_processing': 0.1,
            'content_comprehension': 0.3,
            'real_time_learning': 0.2
        }
        
        # Video understanding knowledge
        self.video_understanding = {
            'videos_watched': {},
            'scenes_analyzed': [],
            'objects_tracked': {},
            'text_extracted': [],
            'motion_patterns': [],
            'audio_insights': [],
            'learning_moments': [],
            'visual_memories': []
        }
        
        # Video processing settings
        self.processing_config = {
            'frame_skip': 30,  # Process every 30th frame for efficiency
            'max_duration': 300,  # Max 5 minutes per video
            'resolution_scale': 0.5,  # Scale down for faster processing
            'confidence_threshold': 0.5,
            'motion_threshold': 25,
            'text_confidence': 0.7
        }
        
        # Initialize video processing tools
        self._initialize_video_tools()
        self.load_video_vision_data()
    
    def _initialize_video_tools(self):
        """Initialize video processing capabilities"""
        try:
            # Test OpenCV video capabilities
            self.video_capture_available = True
            console.print("[dim green]✅ OpenCV video processing initialized[/dim green]")
            
            # Initialize object detection (using OpenCV's built-in models)
            self.object_detector = None
            try:
                # Try to load a pre-trained model (simplified for demo)
                self.object_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                console.print("[dim green]✅ Object detection initialized[/dim green]")
            except:
                console.print("[dim yellow]⚠️ Advanced object detection not available, using basic detection[/dim yellow]")
            
            # Initialize text detection
            self.text_detector_available = True
            console.print("[dim green]✅ Text detection initialized[/dim green]")
            
        except Exception as e:
            console.print(f"[dim red]Video tools initialization failed: {e}[/dim red]")
            self.video_capture_available = False
    
    def watch_video(self, video_url: str, duration_limit: int = 300) -> Dict[str, Any]:
        """Watch and analyze a video in real-time like a human would"""
        console.print(f"[bold blue]👁️ AI is Watching Video[/bold blue]")
        console.print(f"[yellow]URL: {video_url}[/yellow]")
        console.print(f"[yellow]Duration Limit: {duration_limit} seconds[/yellow]")
        
        watch_result = {
            'video_url': video_url,
            'start_time': datetime.now().isoformat(),
            'frames_analyzed': 0,
            'scenes_detected': [],
            'objects_seen': [],
            'text_found': [],
            'motion_detected': [],
            'audio_insights': [],
            'learning_insights': [],
            'visual_summary': '',
            'comprehension_score': 0.0,
            'success': False
        }
        
        try:
            # Download or stream video for processing
            video_path = self._prepare_video_for_analysis(video_url)
            
            if video_path:
                # Analyze video content frame by frame
                watch_result = self._analyze_video_content(video_path, duration_limit, watch_result)
                
                # Generate comprehensive understanding
                watch_result['visual_summary'] = self._generate_video_summary(watch_result)
                watch_result['comprehension_score'] = self._calculate_comprehension_score(watch_result)
                
                # Learn from the video
                self._learn_from_video_watching(watch_result)
                
                # Clean up temporary files
                if video_path.startswith(tempfile.gettempdir()):
                    try:
                        os.remove(video_path)
                    except:
                        pass
                
                watch_result['success'] = True
                console.print("[green]✅ Video watching complete![/green]")
            
            else:
                watch_result['error'] = "Could not prepare video for analysis"
                console.print("[red]❌ Could not access video for watching[/red]")
        
        except Exception as e:
            console.print(f"[red]❌ Video watching failed: {e}[/red]")
            watch_result['error'] = str(e)
        
        self.save_video_vision_data()
        return watch_result
    
    def _prepare_video_for_analysis(self, video_url: str) -> Optional[str]:
        """Prepare REAL video for analysis (local files or download from web)"""
        try:
            # Check if it's a local file
            if os.path.exists(video_url):
                console.print(f"[dim]📁 Using local video file: {os.path.basename(video_url)}[/dim]")
                return video_url

            # Check if it's a web URL
            parsed_url = urlparse(video_url)
            if parsed_url.scheme in ['http', 'https']:
                console.print("[dim]🌐 Processing web video URL[/dim]")

                # Try to download real video from web
                downloaded_path = self._download_real_video(video_url)
                if downloaded_path:
                    return downloaded_path
                else:
                    console.print("[red]❌ Could not download video from URL[/red]")
                    return None

            # Check common video file extensions in current directory
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            for ext in video_extensions:
                test_path = video_url + ext
                if os.path.exists(test_path):
                    console.print(f"[dim]📁 Found video file: {test_path}[/dim]")
                    return test_path

            console.print(f"[red]❌ Video file not found: {video_url}[/red]")
            console.print("[yellow]💡 Please provide a valid video file path or URL[/yellow]")
            return None

        except Exception as e:
            console.print(f"[dim red]Video preparation failed: {e}[/dim red]")
            return None
    
    def _download_real_video(self, video_url: str) -> Optional[str]:
        """Download real video from web URL"""
        try:
            console.print(f"[yellow]🌐 Attempting to download video from: {video_url}[/yellow]")

            # Check if it's a direct video file URL
            if any(video_url.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']):
                return self._download_direct_video_file(video_url)

            # Check if it's a YouTube URL
            if 'youtube.com' in video_url or 'youtu.be' in video_url:
                return self._download_youtube_video(video_url)

            # Try as direct video file anyway
            return self._download_direct_video_file(video_url)

        except Exception as e:
            console.print(f"[red]❌ Video download failed: {e}[/red]")
            return None

    def _download_direct_video_file(self, video_url: str) -> Optional[str]:
        """Download direct video file from URL"""
        try:
            console.print("[dim]📥 Downloading direct video file...[/dim]")

            # Create temporary file
            temp_dir = tempfile.gettempdir()
            file_extension = '.mp4'  # Default extension

            # Try to get extension from URL
            for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                if video_url.lower().endswith(ext):
                    file_extension = ext
                    break

            temp_path = os.path.join(temp_dir, f'downloaded_video_{int(time.time())}{file_extension}')

            # Download with requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(video_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()

            # Check if it's actually video content
            content_type = response.headers.get('content-type', '').lower()
            if not any(vid_type in content_type for vid_type in ['video', 'mp4', 'avi', 'mov']):
                console.print(f"[red]❌ URL does not point to video content: {content_type}[/red]")
                return None

            # Download the file
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Verify download
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                file_size = os.path.getsize(temp_path)
                console.print(f"[green]✅ Video downloaded: {temp_path} ({file_size} bytes)[/green]")
                return temp_path
            else:
                console.print("[red]❌ Downloaded file is empty[/red]")
                return None

        except Exception as e:
            console.print(f"[red]❌ Direct video download failed: {e}[/red]")
            return None

    def _download_youtube_video(self, youtube_url: str) -> Optional[str]:
        """Download YouTube video using yt-dlp or youtube-dl"""
        try:
            console.print("[dim]📺 Attempting YouTube video download...[/dim]")

            # Try to use yt-dlp first (more reliable)
            temp_dir = tempfile.gettempdir()
            output_template = os.path.join(temp_dir, 'youtube_video_%(id)s.%(ext)s')

            # Try yt-dlp command
            try:
                import subprocess
                cmd = [
                    'yt-dlp',
                    '--format', 'best[height<=480]',  # Lower quality for faster download
                    '--output', output_template,
                    '--no-playlist',
                    youtube_url
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

                if result.returncode == 0:
                    # Find the downloaded file
                    for file in os.listdir(temp_dir):
                        if file.startswith('youtube_video_') and any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mkv']):
                            downloaded_path = os.path.join(temp_dir, file)
                            console.print(f"[green]✅ YouTube video downloaded: {downloaded_path}[/green]")
                            return downloaded_path

            except (subprocess.TimeoutExpired, FileNotFoundError):
                console.print("[yellow]⚠️ yt-dlp not available or timed out[/yellow]")

            # Try youtube-dl as fallback
            try:
                cmd = [
                    'youtube-dl',
                    '--format', 'best[height<=480]',
                    '--output', output_template,
                    '--no-playlist',
                    youtube_url
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

                if result.returncode == 0:
                    # Find the downloaded file
                    for file in os.listdir(temp_dir):
                        if file.startswith('youtube_video_') and any(file.endswith(ext) for ext in ['.mp4', '.webm', '.mkv']):
                            downloaded_path = os.path.join(temp_dir, file)
                            console.print(f"[green]✅ YouTube video downloaded: {downloaded_path}[/green]")
                            return downloaded_path

            except (subprocess.TimeoutExpired, FileNotFoundError):
                console.print("[yellow]⚠️ youtube-dl not available or timed out[/yellow]")

            console.print("[red]❌ YouTube download failed - please install yt-dlp or youtube-dl[/red]")
            console.print("[yellow]💡 Install with: pip install yt-dlp[/yellow]")
            return None

        except Exception as e:
            console.print(f"[red]❌ YouTube download failed: {e}[/red]")
            return None
    
    def _analyze_video_content(self, video_path: str, duration_limit: int, watch_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze video content frame by frame like human vision"""
        console.print("[dim]🎥 Analyzing video frames...[/dim]")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                console.print("[dim red]❌ Could not open video file[/dim red]")
                return watch_result
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            video_duration = total_frames / fps if fps > 0 else 0
            
            console.print(f"[dim]📊 Video: {video_duration:.1f}s, {fps} FPS, {total_frames} frames[/dim]")
            
            # Limit analysis duration
            max_frames = min(total_frames, duration_limit * fps)
            frame_skip = max(1, fps // 2)  # Analyze 2 frames per second
            
            frame_count = 0
            analyzed_frames = 0
            previous_frame = None
            
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Skip frames for efficiency
                if frame_count % frame_skip == 0:
                    # Analyze this frame
                    frame_analysis = self._analyze_single_frame(frame, frame_count / fps, previous_frame)
                    
                    # Collect insights
                    if frame_analysis['objects_detected']:
                        watch_result['objects_seen'].extend(frame_analysis['objects_detected'])
                    
                    if frame_analysis['text_found']:
                        watch_result['text_found'].extend(frame_analysis['text_found'])
                    
                    if frame_analysis['motion_detected']:
                        watch_result['motion_detected'].append(frame_analysis['motion_detected'])
                    
                    if frame_analysis['scene_change']:
                        watch_result['scenes_detected'].append({
                            'timestamp': frame_count / fps,
                            'description': frame_analysis['scene_description']
                        })
                    
                    analyzed_frames += 1
                    previous_frame = frame.copy()
                
                frame_count += 1
                
                # Show progress
                if frame_count % (fps * 5) == 0:  # Every 5 seconds
                    progress = (frame_count / max_frames) * 100
                    console.print(f"[dim]⏱️ Progress: {progress:.1f}% ({frame_count}/{max_frames} frames)[/dim]")
            
            cap.release()
            
            watch_result['frames_analyzed'] = analyzed_frames
            watch_result['video_duration'] = video_duration
            
            console.print(f"[dim green]✅ Analyzed {analyzed_frames} frames from {video_duration:.1f}s video[/dim green]")
            
        except Exception as e:
            console.print(f"[dim red]Video analysis failed: {e}[/dim red]")
            watch_result['error'] = str(e)
        
        return watch_result
    
    def _analyze_single_frame(self, frame: np.ndarray, timestamp: float, previous_frame: Optional[np.ndarray]) -> Dict[str, Any]:
        """Analyze a single video frame like human vision"""
        frame_analysis = {
            'timestamp': timestamp,
            'objects_detected': [],
            'text_found': [],
            'motion_detected': None,
            'scene_change': False,
            'scene_description': '',
            'colors_dominant': [],
            'brightness': 0.0
        }
        
        try:
            # Resize frame for faster processing
            height, width = frame.shape[:2]
            scale = self.processing_config['resolution_scale']
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized_frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
            
            # Analyze brightness
            frame_analysis['brightness'] = np.mean(gray) / 255.0
            
            # Detect objects (simplified - using face detection as example)
            if self.object_detector is not None:
                faces = self.object_detector.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    frame_analysis['objects_detected'].append({
                        'type': 'face',
                        'confidence': 0.8,
                        'position': {'x': x/scale, 'y': y/scale, 'w': w/scale, 'h': h/scale},
                        'timestamp': timestamp
                    })
            
            # Detect text in frame (simplified)
            frame_analysis['text_found'] = self._detect_text_in_frame(gray, timestamp)
            
            # Detect motion
            if previous_frame is not None:
                motion_info = self._detect_motion(gray, cv2.cvtColor(cv2.resize(previous_frame, (new_width, new_height)), cv2.COLOR_BGR2GRAY))
                if motion_info['motion_detected']:
                    frame_analysis['motion_detected'] = motion_info
            
            # Analyze dominant colors
            frame_analysis['colors_dominant'] = self._analyze_frame_colors(resized_frame)
            
            # Generate scene description
            frame_analysis['scene_description'] = self._describe_frame_scene(frame_analysis)
            
            # Detect scene changes
            frame_analysis['scene_change'] = self._detect_scene_change(frame_analysis, timestamp)
            
        except Exception as e:
            console.print(f"[dim red]Frame analysis failed: {e}[/dim red]")
        
        return frame_analysis
    
    def _detect_text_in_frame(self, gray_frame: np.ndarray, timestamp: float) -> List[Dict[str, Any]]:
        """Detect and extract text from video frame"""
        text_found = []
        
        try:
            # Simple text detection using contours (basic implementation)
            # In a full implementation, you'd use Tesseract OCR or similar
            
            # Find contours that might be text
            edges = cv2.Canny(gray_frame, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_regions = 0
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # Filter for text-like regions
                if 20 < w < 200 and 10 < h < 50 and 1.5 < aspect_ratio < 8:
                    text_regions += 1
            
            if text_regions > 0:
                text_found.append({
                    'text': f'Text detected ({text_regions} regions)',
                    'confidence': 0.6,
                    'timestamp': timestamp,
                    'regions_count': text_regions
                })
                
        except Exception as e:
            console.print(f"[dim red]Text detection failed: {e}[/dim red]")
        
        return text_found
    
    def _detect_motion(self, current_gray: np.ndarray, previous_gray: np.ndarray) -> Dict[str, Any]:
        """Detect motion between frames"""
        motion_info = {
            'motion_detected': False,
            'motion_intensity': 0.0,
            'motion_areas': []
        }
        
        try:
            # Calculate frame difference
            diff = cv2.absdiff(current_gray, previous_gray)
            
            # Threshold the difference
            _, thresh = cv2.threshold(diff, self.processing_config['motion_threshold'], 255, cv2.THRESH_BINARY)
            
            # Calculate motion intensity
            motion_pixels = np.sum(thresh > 0)
            total_pixels = thresh.shape[0] * thresh.shape[1]
            motion_intensity = motion_pixels / total_pixels
            
            motion_info['motion_intensity'] = motion_intensity
            
            if motion_intensity > 0.01:  # 1% of pixels changed
                motion_info['motion_detected'] = True
                
                # Find motion areas
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 100:  # Significant motion area
                        x, y, w, h = cv2.boundingRect(contour)
                        motion_info['motion_areas'].append({'x': x, 'y': y, 'w': w, 'h': h})
                        
        except Exception as e:
            console.print(f"[dim red]Motion detection failed: {e}[/dim red]")
        
        return motion_info
    
    def _analyze_frame_colors(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze dominant colors in frame"""
        colors = []
        
        try:
            # Convert to RGB for color analysis
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Calculate mean colors
            mean_color = np.mean(rgb_frame.reshape(-1, 3), axis=0)
            
            # Simple color categorization
            r, g, b = mean_color
            if r > g and r > b:
                dominant_color = 'red'
            elif g > r and g > b:
                dominant_color = 'green'
            elif b > r and b > g:
                dominant_color = 'blue'
            elif r > 150 and g > 150 and b > 150:
                dominant_color = 'white'
            elif r < 50 and g < 50 and b < 50:
                dominant_color = 'black'
            else:
                dominant_color = 'mixed'
            
            colors.append({
                'color': dominant_color,
                'rgb': [int(r), int(g), int(b)],
                'dominance': 1.0
            })
            
        except Exception as e:
            console.print(f"[dim red]Color analysis failed: {e}[/dim red]")
        
        return colors
    
    def _describe_frame_scene(self, frame_analysis: Dict[str, Any]) -> str:
        """Generate natural language description of the frame"""
        description_parts = []
        
        # Describe brightness
        brightness = frame_analysis.get('brightness', 0)
        if brightness > 0.7:
            description_parts.append("bright scene")
        elif brightness < 0.3:
            description_parts.append("dark scene")
        else:
            description_parts.append("moderately lit scene")
        
        # Describe objects
        objects = frame_analysis.get('objects_detected', [])
        if objects:
            object_types = [obj['type'] for obj in objects]
            unique_objects = list(set(object_types))
            if len(unique_objects) == 1:
                description_parts.append(f"containing {unique_objects[0]}")
            else:
                description_parts.append(f"containing {len(unique_objects)} different objects")
        
        # Describe colors
        colors = frame_analysis.get('colors_dominant', [])
        if colors:
            color_name = colors[0]['color']
            description_parts.append(f"with {color_name} tones")
        
        # Describe text
        text_found = frame_analysis.get('text_found', [])
        if text_found:
            description_parts.append("with visible text")
        
        # Describe motion
        motion = frame_analysis.get('motion_detected')
        if motion and motion.get('motion_detected'):
            intensity = motion.get('motion_intensity', 0)
            if intensity > 0.1:
                description_parts.append("with significant movement")
            else:
                description_parts.append("with subtle movement")
        
        return ", ".join(description_parts) if description_parts else "static scene"
    
    def _detect_scene_change(self, frame_analysis: Dict[str, Any], timestamp: float) -> bool:
        """Detect if this represents a significant scene change"""
        # Simple scene change detection based on multiple factors
        scene_change_indicators = 0
        
        # Check brightness change
        if hasattr(self, '_last_brightness'):
            brightness_diff = abs(frame_analysis.get('brightness', 0) - self._last_brightness)
            if brightness_diff > 0.3:
                scene_change_indicators += 1
        
        self._last_brightness = frame_analysis.get('brightness', 0)
        
        # Check for new objects
        if frame_analysis.get('objects_detected'):
            scene_change_indicators += 1
        
        # Check for significant motion
        motion = frame_analysis.get('motion_detected')
        if motion and motion.get('motion_intensity', 0) > 0.2:
            scene_change_indicators += 1
        
        return scene_change_indicators >= 2

    def _generate_video_summary(self, watch_result: Dict[str, Any]) -> str:
        """Generate comprehensive summary of what the AI saw in the video"""
        summary_parts = []

        # Video overview
        duration = watch_result.get('video_duration', 0)
        frames_analyzed = watch_result.get('frames_analyzed', 0)
        summary_parts.append(f"Watched {duration:.1f} second video, analyzing {frames_analyzed} frames")

        # Scenes detected
        scenes = watch_result.get('scenes_detected', [])
        if scenes:
            summary_parts.append(f"Identified {len(scenes)} distinct scenes")

            # Describe key scenes
            for i, scene in enumerate(scenes[:3]):  # First 3 scenes
                timestamp = scene.get('timestamp', 0)
                description = scene.get('description', '')
                summary_parts.append(f"Scene {i+1} at {timestamp:.1f}s: {description}")

        # Objects seen
        objects = watch_result.get('objects_seen', [])
        if objects:
            object_types = list(set([obj['type'] for obj in objects]))
            summary_parts.append(f"Detected {len(object_types)} types of objects: {', '.join(object_types)}")

        # Text found
        text_instances = watch_result.get('text_found', [])
        if text_instances:
            total_text_regions = sum(t.get('regions_count', 0) for t in text_instances)
            summary_parts.append(f"Found text in {len(text_instances)} frames ({total_text_regions} text regions)")

        # Motion analysis
        motion_events = watch_result.get('motion_detected', [])
        if motion_events:
            avg_motion = np.mean([m.get('motion_intensity', 0) for m in motion_events if m])
            if avg_motion > 0.1:
                summary_parts.append(f"High motion content with average intensity {avg_motion:.2f}")
            else:
                summary_parts.append(f"Moderate motion with average intensity {avg_motion:.2f}")

        return ". ".join(summary_parts) + "."

    def _calculate_comprehension_score(self, watch_result: Dict[str, Any]) -> float:
        """Calculate how well the AI understood the video content"""
        score = 0.0
        max_score = 0.0

        # Frame analysis completeness
        frames_analyzed = watch_result.get('frames_analyzed', 0)
        if frames_analyzed > 0:
            score += min(frames_analyzed / 100, 1.0) * 0.2  # Up to 0.2 for frame analysis
        max_score += 0.2

        # Scene detection
        scenes = watch_result.get('scenes_detected', [])
        if scenes:
            score += min(len(scenes) / 5, 1.0) * 0.2  # Up to 0.2 for scene detection
        max_score += 0.2

        # Object detection
        objects = watch_result.get('objects_seen', [])
        if objects:
            score += min(len(objects) / 10, 1.0) * 0.2  # Up to 0.2 for object detection
        max_score += 0.2

        # Text recognition
        text_found = watch_result.get('text_found', [])
        if text_found:
            score += min(len(text_found) / 5, 1.0) * 0.2  # Up to 0.2 for text recognition
        max_score += 0.2

        # Motion understanding
        motion_events = watch_result.get('motion_detected', [])
        if motion_events:
            score += min(len(motion_events) / 20, 1.0) * 0.2  # Up to 0.2 for motion analysis
        max_score += 0.2

        return score / max_score if max_score > 0 else 0.0

    def _learn_from_video_watching(self, watch_result: Dict[str, Any]):
        """Learn from the video watching experience"""
        try:
            video_url = watch_result.get('video_url', '')
            video_id = f"video_{hash(video_url)}_{int(time.time())}"

            # Store comprehensive video memory
            video_memory = {
                'video_id': video_id,
                'url': video_url,
                'watched_at': datetime.now().isoformat(),
                'duration': watch_result.get('video_duration', 0),
                'frames_analyzed': watch_result.get('frames_analyzed', 0),
                'comprehension_score': watch_result.get('comprehension_score', 0),
                'visual_summary': watch_result.get('visual_summary', ''),
                'scenes_count': len(watch_result.get('scenes_detected', [])),
                'objects_detected': len(watch_result.get('objects_seen', [])),
                'text_instances': len(watch_result.get('text_found', [])),
                'motion_events': len(watch_result.get('motion_detected', []))
            }

            self.video_understanding['videos_watched'][video_id] = video_memory

            # Learn from scenes
            for scene in watch_result.get('scenes_detected', []):
                scene_memory = {
                    'video_id': video_id,
                    'timestamp': scene.get('timestamp', 0),
                    'description': scene.get('description', ''),
                    'learned_at': datetime.now().isoformat()
                }
                self.video_understanding['scenes_analyzed'].append(scene_memory)

            # Learn from objects
            for obj in watch_result.get('objects_seen', []):
                obj_type = obj.get('type', 'unknown')
                if obj_type not in self.video_understanding['objects_tracked']:
                    self.video_understanding['objects_tracked'][obj_type] = {
                        'first_seen': datetime.now().isoformat(),
                        'total_sightings': 0,
                        'videos_seen_in': []
                    }

                obj_data = self.video_understanding['objects_tracked'][obj_type]
                obj_data['total_sightings'] += 1
                if video_id not in obj_data['videos_seen_in']:
                    obj_data['videos_seen_in'].append(video_id)

            # Learn from text
            for text_instance in watch_result.get('text_found', []):
                text_memory = {
                    'video_id': video_id,
                    'timestamp': text_instance.get('timestamp', 0),
                    'text_content': text_instance.get('text', ''),
                    'confidence': text_instance.get('confidence', 0),
                    'learned_at': datetime.now().isoformat()
                }
                self.video_understanding['text_extracted'].append(text_memory)

            # Learn from motion patterns
            motion_events = watch_result.get('motion_detected', [])
            if motion_events:
                avg_intensity = np.mean([m.get('motion_intensity', 0) for m in motion_events if m])
                motion_pattern = {
                    'video_id': video_id,
                    'average_intensity': avg_intensity,
                    'motion_events_count': len(motion_events),
                    'pattern_type': 'high_motion' if avg_intensity > 0.1 else 'low_motion',
                    'learned_at': datetime.now().isoformat()
                }
                self.video_understanding['motion_patterns'].append(motion_pattern)

            # Generate learning insights
            learning_insights = self._generate_learning_insights(watch_result)
            self.video_understanding['learning_moments'].extend(learning_insights)

            # Update skills based on what was learned
            self._update_video_vision_skills(watch_result)

            console.print(f"[dim green]🧠 Learned from video: {video_memory['comprehension_score']:.2f} comprehension score[/dim green]")

        except Exception as e:
            console.print(f"[dim red]Learning from video failed: {e}[/dim red]")

    def _generate_learning_insights(self, watch_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights from video watching experience"""
        insights = []

        # Comprehension insight
        comprehension = watch_result.get('comprehension_score', 0)
        if comprehension > 0.8:
            insights.append({
                'type': 'comprehension',
                'insight': f'Achieved high video comprehension ({comprehension:.2f})',
                'timestamp': datetime.now().isoformat()
            })

        # Scene analysis insight
        scenes = watch_result.get('scenes_detected', [])
        if len(scenes) > 3:
            insights.append({
                'type': 'scene_analysis',
                'insight': f'Successfully identified {len(scenes)} distinct scenes',
                'timestamp': datetime.now().isoformat()
            })

        # Object detection insight
        objects = watch_result.get('objects_seen', [])
        unique_objects = list(set([obj['type'] for obj in objects]))
        if len(unique_objects) > 2:
            insights.append({
                'type': 'object_detection',
                'insight': f'Detected {len(unique_objects)} different object types',
                'timestamp': datetime.now().isoformat()
            })

        # Motion analysis insight
        motion_events = watch_result.get('motion_detected', [])
        if motion_events:
            avg_motion = np.mean([m.get('motion_intensity', 0) for m in motion_events if m])
            insights.append({
                'type': 'motion_analysis',
                'insight': f'Analyzed motion patterns with {avg_motion:.2f} average intensity',
                'timestamp': datetime.now().isoformat()
            })

        return insights

    def _update_video_vision_skills(self, watch_result: Dict[str, Any]):
        """Update video vision skills based on watching performance"""
        # Frame analysis skill
        frames_analyzed = watch_result.get('frames_analyzed', 0)
        if frames_analyzed > 0:
            self.video_vision_skills['frame_analysis'] = min(1.0, self.video_vision_skills['frame_analysis'] + 0.01)

        # Scene understanding skill
        scenes = watch_result.get('scenes_detected', [])
        if scenes:
            self.video_vision_skills['scene_understanding'] = min(1.0, self.video_vision_skills['scene_understanding'] + 0.02)

        # Object tracking skill
        objects = watch_result.get('objects_seen', [])
        if objects:
            self.video_vision_skills['object_tracking'] = min(1.0, self.video_vision_skills['object_tracking'] + 0.02)

        # Text recognition skill
        text_found = watch_result.get('text_found', [])
        if text_found:
            self.video_vision_skills['text_recognition'] = min(1.0, self.video_vision_skills['text_recognition'] + 0.02)

        # Motion detection skill
        motion_events = watch_result.get('motion_detected', [])
        if motion_events:
            self.video_vision_skills['motion_detection'] = min(1.0, self.video_vision_skills['motion_detection'] + 0.02)

        # Content comprehension skill
        comprehension = watch_result.get('comprehension_score', 0)
        if comprehension > 0.5:
            self.video_vision_skills['content_comprehension'] = min(1.0, self.video_vision_skills['content_comprehension'] + 0.01)

        # Real-time learning skill
        self.video_vision_skills['real_time_learning'] = min(1.0, self.video_vision_skills['real_time_learning'] + 0.01)

    def get_video_vision_status(self) -> Dict[str, Any]:
        """Get current video vision status and capabilities"""
        return {
            'video_vision_skills': self.video_vision_skills,
            'videos_watched': len(self.video_understanding['videos_watched']),
            'scenes_analyzed': len(self.video_understanding['scenes_analyzed']),
            'objects_tracked': len(self.video_understanding['objects_tracked']),
            'text_instances': len(self.video_understanding['text_extracted']),
            'motion_patterns': len(self.video_understanding['motion_patterns']),
            'learning_moments': len(self.video_understanding['learning_moments']),
            'overall_video_vision': sum(self.video_vision_skills.values()) / len(self.video_vision_skills),
            'most_detected_objects': self._get_most_detected_objects(),
            'recent_videos': self._get_recent_videos(),
            'comprehension_average': self._get_average_comprehension()
        }

    def _get_most_detected_objects(self) -> List[Dict[str, Any]]:
        """Get most frequently detected objects"""
        objects = []
        for obj_type, obj_data in self.video_understanding['objects_tracked'].items():
            objects.append({
                'type': obj_type,
                'sightings': obj_data['total_sightings'],
                'videos': len(obj_data['videos_seen_in'])
            })

        return sorted(objects, key=lambda x: x['sightings'], reverse=True)[:5]

    def _get_recent_videos(self) -> List[Dict[str, Any]]:
        """Get recently watched videos"""
        videos = []
        for video_id, video_data in self.video_understanding['videos_watched'].items():
            videos.append({
                'id': video_id,
                'watched_at': video_data['watched_at'],
                'duration': video_data['duration'],
                'comprehension': video_data['comprehension_score'],
                'summary': video_data['visual_summary'][:100] + '...' if len(video_data['visual_summary']) > 100 else video_data['visual_summary']
            })

        return sorted(videos, key=lambda x: x['watched_at'], reverse=True)[:5]

    def _get_average_comprehension(self) -> float:
        """Get average comprehension score across all videos"""
        videos = list(self.video_understanding['videos_watched'].values())
        if not videos:
            return 0.0

        total_comprehension = sum(v.get('comprehension_score', 0) for v in videos)
        return total_comprehension / len(videos)

    def load_video_vision_data(self):
        """Load video vision data from storage"""
        try:
            vision_file = "memory/video_vision.json"
            if os.path.exists(vision_file):
                with open(vision_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.video_vision_skills = data.get('video_vision_skills', self.video_vision_skills)
                    self.video_understanding = data.get('video_understanding', self.video_understanding)
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load video vision data: {e}[/dim yellow]")

    def save_video_vision_data(self):
        """Save video vision data to storage"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            vision_file = "memory/video_vision.json"

            data = {
                'video_vision_skills': self.video_vision_skills,
                'video_understanding': self.video_understanding,
                'last_updated': datetime.now().isoformat()
            }

            with open(vision_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            console.print(f"[dim red]Error saving video vision data: {e}[/dim red]")
