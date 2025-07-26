#!/usr/bin/env python3
"""
Visual Memory Viewer - See everything your AI has seen and learned
"""

import sys
import os
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

def load_visual_memories():
    """Load all visual memories from the AI"""
    try:
        vision_file = "memory/vision_intelligence.json"
        if os.path.exists(vision_file):
            with open(vision_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('visual_knowledge', {})
        else:
            console.print("[yellow]⚠️ No visual memories found yet[/yellow]")
            return {}
    except Exception as e:
        console.print(f"[red]❌ Error loading visual memories: {e}[/red]")
        return {}

def show_visual_memories_overview(visual_knowledge):
    """Show overview of all visual memories"""
    console.print("[bold blue]👁️ AI Visual Memory Overview[/bold blue]")
    console.print("=" * 60)
    
    # Get statistics
    objects_seen = visual_knowledge.get('objects_seen', {})
    color_associations = visual_knowledge.get('color_associations', {})
    visual_memories = visual_knowledge.get('visual_memories', [])
    patterns_learned = visual_knowledge.get('patterns_learned', [])
    
    # Create overview table
    overview_table = Table(title="Visual Intelligence Summary")
    overview_table.add_column("Category", style="cyan")
    overview_table.add_column("Count", style="green")
    overview_table.add_column("Details", style="dim")
    
    overview_table.add_row("🎯 Objects Learned", str(len(objects_seen)), f"{len([o for o in objects_seen.values() if o.get('count', 0) > 1])} seen multiple times")
    overview_table.add_row("🎨 Colors Learned", str(len(color_associations)), f"{len([c for c in color_associations.values() if c.get('seen_count', 0) > 1])} seen multiple times")
    overview_table.add_row("🧠 Visual Memories", str(len(visual_memories)), f"Images analyzed and remembered")
    overview_table.add_row("🔍 Patterns Learned", str(len(patterns_learned)), f"Visual patterns recognized")
    
    console.print(overview_table)
    console.print()

def show_objects_seen(objects_seen):
    """Show all objects the AI has seen"""
    if not objects_seen:
        console.print("[yellow]🎯 No objects seen yet[/yellow]")
        return
    
    console.print("[bold cyan]🎯 Objects Your AI Has Seen[/bold cyan]")
    console.print("=" * 60)
    
    # Sort objects by count (most seen first)
    sorted_objects = sorted(objects_seen.items(), key=lambda x: x[1].get('count', 0), reverse=True)
    
    objects_table = Table()
    objects_table.add_column("Object", style="cyan")
    objects_table.add_column("Category", style="green")
    objects_table.add_column("Times Seen", style="yellow")
    objects_table.add_column("First Seen", style="dim")
    objects_table.add_column("Description", style="white")
    
    for obj_name, obj_data in sorted_objects:
        # Format first seen date
        first_seen = obj_data.get('first_seen', '')
        if first_seen:
            try:
                dt = datetime.fromisoformat(first_seen.replace('Z', '+00:00'))
                first_seen_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                first_seen_str = first_seen[:16]
        else:
            first_seen_str = 'Unknown'
        
        # Get latest description
        descriptions = obj_data.get('descriptions', [])
        latest_desc = descriptions[-1] if descriptions else 'No description'
        if len(latest_desc) > 50:
            latest_desc = latest_desc[:47] + '...'
        
        objects_table.add_row(
            obj_name.replace('_', ' ').title(),
            obj_data.get('category', 'unknown').title(),
            str(obj_data.get('count', 0)),
            first_seen_str,
            latest_desc
        )
    
    console.print(objects_table)
    console.print()

def show_colors_learned(color_associations):
    """Show all colors the AI has learned"""
    if not color_associations:
        console.print("[yellow]🎨 No colors learned yet[/yellow]")
        return
    
    console.print("[bold cyan]🎨 Colors Your AI Has Learned[/bold cyan]")
    console.print("=" * 60)
    
    # Sort colors by seen count
    sorted_colors = sorted(color_associations.items(), key=lambda x: x[1].get('seen_count', 0), reverse=True)
    
    colors_table = Table()
    colors_table.add_column("Color", style="cyan")
    colors_table.add_column("Times Seen", style="yellow")
    colors_table.add_column("Contexts", style="white")
    
    for color_name, color_data in sorted_colors:
        seen_count = color_data.get('seen_count', 0)
        contexts = color_data.get('contexts', [])
        
        # Show latest contexts
        context_str = ', '.join(contexts[-3:]) if contexts else 'No context'
        if len(context_str) > 60:
            context_str = context_str[:57] + '...'
        
        colors_table.add_row(
            color_name.title(),
            str(seen_count),
            context_str
        )
    
    console.print(colors_table)
    console.print()

def show_visual_memories(visual_memories):
    """Show detailed visual memories"""
    if not visual_memories:
        console.print("[yellow]🧠 No visual memories stored yet[/yellow]")
        return
    
    console.print("[bold cyan]🧠 Visual Memories (Images Analyzed)[/bold cyan]")
    console.print("=" * 60)
    
    # Sort by timestamp (most recent first)
    sorted_memories = sorted(visual_memories, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    for i, memory in enumerate(sorted_memories, 1):
        # Format timestamp
        timestamp = memory.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                time_str = timestamp[:19]
        else:
            time_str = 'Unknown time'
        
        # Create memory panel
        image_path = memory.get('image_path', 'Unknown')
        image_name = os.path.basename(image_path) if image_path != 'Unknown' else 'Unknown'
        
        memory_content = []
        memory_content.append(f"📸 **Image**: {image_name}")
        memory_content.append(f"🕒 **Analyzed**: {time_str}")
        
        # Scene description
        scene_desc = memory.get('scene_description', '')
        if scene_desc:
            memory_content.append(f"📖 **Description**: {scene_desc}")
        
        # Objects detected
        objects = memory.get('objects_detected', [])
        if objects:
            objects_str = ', '.join([obj.replace('_', ' ').title() for obj in objects])
            memory_content.append(f"🎯 **Objects**: {objects_str}")
        
        # Colors
        colors = memory.get('dominant_colors', [])
        if colors:
            colors_str = ', '.join([color.title() for color in colors])
            memory_content.append(f"🎨 **Colors**: {colors_str}")
        
        # Text content
        text_content = memory.get('text_content', '')
        if text_content and len(text_content.strip()) > 10:
            text_preview = text_content[:100] + '...' if len(text_content) > 100 else text_content
            memory_content.append(f"📝 **Text Found**: {text_preview}")
        
        # Learning insights
        insights = memory.get('learning_insights', [])
        if insights:
            insights_str = '; '.join(insights[:2])
            memory_content.append(f"🧠 **Learned**: {insights_str}")
        
        panel_content = '\n'.join(memory_content)
        panel = Panel(panel_content, title=f"Memory #{i}", border_style="blue")
        console.print(panel)
        console.print()

def show_patterns_learned(patterns_learned):
    """Show visual patterns the AI has learned"""
    if not patterns_learned:
        console.print("[yellow]🔍 No patterns learned yet[/yellow]")
        return
    
    console.print("[bold cyan]🔍 Visual Patterns Learned[/bold cyan]")
    console.print("=" * 60)
    
    # Group patterns by type
    complexity_patterns = {}
    sharpness_patterns = {}
    
    for pattern in patterns_learned:
        complexity = pattern.get('complexity_level', 'unknown')
        sharpness = pattern.get('sharpness_level', 'unknown')
        
        if complexity not in complexity_patterns:
            complexity_patterns[complexity] = 0
        complexity_patterns[complexity] += 1
        
        if sharpness not in sharpness_patterns:
            sharpness_patterns[sharpness] = 0
        sharpness_patterns[sharpness] += 1
    
    patterns_table = Table()
    patterns_table.add_column("Pattern Type", style="cyan")
    patterns_table.add_column("Variations Learned", style="green")
    patterns_table.add_column("Details", style="white")
    
    # Add complexity patterns
    for complexity, count in complexity_patterns.items():
        patterns_table.add_row(
            f"Complexity: {complexity.title()}",
            str(count),
            f"Images with {complexity} visual complexity"
        )
    
    # Add sharpness patterns
    for sharpness, count in sharpness_patterns.items():
        patterns_table.add_row(
            f"Sharpness: {sharpness.title()}",
            str(count),
            f"Images with {sharpness} sharpness level"
        )
    
    console.print(patterns_table)
    console.print()

def show_learning_timeline(visual_memories):
    """Show timeline of AI's visual learning"""
    if not visual_memories:
        console.print("[yellow]📅 No learning timeline available[/yellow]")
        return
    
    console.print("[bold cyan]📅 AI Visual Learning Timeline[/bold cyan]")
    console.print("=" * 60)
    
    # Sort by timestamp
    sorted_memories = sorted(visual_memories, key=lambda x: x.get('timestamp', ''))
    
    timeline_table = Table()
    timeline_table.add_column("Time", style="dim")
    timeline_table.add_column("Image", style="cyan")
    timeline_table.add_column("What AI Learned", style="green")
    
    for memory in sorted_memories:
        # Format timestamp
        timestamp = memory.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S')
            except:
                time_str = timestamp[11:19] if len(timestamp) > 19 else timestamp
        else:
            time_str = '??:??:??'
        
        image_name = os.path.basename(memory.get('image_path', 'Unknown'))
        
        # Summarize learning
        learning_summary = []
        objects = memory.get('objects_detected', [])
        if objects:
            learning_summary.append(f"{len(objects)} objects")
        
        colors = memory.get('dominant_colors', [])
        if colors:
            learning_summary.append(f"{len(colors)} colors")
        
        insights = memory.get('learning_insights', [])
        if insights:
            learning_summary.append(f"{len(insights)} insights")
        
        learning_str = ', '.join(learning_summary) if learning_summary else 'Basic analysis'
        
        timeline_table.add_row(time_str, image_name, learning_str)
    
    console.print(timeline_table)
    console.print()

def show_ai_vision_stats(visual_knowledge):
    """Show detailed AI vision statistics"""
    console.print("[bold cyan]📊 AI Vision Intelligence Statistics[/bold cyan]")
    console.print("=" * 60)
    
    objects_seen = visual_knowledge.get('objects_seen', {})
    color_associations = visual_knowledge.get('color_associations', {})
    visual_memories = visual_knowledge.get('visual_memories', [])
    patterns_learned = visual_knowledge.get('patterns_learned', [])
    
    # Calculate statistics
    total_objects = len(objects_seen)
    total_object_sightings = sum(obj.get('count', 0) for obj in objects_seen.values())
    total_colors = len(color_associations)
    total_color_sightings = sum(color.get('seen_count', 0) for color in color_associations.values())
    
    # Most seen object
    most_seen_obj = max(objects_seen.items(), key=lambda x: x[1].get('count', 0)) if objects_seen else None
    most_seen_color = max(color_associations.items(), key=lambda x: x[1].get('seen_count', 0)) if color_associations else None
    
    stats_table = Table()
    stats_table.add_column("Statistic", style="cyan")
    stats_table.add_column("Value", style="green")
    stats_table.add_column("Details", style="dim")
    
    stats_table.add_row("Total Images Analyzed", str(len(visual_memories)), "Images processed by AI")
    stats_table.add_row("Unique Objects Learned", str(total_objects), f"Total sightings: {total_object_sightings}")
    stats_table.add_row("Unique Colors Learned", str(total_colors), f"Total sightings: {total_color_sightings}")
    stats_table.add_row("Visual Patterns", str(len(patterns_learned)), "Complexity and sharpness patterns")
    
    if most_seen_obj:
        obj_name, obj_data = most_seen_obj
        stats_table.add_row("Most Seen Object", obj_name.replace('_', ' ').title(), f"Seen {obj_data.get('count', 0)} times")
    
    if most_seen_color:
        color_name, color_data = most_seen_color
        stats_table.add_row("Most Seen Color", color_name.title(), f"Seen {color_data.get('seen_count', 0)} times")
    
    console.print(stats_table)
    console.print()

def main():
    """Main function to show AI's visual memories"""
    console.print("[bold green]👁️ AI Visual Memory Viewer[/bold green]")
    console.print("See everything your AI has seen and learned from images!")
    console.print("=" * 60)
    
    # Load visual memories
    visual_knowledge = load_visual_memories()
    
    if not visual_knowledge:
        console.print("[yellow]📸 Your AI hasn't seen any images yet![/yellow]")
        console.print("\n[cyan]To give your AI vision:[/cyan]")
        console.print("  python main_ai.py interactive")
        console.print("  Then use: see <image_path>")
        console.print("  Or use: analyze_image <image_path>")
        return
    
    # Show overview
    show_visual_memories_overview(visual_knowledge)
    
    # Show detailed sections
    show_objects_seen(visual_knowledge.get('objects_seen', {}))
    show_colors_learned(visual_knowledge.get('color_associations', {}))
    show_visual_memories(visual_knowledge.get('visual_memories', []))
    show_patterns_learned(visual_knowledge.get('patterns_learned', []))
    show_learning_timeline(visual_knowledge.get('visual_memories', []))
    show_ai_vision_stats(visual_knowledge)
    
    console.print("[bold green]✅ Visual Memory Review Complete![/bold green]")
    console.print("\n[cyan]💡 Your AI remembers everything it sees and learns from each image![/cyan]")

if __name__ == "__main__":
    main()
