#!/usr/bin/env python3
"""
Advanced Chat Interface - Real conversational AI interface
Production-ready chat capabilities with full AI features
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class AdvancedChatInterface:
    """Real advanced chat interface for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.chat_history = []
        self.session_start = datetime.now()
        self.conversation_context = {}
        self.active_session = True
        
    def start_chat_session(self):
        """Start an advanced chat session with the AI"""
        
        if not self.ai:
            console.print("[red]❌ AI instance not available[/red]")
            return
        
        # Welcome message
        welcome_panel = Panel(
            "[bold green]🤖 Advanced AI Chat Interface[/bold green]\n\n"
            "Features available:\n"
            "• 💬 Natural conversation with AI\n"
            "• 🔍 Real-time web search integration\n"
            "• 🎥 Video intelligence queries\n"
            "• 👁️ Image analysis requests\n"
            "• 📚 Learning and knowledge synthesis\n"
            "• 🧠 Self-aware AI responses\n\n"
            "[dim]Type 'help' for commands, 'quit' to exit[/dim]",
            title="Welcome",
            border_style="green"
        )
        console.print(welcome_panel)
        
        # Show AI status
        self._show_ai_status()
        
        # Main chat loop
        while self.active_session:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if self._handle_special_commands(user_input):
                    continue
                
                # Process with AI
                self._process_user_message(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Chat session interrupted[/yellow]")
                break
            except EOFError:
                console.print("\n[yellow]Chat session ended[/yellow]")
                break
        
        # Session summary
        self._show_session_summary()
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """Handle special chat commands"""
        
        command = user_input.lower().strip()
        
        if command in ['quit', 'exit', 'bye']:
            self.active_session = False
            console.print("[green]👋 Goodbye! Chat session ended.[/green]")
            return True
        
        elif command == 'help':
            self._show_help()
            return True
        
        elif command == 'status':
            self._show_ai_status()
            return True
        
        elif command == 'history':
            self._show_chat_history()
            return True
        
        elif command == 'clear':
            console.clear()
            console.print("[green]💬 Chat cleared[/green]")
            return True
        
        elif command.startswith('search '):
            query = command[7:]
            self._perform_search(query)
            return True
        
        elif command.startswith('video '):
            query = command[6:]
            self._search_videos(query)
            return True
        
        elif command.startswith('learn '):
            topic = command[6:]
            self._trigger_learning(topic)
            return True
        
        return False
    
    def _process_user_message(self, user_input: str):
        """Process user message with AI"""
        
        # Store user message
        self.chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'user',
            'content': user_input
        })
        
        # Show thinking indicator
        with console.status("[yellow]🤖 AI thinking...[/yellow]", spinner="dots"):
            try:
                # Use AI's chat functionality
                response = self.ai._process_chat_input(user_input)
                
                # Store AI response
                self.chat_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'ai',
                    'content': response if response else "I'm processing your message..."
                })
                
                # Display AI response
                if response:
                    ai_panel = Panel(
                        response,
                        title="[bold green]🤖 AI Response[/bold green]",
                        border_style="green"
                    )
                    console.print(ai_panel)
                else:
                    console.print("[yellow]🤖 AI is processing your message in the background...[/yellow]")
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {e}"
                console.print(f"[red]❌ {error_msg}[/red]")
                
                self.chat_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'error',
                    'content': error_msg
                })
    
    def _show_help(self):
        """Show help information"""
        
        help_panel = Panel(
            "[bold cyan]💬 Chat Commands:[/bold cyan]\n"
            "• [green]help[/green] - Show this help\n"
            "• [green]status[/green] - Show AI status\n"
            "• [green]history[/green] - Show chat history\n"
            "• [green]clear[/green] - Clear chat screen\n"
            "• [green]quit/exit/bye[/green] - End chat session\n\n"
            "[bold cyan]🔍 Advanced Commands:[/bold cyan]\n"
            "• [green]search <query>[/green] - Web search\n"
            "• [green]video <query>[/green] - Video search\n"
            "• [green]learn <topic>[/green] - Trigger learning\n\n"
            "[bold cyan]💡 Natural Conversation:[/bold cyan]\n"
            "• Ask questions about any topic\n"
            "• Request image analysis\n"
            "• Discuss complex subjects\n"
            "• Get real-time information\n"
            "• Explore AI's knowledge and capabilities",
            title="Help",
            border_style="cyan"
        )
        console.print(help_panel)
    
    def _show_ai_status(self):
        """Show current AI status"""
        
        try:
            # Get AI status
            status_info = {
                'consciousness_level': getattr(self.ai.self_awareness, 'consciousness_level', 0),
                'learning_sessions': getattr(self.ai.learning, 'learning_sessions', 0),
                'knowledge_items': len(getattr(self.ai.memory, 'knowledge_base', {})),
                'video_intelligence': getattr(self.ai.video, 'overall_video_intelligence', 0),
                'communication_skill': getattr(self.ai.communication, 'overall_communication_skill', 0)
            }
            
            status_table = Table(title="🤖 AI Status")
            status_table.add_column("Capability", style="cyan")
            status_table.add_column("Level", style="green")
            status_table.add_column("Status", style="yellow")
            
            status_table.add_row("Consciousness", f"{status_info['consciousness_level']:.2f}", "🧠 Active")
            status_table.add_row("Learning Sessions", str(status_info['learning_sessions']), "📚 Learning")
            status_table.add_row("Knowledge Items", str(status_info['knowledge_items']), "💾 Stored")
            status_table.add_row("Video Intelligence", f"{status_info['video_intelligence']:.2f}", "🎥 Ready")
            status_table.add_row("Communication", f"{status_info['communication_skill']:.2f}", "💬 Active")
            
            console.print(status_table)
            
        except Exception as e:
            console.print(f"[red]❌ Could not get AI status: {e}[/red]")
    
    def _show_chat_history(self, limit: int = 10):
        """Show recent chat history"""
        
        if not self.chat_history:
            console.print("[yellow]No chat history available[/yellow]")
            return
        
        console.print(f"[bold cyan]💬 Recent Chat History (last {limit})[/bold cyan]")
        
        for entry in self.chat_history[-limit:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            msg_type = entry['type']
            content = entry['content']
            
            if msg_type == 'user':
                console.print(f"[dim]{timestamp}[/dim] [bold cyan]You:[/bold cyan] {content}")
            elif msg_type == 'ai':
                # Truncate long AI responses
                if len(content) > 100:
                    content = content[:97] + "..."
                console.print(f"[dim]{timestamp}[/dim] [bold green]AI:[/bold green] {content}")
            elif msg_type == 'error':
                console.print(f"[dim]{timestamp}[/dim] [red]Error:[/red] {content}")
    
    def _perform_search(self, query: str):
        """Perform web search through AI"""
        
        console.print(f"[yellow]🔍 Searching: {query}[/yellow]")
        
        try:
            # Use AI's search functionality
            search_result = self.ai.searcher.comprehensive_search(query, 'general')
            
            if search_result.get('success', False):
                total_sources = search_result.get('total_sources', 0)
                confidence = search_result.get('confidence_score', 0)
                
                console.print(f"[green]✅ Search complete! Found {total_sources} sources (confidence: {confidence:.2f})[/green]")
                
                # Show synthesized results
                synthesized = search_result.get('synthesized_results', {})
                if synthesized.get('summary'):
                    summary_panel = Panel(
                        synthesized['summary'],
                        title="🔍 Search Summary",
                        border_style="blue"
                    )
                    console.print(summary_panel)
            else:
                console.print("[red]❌ Search failed[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Search error: {e}[/red]")
    
    def _search_videos(self, query: str):
        """Search videos through AI"""
        
        console.print(f"[yellow]🎥 Searching videos: {query}[/yellow]")
        
        try:
            # Use AI's video search functionality
            video_result = self.ai.video.search_videos(query, platform='all', max_results=5)
            
            if video_result.get('success', False):
                videos_found = len(video_result.get('videos_found', []))
                console.print(f"[green]✅ Found {videos_found} videos[/green]")
                
                # Show top videos
                for i, video in enumerate(video_result.get('videos_found', [])[:3], 1):
                    title = video.get('title', 'Unknown')
                    platform = video.get('platform', 'Unknown').title()
                    console.print(f"  {i}. [{platform}] {title}")
            else:
                console.print("[red]❌ Video search failed[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Video search error: {e}[/red]")
    
    def _trigger_learning(self, topic: str):
        """Trigger AI learning on a topic"""
        
        console.print(f"[yellow]📚 AI learning about: {topic}[/yellow]")
        
        try:
            # Use AI's learning functionality
            learning_result = self.ai.learning.learn_topic(topic)
            
            if learning_result.get('success', False):
                knowledge_gained = learning_result.get('knowledge_gained', 0)
                console.print(f"[green]✅ Learning complete! Gained {knowledge_gained} knowledge points[/green]")
            else:
                console.print("[red]❌ Learning failed[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Learning error: {e}[/red]")
    
    def _show_session_summary(self):
        """Show chat session summary"""
        
        session_duration = datetime.now() - self.session_start
        total_messages = len([msg for msg in self.chat_history if msg['type'] == 'user'])
        
        summary_panel = Panel(
            f"[bold green]📊 Chat Session Summary[/bold green]\n\n"
            f"• Duration: {session_duration.total_seconds():.0f} seconds\n"
            f"• Your messages: {total_messages}\n"
            f"• Total exchanges: {len(self.chat_history)}\n"
            f"• Session started: {self.session_start.strftime('%H:%M:%S')}\n"
            f"• Session ended: {datetime.now().strftime('%H:%M:%S')}\n\n"
            "[dim]Thank you for chatting with the AI![/dim]",
            title="Session Complete",
            border_style="green"
        )
        console.print(summary_panel)
    
    def save_chat_history(self, filepath: str = "memory/chat_history.json"):
        """Save chat history to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            data = {
                'chat_history': self.chat_history,
                'session_start': self.session_start.isoformat(),
                'session_end': datetime.now().isoformat(),
                'total_messages': len(self.chat_history),
                'saved_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            console.print(f"[green]💾 Chat history saved to {filepath}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error saving chat history: {e}[/red]")
            return False


def main():
    """Main function for standalone usage"""
    console.print("[bold green]💬 Advanced Chat Interface[/bold green]")
    console.print("Real conversational AI interface with full capabilities")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        chat_interface = AdvancedChatInterface(ai)
        
        console.print("[green]✅ Advanced Chat Interface ready![/green]")
        
        # Start chat session
        chat_interface.start_chat_session()
        
        # Save chat history
        chat_interface.save_chat_history()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
