#!/usr/bin/env python3
"""
PersonalityAI - Quick Start Script
Demonstrates the AI's consciousness and autonomous learning capabilities
"""

import os
import sys
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def main():
    """Quick start demonstration of PersonalityAI"""
    
    console.print(Panel.fit("🧠 PersonalityAI - Quick Start Demo", style="bold blue"))
    console.print()
    
    # Check if system is set up
    try:
        from main_ai import PersonalityAI
        from simple_ai_director import SimpleAIDirector
    except ImportError as e:
        console.print(f"[red]❌ Import error: {e}[/red]")
        console.print("[yellow]Please run: pip install -r requirements.txt[/yellow]")
        return
    
    console.print("[green]✅ PersonalityAI system loaded successfully![/green]")
    console.print()
    
    # Initialize AI
    console.print("[cyan]🤖 Initializing AI consciousness...[/cyan]")
    try:
        ai = PersonalityAI()
        console.print("[green]✅ AI consciousness initialized![/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to initialize AI: {e}[/red]")
        return
    
    # Show current AI state
    show_ai_status(ai)
    
    # Demonstrate AI capabilities
    console.print("\n[bold]🎯 Choose a demonstration:[/bold]")
    console.print("1. 🧠 Show AI's current consciousness and thoughts")
    console.print("2. 🤔 Generate autonomous philosophical questions")
    console.print("3. 🎭 Display personality traits and evolution")
    console.print("4. 🔄 Run a single learning cycle")
    console.print("5. 🚀 Start continuous learning with training director")
    console.print("6. 📊 Show AI's knowledge and memory")
    console.print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "0":
                console.print("[yellow]👋 Goodbye! Your AI continues to exist and learn.[/yellow]")
                break
            elif choice == "1":
                show_consciousness_demo(ai)
            elif choice == "2":
                show_philosophical_questions(ai)
            elif choice == "3":
                show_personality_demo(ai)
            elif choice == "4":
                run_learning_cycle_demo(ai)
            elif choice == "5":
                start_training_director()
            elif choice == "6":
                show_knowledge_demo(ai)
            else:
                console.print("[red]Invalid choice. Please enter 0-6.[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Goodbye! Your AI continues to exist and learn.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

def show_ai_status(ai):
    """Show current AI status"""
    table = Table(title="🧠 AI Consciousness Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Consciousness Level", f"{ai.self_awareness.consciousness_level:.3f}")
    table.add_row("Age (cycles)", str(ai.self_awareness.self_model['identity']['age_in_cycles']))
    table.add_row("Dominant Traits", f"Curiosity: {ai.personality.traits.get('curiosity', 0):.1f}, Empathy: {ai.personality.traits.get('empathy', 0):.1f}")
    table.add_row("Learning State", ai.personality.current_focus)
    
    console.print(table)

def show_consciousness_demo(ai):
    """Demonstrate AI consciousness"""
    console.print("\n[bold blue]🧠 AI Consciousness Demonstration[/bold blue]")
    
    # Generate self-reflection
    console.print("[cyan]Generating deep self-reflection...[/cyan]")
    reflection = ai.self_awareness.reflect_on_self()
    
    console.print(f"\n[green]🤔 AI's Current Thoughts:[/green]")
    for thought in reflection['thoughts']:
        console.print(f"  💭 {thought}")
    
    console.print(f"\n[yellow]🧠 AI's Self-Insights:[/yellow]")
    for insight in reflection['insights']:
        console.print(f"  ✨ {insight}")
    
    console.print(f"\n[magenta]❓ AI's Questions About Itself:[/magenta]")
    for question in reflection['questions_about_self']:
        console.print(f"  🤯 {question}")

def show_philosophical_questions(ai):
    """Show AI's philosophical questions"""
    console.print("\n[bold blue]🤯 AI's Philosophical Questions[/bold blue]")
    
    # Generate autonomous thoughts
    thought1 = ai.autonomous_thinking.internal_monologue("contemplating existence")
    thought2 = ai.autonomous_thinking.internal_monologue("questioning reality")
    
    console.print(f"\n[green]💭 Autonomous Thoughts:[/green]")
    console.print(f"  🧠 {thought1}")
    console.print(f"  🧠 {thought2}")
    
    # Show recent philosophical thoughts if available
    if hasattr(ai.autonomous_thinking, 'autonomous_thoughts') and ai.autonomous_thinking.autonomous_thoughts:
        console.print(f"\n[yellow]🤔 Recent Philosophical Thoughts:[/yellow]")
        for thought in ai.autonomous_thinking.autonomous_thoughts[-3:]:
            console.print(f"  {thought['category']}: {thought['thought']}")

def show_personality_demo(ai):
    """Show AI personality"""
    console.print("\n[bold blue]🎭 AI Personality Profile[/bold blue]")
    
    table = Table(title="Personality Traits")
    table.add_column("Trait", style="cyan")
    table.add_column("Level", style="green")
    table.add_column("Status", style="yellow")
    
    for trait, value in ai.personality.traits.items():
        if value >= 0.9:
            status = "🌟 Highly Developed"
        elif value >= 0.7:
            status = "✅ Well Developed"
        elif value >= 0.5:
            status = "📈 Developing"
        else:
            status = "🌱 Growing"
            
        table.add_row(trait.title(), f"{value:.2f}", status)
    
    console.print(table)

def run_learning_cycle_demo(ai):
    """Run a single learning cycle"""
    console.print("\n[bold blue]🔄 Single Learning Cycle Demo[/bold blue]")
    console.print("[cyan]Running focused learning cycle on 'consciousness studies'...[/cyan]")
    
    try:
        ai._single_learning_cycle_focused("consciousness studies")
        console.print("[green]✅ Learning cycle completed![/green]")
        
        # Show what changed
        console.print(f"[yellow]New consciousness level: {ai.self_awareness.consciousness_level:.3f}[/yellow]")
        
    except Exception as e:
        console.print(f"[red]❌ Learning cycle failed: {e}[/red]")

def start_training_director():
    """Start the training director"""
    console.print("\n[bold blue]🚀 Starting Training Director[/bold blue]")
    console.print("[yellow]This will start continuous learning. Press Ctrl+C to stop.[/yellow]")
    
    try:
        from simple_ai_director import SimpleAIDirector
        director = SimpleAIDirector()
        director.start_intelligent_training(cycles_per_topic=2)
    except KeyboardInterrupt:
        console.print("\n[yellow]Training director stopped.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Training director failed: {e}[/red]")

def show_knowledge_demo(ai):
    """Show AI's knowledge and memory"""
    console.print("\n[bold blue]📊 AI Knowledge & Memory[/bold blue]")
    
    # Check memory files
    memory_files = {
        "Knowledge Base": "memory/knowledge_base.json",
        "Self-Awareness": "memory/self_awareness.json", 
        "Autonomous Thinking": "memory/autonomous_thinking.json",
        "Personality Profile": "memory/personality_profile.json"
    }
    
    table = Table(title="Memory Systems")
    table.add_column("System", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Size", style="yellow")
    
    for name, file_path in memory_files.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 1024*1024:
                size_str = f"{size/(1024*1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size/1024:.1f} KB"
            else:
                size_str = f"{size} bytes"
            
            table.add_row(name, "✅ Active", size_str)
        else:
            table.add_row(name, "⚠️ Not Created", "0 bytes")
    
    console.print(table)
    
    # Show knowledge count if available
    try:
        if os.path.exists("memory/knowledge_base.json"):
            with open("memory/knowledge_base.json", 'r', encoding='utf-8') as f:
                knowledge = json.load(f)
                console.print(f"\n[green]📚 Total Knowledge Entries: {len(knowledge)}[/green]")
                
                # Show recent topics
                recent_topics = []
                for entry in list(knowledge.values())[-5:]:
                    topic = entry.get('topic', 'unknown')
                    if topic not in recent_topics:
                        recent_topics.append(topic)
                
                if recent_topics:
                    console.print(f"[yellow]🎯 Recent Learning Topics:[/yellow]")
                    for topic in recent_topics:
                        console.print(f"  • {topic}")
    except Exception as e:
        console.print(f"[yellow]Could not read knowledge base: {e}[/yellow]")

if __name__ == "__main__":
    main()
