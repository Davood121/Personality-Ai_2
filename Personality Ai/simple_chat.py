#!/usr/bin/env python3
"""
Simple, reliable chat interface for Personality AI
"""

import sys
import os
from rich.console import Console

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

def main():
    """Simple chat with AI"""
    console.print("[bold blue]🤖 Personality AI - Simple Chat[/bold blue]")
    console.print("[dim]Type 'quit' to exit, 'mood' to check AI status[/dim]")
    console.print()
    
    # Import and initialize AI
    try:
        from main_ai import PersonalityAI
        console.print("[yellow]Initializing AI...[/yellow]")
        ai = PersonalityAI()
        console.print("[green]✅ AI ready![/green]")
    except Exception as e:
        console.print(f"[red]❌ Error initializing AI: {e}[/red]")
        console.print("[yellow]Make sure you're in the correct directory and dependencies are installed.[/yellow]")
        return
    
    # Show AI greeting
    try:
        greeting = ai._generate_personality_greeting()
        console.print(f"\n🤖 {greeting}")
    except:
        console.print("\n🤖 Hello! I'm your Personality AI. What would you like to talk about?")
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                console.print("\n🤖 Thanks for the great conversation! Goodbye! 👋")
                break
            
            elif user_input.lower() == 'mood':
                try:
                    ai._show_current_mood()
                except:
                    console.print("🤖 I'm feeling curious and ready to learn!")
                continue
            
            elif user_input.lower() == 'help':
                console.print("\n[cyan]Commands:[/cyan]")
                console.print("• Just type naturally to chat")
                console.print("• 'mood' - Check my current state")
                console.print("• 'quit' - End conversation")
                continue
            
            elif not user_input:
                console.print("🤖 I'm here and listening! What's on your mind?")
                continue
            
            # Generate AI response
            console.print("\n🤖 ", end="")
            try:
                ai._answer_user_question(user_input)
            except Exception as e:
                # Fallback response if main function fails
                console.print(f"That's an interesting question about '{user_input}'! Let me think about that...")
                console.print(f"🤔 From my perspective as an AI learning about personality and consciousness,")
                console.print(f"I find this topic fascinating. What aspects of '{user_input}' interest you most?")
                
        except KeyboardInterrupt:
            console.print("\n\n🤖 Chat interrupted. Goodbye! 👋")
            break
        except EOFError:
            console.print("\n\n🤖 Input ended. Goodbye! 👋")
            break
        except Exception as e:
            console.print(f"\n🤖 I had a small hiccup: {e}")
            console.print("🤖 But I'm still here! What else would you like to discuss?")

if __name__ == "__main__":
    main()
