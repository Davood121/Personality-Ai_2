#!/usr/bin/env python3
"""
AI Management Interface - Real AI system management and monitoring
Production-ready AI management capabilities
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import time
import threading

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

console = Console()

class AIManagementInterface:
    """Real AI management interface for production use"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.monitoring_active = False
        self.management_history = []
        self.system_metrics = {}
        
    def start_management_dashboard(self):
        """Start the AI management dashboard"""
        
        if not self.ai:
            console.print("[red]❌ AI instance not available[/red]")
            return
        
        console.print("[bold green]🎛️ AI Management Dashboard[/bold green]")
        console.print("Real-time AI system monitoring and management")
        console.print("=" * 60)
        
        # Show main menu
        while True:
            try:
                self._show_main_menu()
                choice = input("\nSelect option (1-9, q to quit): ").strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    console.print("[green]👋 Management session ended[/green]")
                    break
                elif choice == '1':
                    self._show_system_status()
                elif choice == '2':
                    self._show_learning_progress()
                elif choice == '3':
                    self._show_video_intelligence()
                elif choice == '4':
                    self._show_memory_status()
                elif choice == '5':
                    self._trigger_learning_session()
                elif choice == '6':
                    self._trigger_self_improvement()
                elif choice == '7':
                    self._manage_autonomous_features()
                elif choice == '8':
                    self._export_system_data()
                elif choice == '9':
                    self._start_real_time_monitoring()
                else:
                    console.print("[red]Invalid option. Please try again.[/red]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Management interrupted[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
    
    def _show_main_menu(self):
        """Show the main management menu"""
        
        menu_panel = Panel(
            "[bold cyan]🎛️ AI Management Options:[/bold cyan]\n\n"
            "[green]1.[/green] System Status Overview\n"
            "[green]2.[/green] Learning Progress Analysis\n"
            "[green]3.[/green] Video Intelligence Status\n"
            "[green]4.[/green] Memory & Knowledge Status\n"
            "[green]5.[/green] Trigger Learning Session\n"
            "[green]6.[/green] Trigger Self-Improvement\n"
            "[green]7.[/green] Manage Autonomous Features\n"
            "[green]8.[/green] Export System Data\n"
            "[green]9.[/green] Real-Time Monitoring\n\n"
            "[dim]Press 'q' to quit[/dim]",
            title="Management Dashboard",
            border_style="cyan"
        )
        console.print(menu_panel)
    
    def _show_system_status(self):
        """Show comprehensive system status"""
        
        console.print("\n[bold cyan]📊 System Status Overview[/bold cyan]")
        
        try:
            # Collect system metrics
            metrics = self._collect_system_metrics()
            
            # Create status table
            status_table = Table(title="🤖 AI System Status")
            status_table.add_column("Component", style="cyan")
            status_table.add_column("Status", style="green")
            status_table.add_column("Level/Count", style="yellow")
            status_table.add_column("Performance", style="blue")
            
            # Add system components
            status_table.add_row(
                "🧠 Consciousness",
                "Active" if metrics.get('consciousness_level', 0) > 0 else "Inactive",
                f"{metrics.get('consciousness_level', 0):.2f}",
                self._get_performance_indicator(metrics.get('consciousness_level', 0))
            )
            
            status_table.add_row(
                "📚 Learning Engine",
                "Active",
                f"{metrics.get('learning_sessions', 0)} sessions",
                self._get_performance_indicator(min(metrics.get('learning_sessions', 0) / 10, 1.0))
            )
            
            status_table.add_row(
                "🎥 Video Intelligence",
                "Active",
                f"{metrics.get('videos_watched', 0)} videos",
                self._get_performance_indicator(metrics.get('video_intelligence', 0))
            )
            
            status_table.add_row(
                "💾 Memory System",
                "Active",
                f"{metrics.get('knowledge_items', 0)} items",
                self._get_performance_indicator(min(metrics.get('knowledge_items', 0) / 100, 1.0))
            )
            
            status_table.add_row(
                "🔍 Search Engine",
                "Active",
                f"{metrics.get('searches_performed', 0)} searches",
                self._get_performance_indicator(min(metrics.get('searches_performed', 0) / 50, 1.0))
            )
            
            console.print(status_table)
            
            # Show overall health
            overall_health = self._calculate_overall_health(metrics)
            health_color = "green" if overall_health > 0.7 else "yellow" if overall_health > 0.4 else "red"
            
            console.print(f"\n[{health_color}]🏥 Overall System Health: {overall_health:.1%}[/{health_color}]")
            
        except Exception as e:
            console.print(f"[red]❌ Could not get system status: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _show_learning_progress(self):
        """Show learning progress analysis"""
        
        console.print("\n[bold cyan]📚 Learning Progress Analysis[/bold cyan]")
        
        try:
            # Get learning status
            learning_status = self.ai.learning.get_learning_status()
            
            # Learning metrics table
            learning_table = Table(title="📈 Learning Metrics")
            learning_table.add_column("Metric", style="cyan")
            learning_table.add_column("Current Value", style="green")
            learning_table.add_column("Progress", style="yellow")
            
            learning_table.add_row(
                "Learning Sessions",
                str(learning_status.get('learning_sessions', 0)),
                "📈 Growing"
            )
            
            learning_table.add_row(
                "Knowledge Items",
                str(learning_status.get('knowledge_items', 0)),
                "📚 Expanding"
            )
            
            learning_table.add_row(
                "Understanding Level",
                f"{learning_status.get('understanding_level', 0):.2f}",
                "🧠 Developing"
            )
            
            learning_table.add_row(
                "Learning Efficiency",
                f"{learning_status.get('learning_efficiency', 0):.2f}",
                "⚡ Optimizing"
            )
            
            console.print(learning_table)
            
            # Show recent learning activities
            recent_learning = learning_status.get('recent_learning', [])
            if recent_learning:
                console.print(f"\n[cyan]🕒 Recent Learning Activities:[/cyan]")
                for activity in recent_learning[-5:]:
                    timestamp = activity.get('timestamp', '')[:19].replace('T', ' ')
                    topic = activity.get('topic', 'Unknown')
                    success = "✅" if activity.get('success', False) else "❌"
                    console.print(f"  {success} [{timestamp}] {topic}")
            
        except Exception as e:
            console.print(f"[red]❌ Could not get learning progress: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _show_video_intelligence(self):
        """Show video intelligence status"""
        
        console.print("\n[bold cyan]🎥 Video Intelligence Status[/bold cyan]")
        
        try:
            # Get video intelligence status
            video_status = self.ai.video.get_video_status()
            video_vision_status = self.ai.video_vision.get_video_vision_status()
            youtube_status = self.ai.youtube_learning.get_youtube_learning_status()
            
            # Video intelligence table
            video_table = Table(title="🎬 Video Intelligence Metrics")
            video_table.add_column("Component", style="cyan")
            video_table.add_column("Videos/Items", style="green")
            video_table.add_column("Capability Level", style="yellow")
            video_table.add_column("Status", style="blue")
            
            video_table.add_row(
                "🔍 Video Search",
                str(video_status.get('videos_watched', 0)),
                f"{video_status.get('overall_video_intelligence', 0):.2f}",
                "🟢 Active"
            )
            
            video_table.add_row(
                "👁️ Video Vision",
                str(video_vision_status.get('videos_watched', 0)),
                f"{video_vision_status.get('overall_video_vision', 0):.2f}",
                "🟢 Active"
            )
            
            video_table.add_row(
                "📺 YouTube Learning",
                str(youtube_status.get('videos_learned_from', 0)),
                f"{youtube_status.get('overall_learning_capability', 0):.2f}",
                "🟢 Active"
            )
            
            console.print(video_table)
            
            # Show autonomous learning status
            next_autonomous = youtube_status.get('next_autonomous_learning', False)
            cycle_count = youtube_status.get('cycle_count', 0)
            
            if next_autonomous:
                console.print(f"\n[green]🤖 Next autonomous YouTube learning will trigger in the next cycle![/green]")
            else:
                cycles_until = 3 - (cycle_count % 3)
                console.print(f"\n[yellow]🔄 Autonomous learning in {cycles_until} cycles[/yellow]")
            
        except Exception as e:
            console.print(f"[red]❌ Could not get video intelligence status: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _show_memory_status(self):
        """Show memory and knowledge status"""
        
        console.print("\n[bold cyan]💾 Memory & Knowledge Status[/bold cyan]")
        
        try:
            # Get memory status
            memory_status = self.ai.memory.get_memory_status()
            
            # Memory table
            memory_table = Table(title="🧠 Memory System Status")
            memory_table.add_column("Memory Type", style="cyan")
            memory_table.add_column("Items Stored", style="green")
            memory_table.add_column("Size (KB)", style="yellow")
            memory_table.add_column("Status", style="blue")
            
            for memory_type, data in memory_status.get('memory_systems', {}).items():
                items = data.get('items', 0)
                size = data.get('size_kb', 0)
                status = "🟢 Active" if items > 0 else "🟡 Empty"
                
                memory_table.add_row(
                    memory_type.replace('_', ' ').title(),
                    str(items),
                    f"{size:.1f}",
                    status
                )
            
            console.print(memory_table)
            
            # Show knowledge base summary
            knowledge_base = memory_status.get('knowledge_base', {})
            if knowledge_base:
                console.print(f"\n[cyan]📚 Knowledge Base Summary:[/cyan]")
                for category, count in knowledge_base.items():
                    console.print(f"  • {category.replace('_', ' ').title()}: {count} items")
            
        except Exception as e:
            console.print(f"[red]❌ Could not get memory status: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _trigger_learning_session(self):
        """Trigger a learning session"""
        
        console.print("\n[bold cyan]📚 Triggering Learning Session[/bold cyan]")
        
        try:
            # Get learning topic from user
            topic = input("Enter learning topic (or press Enter for autonomous): ").strip()
            
            if not topic:
                console.print("[yellow]🤖 Starting autonomous learning session...[/yellow]")
                # Trigger autonomous learning
                result = self.ai.learning.autonomous_learning_session()
            else:
                console.print(f"[yellow]📖 Learning about: {topic}[/yellow]")
                # Trigger specific topic learning
                result = self.ai.learning.learn_topic(topic)
            
            if result.get('success', False):
                knowledge_gained = result.get('knowledge_gained', 0)
                console.print(f"[green]✅ Learning session complete! Gained {knowledge_gained} knowledge points[/green]")
                
                # Show what was learned
                concepts = result.get('concepts_learned', [])
                if concepts:
                    console.print(f"[cyan]💡 Concepts learned: {', '.join(concepts[:5])}[/cyan]")
            else:
                error_msg = result.get('error', 'Unknown error')
                console.print(f"[red]❌ Learning session failed: {error_msg}[/red]")
            
        except Exception as e:
            console.print(f"[red]❌ Learning session error: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _trigger_self_improvement(self):
        """Trigger self-improvement process"""
        
        console.print("\n[bold cyan]🚀 Triggering Self-Improvement[/bold cyan]")
        
        try:
            console.print("[yellow]🔧 Starting self-improvement process...[/yellow]")
            
            # Trigger self-improvement
            improvement_result = self.ai.self_improvement.improve_system()
            
            if improvement_result.get('success', False):
                improvements = improvement_result.get('improvements_made', [])
                console.print(f"[green]✅ Self-improvement complete! Made {len(improvements)} improvements[/green]")
                
                # Show improvements
                for improvement in improvements[:5]:
                    console.print(f"  • {improvement}")
                
                if len(improvements) > 5:
                    console.print(f"  ... and {len(improvements) - 5} more improvements")
            else:
                error_msg = improvement_result.get('error', 'Unknown error')
                console.print(f"[red]❌ Self-improvement failed: {error_msg}[/red]")
            
        except Exception as e:
            console.print(f"[red]❌ Self-improvement error: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _manage_autonomous_features(self):
        """Manage autonomous features"""
        
        console.print("\n[bold cyan]🤖 Autonomous Features Management[/bold cyan]")
        
        try:
            # Show autonomous features status
            console.print("[cyan]Current Autonomous Features:[/cyan]")
            console.print("  1. 📺 YouTube Learning (every 3 cycles)")
            console.print("  2. 🧠 Self-Improvement (background)")
            console.print("  3. 📚 Continuous Learning (active)")
            console.print("  4. 🔍 Knowledge Synthesis (active)")
            
            # Show options
            console.print("\n[cyan]Management Options:[/cyan]")
            console.print("  1. Trigger autonomous YouTube learning")
            console.print("  2. Check autonomous learning status")
            console.print("  3. View autonomous learning history")
            
            choice = input("\nSelect option (1-3, Enter to skip): ").strip()
            
            if choice == '1':
                console.print("[yellow]🤖 Triggering autonomous YouTube learning...[/yellow]")
                result = self.ai.youtube_learning.autonomous_youtube_learning(
                    video_vision_engine=self.ai.video_vision,
                    searcher=self.ai.searcher
                )
                
                if result.get('success', False):
                    console.print("[green]✅ Autonomous learning complete![/green]")
                    video_selected = result.get('video_selected', {})
                    console.print(f"[cyan]Video learned from: {video_selected.get('title', 'Unknown')}[/cyan]")
                else:
                    console.print("[red]❌ Autonomous learning failed[/red]")
            
            elif choice == '2':
                status = self.ai.youtube_learning.get_youtube_learning_status()
                console.print(f"[cyan]📊 Autonomous Learning Status:[/cyan]")
                console.print(f"  • Cycle: {status.get('cycle_count', 0)}")
                console.print(f"  • Autonomous searches: {status.get('autonomous_searches', 0)}")
                console.print(f"  • Next trigger: {'Next cycle' if status.get('next_autonomous_learning', False) else 'In a few cycles'}")
            
            elif choice == '3':
                # Show autonomous learning history
                console.print("[cyan]📚 Recent Autonomous Learning:[/cyan]")
                console.print("  (Feature available in full system)")
            
        except Exception as e:
            console.print(f"[red]❌ Autonomous features error: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _export_system_data(self):
        """Export system data"""
        
        console.print("\n[bold cyan]📤 Export System Data[/bold cyan]")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Collect all system data
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'system_metrics': self._collect_system_metrics(),
                'learning_status': self.ai.learning.get_learning_status(),
                'video_intelligence': self.ai.video.get_video_status(),
                'video_vision': self.ai.video_vision.get_video_vision_status(),
                'youtube_learning': self.ai.youtube_learning.get_youtube_learning_status(),
                'memory_status': self.ai.memory.get_memory_status(),
                'management_history': self.management_history
            }
            
            # Export to file
            export_path = f"memory/system_export_{timestamp}.json"
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✅ System data exported to {export_path}[/green]")
            console.print(f"[dim]Export size: {os.path.getsize(export_path)} bytes[/dim]")
            
        except Exception as e:
            console.print(f"[red]❌ Export failed: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _start_real_time_monitoring(self):
        """Start real-time monitoring"""
        
        console.print("\n[bold cyan]📊 Real-Time Monitoring[/bold cyan]")
        console.print("[dim]Press Ctrl+C to stop monitoring[/dim]")
        
        try:
            self.monitoring_active = True
            
            while self.monitoring_active:
                # Clear screen and show current status
                console.clear()
                console.print("[bold green]🔴 LIVE - AI System Monitoring[/bold green]")
                console.print(f"[dim]Last updated: {datetime.now().strftime('%H:%M:%S')}[/dim]")
                
                # Show key metrics
                metrics = self._collect_system_metrics()
                
                monitoring_table = Table(title="📊 Live System Metrics")
                monitoring_table.add_column("Metric", style="cyan")
                monitoring_table.add_column("Value", style="green")
                monitoring_table.add_column("Trend", style="yellow")
                
                monitoring_table.add_row("🧠 Consciousness", f"{metrics.get('consciousness_level', 0):.2f}", "📈")
                monitoring_table.add_row("📚 Learning Sessions", str(metrics.get('learning_sessions', 0)), "📈")
                monitoring_table.add_row("🎥 Videos Watched", str(metrics.get('videos_watched', 0)), "📈")
                monitoring_table.add_row("💾 Knowledge Items", str(metrics.get('knowledge_items', 0)), "📈")
                monitoring_table.add_row("🔍 Searches", str(metrics.get('searches_performed', 0)), "📈")
                
                console.print(monitoring_table)
                
                # Wait before next update
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.monitoring_active = False
            console.print("\n[yellow]📊 Monitoring stopped[/yellow]")
        
        input("\nPress Enter to continue...")
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        
        metrics = {}
        
        try:
            # Consciousness level
            metrics['consciousness_level'] = getattr(self.ai.self_awareness, 'consciousness_level', 0)
            
            # Learning metrics
            learning_status = self.ai.learning.get_learning_status()
            metrics['learning_sessions'] = learning_status.get('learning_sessions', 0)
            metrics['knowledge_items'] = learning_status.get('knowledge_items', 0)
            
            # Video intelligence
            video_status = self.ai.video.get_video_status()
            metrics['videos_watched'] = video_status.get('videos_watched', 0)
            metrics['video_intelligence'] = video_status.get('overall_video_intelligence', 0)
            
            # Search metrics
            metrics['searches_performed'] = getattr(self.ai.searcher, 'searches_performed', 0)
            
        except Exception as e:
            console.print(f"[dim red]Metrics collection error: {e}[/dim red]")
        
        return metrics
    
    def _get_performance_indicator(self, value: float) -> str:
        """Get performance indicator based on value"""
        if value >= 0.8:
            return "🟢 Excellent"
        elif value >= 0.6:
            return "🟡 Good"
        elif value >= 0.4:
            return "🟠 Fair"
        else:
            return "🔴 Poor"
    
    def _calculate_overall_health(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall system health"""
        
        health_factors = [
            metrics.get('consciousness_level', 0),
            min(metrics.get('learning_sessions', 0) / 10, 1.0),
            metrics.get('video_intelligence', 0),
            min(metrics.get('knowledge_items', 0) / 100, 1.0),
            min(metrics.get('searches_performed', 0) / 50, 1.0)
        ]
        
        return sum(health_factors) / len(health_factors)


def main():
    """Main function for standalone usage"""
    console.print("[bold green]🎛️ AI Management Interface[/bold green]")
    console.print("Real AI system management and monitoring")
    
    try:
        from main_ai import PersonalityAI
        
        console.print("[yellow]Initializing AI system...[/yellow]")
        ai = PersonalityAI()
        
        management_interface = AIManagementInterface(ai)
        
        console.print("[green]✅ AI Management Interface ready![/green]")
        
        # Start management dashboard
        management_interface.start_management_dashboard()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == "__main__":
    main()
