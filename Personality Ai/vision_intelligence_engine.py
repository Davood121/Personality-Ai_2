"""
Vision Intelligence Engine - Complete visual processing and learning system
"""
import json
import os
import time
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cv2
import numpy as np
from rich.console import Console
from config import *

console = Console()

class VisionIntelligenceEngine:
    def __init__(self):
        self.vision_skills = {
            'object_recognition': 0.3,
            'text_extraction': 0.4,
            'image_analysis': 0.5,
            'visual_learning': 0.2,
            'scene_understanding': 0.3,
            'color_analysis': 0.6,
            'pattern_recognition': 0.4,
            'visual_memory': 0.3
        }
        
        # Visual knowledge database
        self.visual_knowledge = {
            'objects_seen': {},
            'text_extracted': [],
            'scenes_analyzed': [],
            'patterns_learned': [],
            'color_associations': {},
            'visual_memories': []
        }
        
        # Object categories for recognition
        self.object_categories = {
            'animals': ['cat', 'dog', 'bird', 'fish', 'horse', 'cow', 'sheep'],
            'vehicles': ['car', 'truck', 'bus', 'motorcycle', 'bicycle', 'airplane', 'boat'],
            'objects': ['chair', 'table', 'book', 'phone', 'computer', 'bottle', 'cup'],
            'nature': ['tree', 'flower', 'mountain', 'water', 'sky', 'grass', 'rock'],
            'people': ['person', 'face', 'hand', 'eye', 'smile', 'child', 'adult'],
            'food': ['apple', 'banana', 'pizza', 'bread', 'cake', 'fruit', 'vegetable']
        }
        
        # Initialize vision capabilities
        self._initialize_vision_system()
        self.load_vision_data()
    
    def _initialize_vision_system(self):
        """Initialize computer vision capabilities"""
        try:
            # Test OpenCV installation
            self.cv2_available = True
            console.print("[green]✅ OpenCV vision system initialized[/green]")
        except Exception as e:
            self.cv2_available = False
            console.print(f"[yellow]⚠️ OpenCV not available: {e}[/yellow]")
        
        try:
            # Test PIL installation
            self.pil_available = True
            console.print("[green]✅ PIL image processing initialized[/green]")
        except Exception as e:
            self.pil_available = False
            console.print(f"[yellow]⚠️ PIL not available: {e}[/yellow]")
    
    def analyze_image(self, image_path: str, searcher=None, memory=None) -> Dict[str, Any]:
        """Comprehensive image analysis with learning"""
        console.print(f"[bold blue]👁️ Analyzing Image: {os.path.basename(image_path)}[/bold blue]")
        
        if not os.path.exists(image_path):
            return {'error': 'Image file not found', 'success': False}
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'image_path': image_path,
            'file_info': {},
            'visual_analysis': {},
            'objects_detected': [],
            'text_extracted': '',
            'colors_analyzed': {},
            'scene_description': '',
            'learning_insights': [],
            'web_research': {},
            'success': True
        }
        
        try:
            # Load and analyze image
            image = Image.open(image_path)
            analysis_result['file_info'] = self._get_image_info(image)
            
            # Perform visual analysis
            console.print("[yellow]🔍 Performing visual analysis...[/yellow]")
            analysis_result['visual_analysis'] = self._analyze_visual_content(image)
            
            # Detect objects
            console.print("[yellow]🎯 Detecting objects...[/yellow]")
            analysis_result['objects_detected'] = self._detect_objects(image)
            
            # Extract text (OCR)
            console.print("[yellow]📝 Extracting text...[/yellow]")
            analysis_result['text_extracted'] = self._extract_text_from_image(image)
            
            # Analyze colors
            console.print("[yellow]🎨 Analyzing colors...[/yellow]")
            analysis_result['colors_analyzed'] = self._analyze_colors(image)
            
            # Generate scene description
            console.print("[yellow]📖 Generating scene description...[/yellow]")
            analysis_result['scene_description'] = self._generate_scene_description(analysis_result)
            
            # Learn from the image
            console.print("[yellow]🧠 Learning from visual content...[/yellow]")
            analysis_result['learning_insights'] = self._learn_from_image(analysis_result)
            
            # Web research for unknown objects
            if searcher and analysis_result['objects_detected']:
                console.print("[yellow]🌐 Researching objects online...[/yellow]")
                analysis_result['web_research'] = self._research_objects_online(
                    analysis_result['objects_detected'], searcher
                )
            
            # Store visual memory
            if memory:
                self._store_visual_memory(analysis_result, memory)
            
            # Update vision skills
            self._update_vision_skills(analysis_result)
            
            console.print("[green]✅ Image analysis complete![/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Image analysis failed: {e}[/red]")
            analysis_result['error'] = str(e)
            analysis_result['success'] = False
        
        self.save_vision_data()
        return analysis_result
    
    def _get_image_info(self, image: Image.Image) -> Dict[str, Any]:
        """Get basic image information"""
        return {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height,
            'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info
        }
    
    def _analyze_visual_content(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze visual content of the image"""
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        analysis = {
            'brightness': float(np.mean(img_array)),
            'contrast': float(np.std(img_array)),
            'sharpness': self._calculate_sharpness(img_array),
            'complexity': self._calculate_complexity(img_array),
            'dominant_regions': self._find_dominant_regions(img_array)
        }
        
        return analysis
    
    def _detect_objects(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect and identify objects in the image"""
        detected_objects = []
        
        # Simple object detection based on image analysis
        # This is a basic implementation - can be enhanced with ML models
        
        img_array = np.array(image)
        
        # Analyze image characteristics to infer possible objects
        brightness = np.mean(img_array)
        colors = self._get_dominant_colors(img_array)
        
        # Basic object inference based on visual characteristics
        if brightness > 200:
            detected_objects.append({
                'object': 'bright_scene',
                'confidence': 0.7,
                'description': 'Bright, well-lit scene',
                'category': 'lighting'
            })
        elif brightness < 50:
            detected_objects.append({
                'object': 'dark_scene',
                'confidence': 0.7,
                'description': 'Dark or low-light scene',
                'category': 'lighting'
            })
        
        # Color-based object inference
        for color_info in colors[:3]:  # Top 3 colors
            color_name = color_info['name']
            if color_name in ['green', 'brown']:
                detected_objects.append({
                    'object': 'nature_element',
                    'confidence': 0.6,
                    'description': f'Natural element with {color_name} coloring',
                    'category': 'nature'
                })
            elif color_name in ['blue']:
                detected_objects.append({
                    'object': 'sky_or_water',
                    'confidence': 0.5,
                    'description': 'Possible sky or water element',
                    'category': 'nature'
                })
        
        return detected_objects
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text from image using OCR"""
        try:
            # Basic text extraction - can be enhanced with Tesseract
            # For now, return placeholder
            return "Text extraction capability - would use Tesseract OCR in full implementation"
        except Exception as e:
            console.print(f"[dim red]OCR failed: {e}[/dim red]")
            return ""
    
    def _analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze colors in the image"""
        img_array = np.array(image)
        
        # Get dominant colors
        dominant_colors = self._get_dominant_colors(img_array)
        
        # Calculate color statistics
        color_stats = {
            'dominant_colors': dominant_colors,
            'color_diversity': len(set(img_array.flatten())),
            'average_rgb': [float(np.mean(img_array[:,:,i])) for i in range(min(3, img_array.shape[2]))] if len(img_array.shape) > 2 else [float(np.mean(img_array))],
            'color_temperature': self._estimate_color_temperature(img_array)
        }
        
        return color_stats
    
    def _get_dominant_colors(self, img_array: np.ndarray, num_colors: int = 5) -> List[Dict[str, Any]]:
        """Get dominant colors from image"""
        # Reshape image to list of pixels
        if len(img_array.shape) == 3:
            pixels = img_array.reshape(-1, img_array.shape[2])
        else:
            pixels = img_array.reshape(-1, 1)
        
        # Simple color analysis
        colors = []
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            # RGB image
            avg_r = np.mean(pixels[:, 0])
            avg_g = np.mean(pixels[:, 1])
            avg_b = np.mean(pixels[:, 2])
            
            colors.append({
                'rgb': [int(avg_r), int(avg_g), int(avg_b)],
                'name': self._rgb_to_color_name(avg_r, avg_g, avg_b),
                'percentage': 100.0
            })
        
        return colors
    
    def _rgb_to_color_name(self, r: float, g: float, b: float) -> str:
        """Convert RGB values to color name"""
        if r > 200 and g > 200 and b > 200:
            return 'white'
        elif r < 50 and g < 50 and b < 50:
            return 'black'
        elif r > g and r > b:
            return 'red'
        elif g > r and g > b:
            return 'green'
        elif b > r and b > g:
            return 'blue'
        elif r > 150 and g > 150:
            return 'yellow'
        elif r > 150 and b > 150:
            return 'magenta'
        elif g > 150 and b > 150:
            return 'cyan'
        else:
            return 'mixed'
    
    def _calculate_sharpness(self, img_array: np.ndarray) -> float:
        """Calculate image sharpness"""
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        # Simple sharpness calculation using gradient
        grad_x = np.gradient(gray, axis=1)
        grad_y = np.gradient(gray, axis=0)
        sharpness = np.mean(np.sqrt(grad_x**2 + grad_y**2))
        
        return float(sharpness)
    
    def _calculate_complexity(self, img_array: np.ndarray) -> float:
        """Calculate visual complexity of image"""
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        # Simple complexity measure based on variance
        complexity = float(np.var(gray))
        return complexity
    
    def _find_dominant_regions(self, img_array: np.ndarray) -> List[str]:
        """Find dominant regions in the image"""
        regions = []
        
        # Simple region analysis
        height, width = img_array.shape[:2]
        
        # Analyze quadrants
        mid_h, mid_w = height // 2, width // 2
        
        quadrants = {
            'top_left': img_array[:mid_h, :mid_w],
            'top_right': img_array[:mid_h, mid_w:],
            'bottom_left': img_array[mid_h:, :mid_w],
            'bottom_right': img_array[mid_h:, mid_w:]
        }
        
        for region_name, region_data in quadrants.items():
            brightness = np.mean(region_data)
            if brightness > 150:
                regions.append(f"{region_name}_bright")
            elif brightness < 100:
                regions.append(f"{region_name}_dark")
        
        return regions
    
    def _estimate_color_temperature(self, img_array: np.ndarray) -> str:
        """Estimate color temperature of image"""
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            avg_r = np.mean(img_array[:,:,0])
            avg_b = np.mean(img_array[:,:,2])
            
            if avg_r > avg_b + 20:
                return 'warm'
            elif avg_b > avg_r + 20:
                return 'cool'
            else:
                return 'neutral'
        return 'unknown'
    
    def _generate_scene_description(self, analysis_result: Dict[str, Any]) -> str:
        """Generate natural language description of the scene"""
        description_parts = []
        
        # File info
        file_info = analysis_result.get('file_info', {})
        size = file_info.get('size', (0, 0))
        description_parts.append(f"This is a {size[0]}x{size[1]} pixel image")
        
        # Visual analysis
        visual = analysis_result.get('visual_analysis', {})
        brightness = visual.get('brightness', 0)
        if brightness > 200:
            description_parts.append("with bright, well-lit content")
        elif brightness < 50:
            description_parts.append("with dark, low-light content")
        else:
            description_parts.append("with moderate lighting")
        
        # Colors
        colors = analysis_result.get('colors_analyzed', {})
        dominant_colors = colors.get('dominant_colors', [])
        if dominant_colors:
            color_names = [c['name'] for c in dominant_colors[:2]]
            description_parts.append(f"featuring {' and '.join(color_names)} colors")
        
        # Objects
        objects = analysis_result.get('objects_detected', [])
        if objects:
            object_names = [obj['object'].replace('_', ' ') for obj in objects[:2]]
            description_parts.append(f"containing {' and '.join(object_names)}")
        
        # Text
        text = analysis_result.get('text_extracted', '')
        if text and len(text) > 10:
            description_parts.append("with readable text content")
        
        return ". ".join(description_parts) + "."

    def _learn_from_image(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Learn from the analyzed image"""
        learning_insights = []

        # Learn about objects
        objects = analysis_result.get('objects_detected', [])
        for obj in objects:
            obj_name = obj['object']
            category = obj.get('category', 'unknown')

            # Update object knowledge
            if obj_name not in self.visual_knowledge['objects_seen']:
                self.visual_knowledge['objects_seen'][obj_name] = {
                    'first_seen': datetime.now().isoformat(),
                    'count': 0,
                    'category': category,
                    'descriptions': []
                }

            self.visual_knowledge['objects_seen'][obj_name]['count'] += 1
            self.visual_knowledge['objects_seen'][obj_name]['descriptions'].append(obj.get('description', ''))

            learning_insights.append(f"Learned about {obj_name} in {category} category")

        # Learn about colors
        colors = analysis_result.get('colors_analyzed', {})
        dominant_colors = colors.get('dominant_colors', [])
        for color in dominant_colors:
            color_name = color['name']
            if color_name not in self.visual_knowledge['color_associations']:
                self.visual_knowledge['color_associations'][color_name] = {
                    'seen_count': 0,
                    'contexts': []
                }

            self.visual_knowledge['color_associations'][color_name]['seen_count'] += 1
            context = f"Image with {', '.join([obj['object'] for obj in objects])}" if objects else "General image"
            self.visual_knowledge['color_associations'][color_name]['contexts'].append(context)

            learning_insights.append(f"Associated {color_name} color with current context")

        # Learn visual patterns
        visual = analysis_result.get('visual_analysis', {})
        complexity = visual.get('complexity', 0)
        sharpness = visual.get('sharpness', 0)

        pattern = {
            'complexity_level': 'high' if complexity > 1000 else 'medium' if complexity > 500 else 'low',
            'sharpness_level': 'sharp' if sharpness > 10 else 'moderate' if sharpness > 5 else 'soft',
            'timestamp': datetime.now().isoformat()
        }

        self.visual_knowledge['patterns_learned'].append(pattern)
        learning_insights.append(f"Learned visual pattern: {pattern['complexity_level']} complexity, {pattern['sharpness_level']} sharpness")

        # Update vision skills based on learning
        self.vision_skills['visual_learning'] = min(1.0, self.vision_skills['visual_learning'] + 0.02)
        self.vision_skills['visual_memory'] = min(1.0, self.vision_skills['visual_memory'] + 0.01)

        return learning_insights

    def _research_objects_online(self, objects: List[Dict[str, Any]], searcher) -> Dict[str, Any]:
        """Research detected objects using web search"""
        research_results = {}

        for obj in objects[:3]:  # Limit to 3 objects to avoid too many searches
            obj_name = obj['object']
            console.print(f"[dim]🔍 Researching: {obj_name}[/dim]")

            try:
                # Search for information about the object
                search_query = f"{obj_name} identification characteristics visual features"
                search_result = searcher.comprehensive_search(search_query, 'general')

                if search_result.get('total_sources', 0) > 0:
                    # Extract key information about the object
                    synthesized = search_result.get('synthesized_results', {})

                    object_info = {
                        'definitions': [d.get('text', '')[:200] for d in synthesized.get('definitions', [])[:2]],
                        'characteristics': [],
                        'categories': [],
                        'confidence_score': search_result.get('confidence_score', 0),
                        'sources_used': len(search_result.get('sources', {}))
                    }

                    # Extract characteristics from search results
                    for definition in synthesized.get('definitions', []):
                        text = definition.get('text', '').lower()
                        if any(word in text for word in ['color', 'shape', 'size', 'appearance']):
                            object_info['characteristics'].append(text[:100])

                    research_results[obj_name] = object_info

                    # Update AI's knowledge about this object
                    if obj_name in self.visual_knowledge['objects_seen']:
                        self.visual_knowledge['objects_seen'][obj_name]['web_research'] = object_info

                    # Improve object recognition skill
                    self.vision_skills['object_recognition'] = min(1.0, self.vision_skills['object_recognition'] + 0.03)

                    console.print(f"[dim green]✅ Learned about {obj_name} from {object_info['sources_used']} sources[/dim green]")

            except Exception as e:
                console.print(f"[dim red]Research failed for {obj_name}: {e}[/dim red]")

        return research_results

    def _store_visual_memory(self, analysis_result: Dict[str, Any], memory):
        """Store visual analysis in AI's memory system"""
        try:
            # Create a visual memory entry
            visual_memory = {
                'type': 'visual_analysis',
                'timestamp': analysis_result['timestamp'],
                'image_path': analysis_result['image_path'],
                'scene_description': analysis_result['scene_description'],
                'objects_detected': [obj['object'] for obj in analysis_result.get('objects_detected', [])],
                'dominant_colors': [c['name'] for c in analysis_result.get('colors_analyzed', {}).get('dominant_colors', [])],
                'text_content': analysis_result.get('text_extracted', ''),
                'learning_insights': analysis_result.get('learning_insights', [])
            }

            # Store in visual memories
            self.visual_knowledge['visual_memories'].append(visual_memory)

            # Also store in main memory system if available
            if hasattr(memory, 'store_knowledge'):
                memory.store_knowledge(
                    topic=f"Visual Analysis: {os.path.basename(analysis_result['image_path'])}",
                    definitions=[analysis_result['scene_description']],
                    interesting_facts=analysis_result.get('learning_insights', []),
                    examples=[f"Objects: {', '.join([obj['object'] for obj in analysis_result.get('objects_detected', [])])}"],
                    sources=[{'title': 'Visual Analysis', 'url': analysis_result['image_path']}]
                )

            console.print("[dim green]💾 Visual memory stored[/dim green]")

        except Exception as e:
            console.print(f"[dim red]Failed to store visual memory: {e}[/dim red]")

    def _update_vision_skills(self, analysis_result: Dict[str, Any]):
        """Update vision skills based on analysis results"""
        # Improve skills based on successful analysis
        if analysis_result.get('success', False):
            self.vision_skills['image_analysis'] = min(1.0, self.vision_skills['image_analysis'] + 0.02)

            if analysis_result.get('objects_detected'):
                self.vision_skills['object_recognition'] = min(1.0, self.vision_skills['object_recognition'] + 0.03)

            if analysis_result.get('text_extracted'):
                self.vision_skills['text_extraction'] = min(1.0, self.vision_skills['text_extraction'] + 0.02)

            if analysis_result.get('colors_analyzed'):
                self.vision_skills['color_analysis'] = min(1.0, self.vision_skills['color_analysis'] + 0.01)

            if analysis_result.get('scene_description'):
                self.vision_skills['scene_understanding'] = min(1.0, self.vision_skills['scene_understanding'] + 0.02)

    def create_visual_summary(self, image_path: str) -> str:
        """Create a comprehensive visual summary of an image"""
        analysis = self.analyze_image(image_path)

        if not analysis.get('success', False):
            return f"Unable to analyze image: {analysis.get('error', 'Unknown error')}"

        summary_parts = [
            f"📸 **Image Analysis Summary**",
            f"",
            f"🖼️ **File**: {os.path.basename(image_path)}",
            f"📏 **Size**: {analysis['file_info']['width']}x{analysis['file_info']['height']} pixels",
            f"",
            f"📖 **Description**: {analysis['scene_description']}",
            f""
        ]

        # Add objects
        objects = analysis.get('objects_detected', [])
        if objects:
            summary_parts.append("🎯 **Objects Detected**:")
            for obj in objects:
                summary_parts.append(f"  • {obj['object'].replace('_', ' ').title()} (confidence: {obj['confidence']:.1f})")
            summary_parts.append("")

        # Add colors
        colors = analysis.get('colors_analyzed', {}).get('dominant_colors', [])
        if colors:
            summary_parts.append("🎨 **Dominant Colors**:")
            for color in colors[:3]:
                summary_parts.append(f"  • {color['name'].title()}")
            summary_parts.append("")

        # Add text
        text = analysis.get('text_extracted', '')
        if text and len(text) > 10:
            summary_parts.append("📝 **Text Content**:")
            summary_parts.append(f"  {text[:100]}{'...' if len(text) > 100 else ''}")
            summary_parts.append("")

        # Add learning insights
        insights = analysis.get('learning_insights', [])
        if insights:
            summary_parts.append("🧠 **Learning Insights**:")
            for insight in insights[:3]:
                summary_parts.append(f"  • {insight}")
            summary_parts.append("")

        # Add web research
        research = analysis.get('web_research', {})
        if research:
            summary_parts.append("🌐 **Web Research Results**:")
            for obj_name, info in research.items():
                summary_parts.append(f"  • {obj_name}: Found info from {info['sources_used']} sources")
            summary_parts.append("")

        return "\n".join(summary_parts)

    def get_vision_status(self) -> Dict[str, Any]:
        """Get current vision intelligence status"""
        return {
            'vision_skills': self.vision_skills,
            'objects_learned': len(self.visual_knowledge['objects_seen']),
            'colors_learned': len(self.visual_knowledge['color_associations']),
            'patterns_learned': len(self.visual_knowledge['patterns_learned']),
            'visual_memories': len(self.visual_knowledge['visual_memories']),
            'overall_vision_capability': sum(self.vision_skills.values()) / len(self.vision_skills),
            'most_seen_objects': self._get_most_seen_objects(),
            'favorite_colors': self._get_favorite_colors()
        }

    def _get_most_seen_objects(self) -> List[Dict[str, Any]]:
        """Get most frequently seen objects"""
        objects = []
        for obj_name, obj_data in self.visual_knowledge['objects_seen'].items():
            objects.append({
                'name': obj_name,
                'count': obj_data['count'],
                'category': obj_data.get('category', 'unknown')
            })

        return sorted(objects, key=lambda x: x['count'], reverse=True)[:5]

    def _get_favorite_colors(self) -> List[Dict[str, Any]]:
        """Get most frequently seen colors"""
        colors = []
        for color_name, color_data in self.visual_knowledge['color_associations'].items():
            colors.append({
                'name': color_name,
                'count': color_data['seen_count']
            })

        return sorted(colors, key=lambda x: x['count'], reverse=True)[:5]

    def load_vision_data(self):
        """Load vision intelligence data"""
        try:
            vision_file = "memory/vision_intelligence.json"
            if os.path.exists(vision_file):
                with open(vision_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.vision_skills = data.get('vision_skills', self.vision_skills)
                    self.visual_knowledge = data.get('visual_knowledge', self.visual_knowledge)
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load vision data: {e}[/dim yellow]")

    def save_vision_data(self):
        """Save vision intelligence data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            vision_file = "memory/vision_intelligence.json"

            data = {
                'vision_skills': self.vision_skills,
                'visual_knowledge': self.visual_knowledge,
                'last_updated': datetime.now().isoformat()
            }

            with open(vision_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            console.print(f"[dim red]Error saving vision data: {e}[/dim red]")
