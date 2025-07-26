#!/usr/bin/env python3
"""
Start your AI's programming learning journey
"""

import sys
import os
from rich.console import Console

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

def main():
    """Start programming learning"""
    console.print("[bold blue]🚀 Starting AI Programming Learning[/bold blue]")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI...[/yellow]")
        ai = PersonalityAI()
        
        console.print("[green]✅ AI initialized![/green]")
        console.print("\n[cyan]Starting programming curriculum...[/cyan]")
        
        # Start programming learning
        ai._start_programming_learning()
        
        console.print("\n[bold green]🎉 Programming learning session complete![/bold green]")
        console.print("\n[cyan]To continue learning, run this script again or use:[/cyan]")
        console.print("[yellow]python main_ai.py interactive[/yellow]")
        console.print("[yellow]Then type: learn_coding[/yellow]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
