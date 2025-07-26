"""
Simple AI Training Director
Monitors AI and automatically guides it to related topics
"""
import json
import time
import os
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class SimpleAIDirector:
    def __init__(self):
        self.topic_categories = {
            'personality_basics': [
                'personality traits', 'personality development', 'personality psychology',
                'individual differences', 'personality theories'
            ],
            'emotional_intelligence': [
                'emotional intelligence', 'empathy development', 'emotional regulation',
                'social awareness', 'emotional skills'
            ],
            'cognitive_abilities': [
                'cognitive psychology', 'critical thinking', 'problem solving',
                'creativity and innovation', 'memory and learning'
            ],
            'self_awareness': [
                'self-awareness psychology', 'metacognition', 'self-reflection',
                'consciousness studies', 'mindfulness'
            ],
            'social_psychology': [
                'social behavior', 'interpersonal relationships', 'communication skills',
                'social influence', 'group dynamics'
            ],
            'behavioral_psychology': [
                'human behavior', 'behavioral patterns', 'motivation psychology',
                'habit formation', 'behavioral change'
            ]
        }
        
        self.progression_path = [
            'personality_basics',
            'emotional_intelligence', 
            'cognitive_abilities',
            'self_awareness',
            'social_psychology',
            'behavioral_psychology'
        ]
        
        self.current_category_index = 0
        self.topics_completed = 0
        self.session_count = 0
        
    def start_intelligent_training(self, cycles_per_topic: int = 2):
        """Start intelligent training with automatic topic progression"""
        console.print(Panel.fit("🎯 Simple AI Training Director", style="bold green"))
        console.print("[cyan]Automatic topic progression and monitoring enabled[/cyan]")
        console.print(f"[yellow]Running {cycles_per_topic} cycles per topic[/yellow]")
        console.print()
        
        try:
            while True:
                # Step 1: Analyze current AI state
                ai_state = self._analyze_ai_state()
                console.print(f"[blue]📊 AI State: {ai_state['summary']}[/blue]")
                
                # Step 2: Select next topic
                next_topic = self._select_next_topic()
                console.print(f"[green]🎯 Selected topic: {next_topic}[/green]")
                
                # Step 3: Run AI on topic
                self._run_ai_on_topic(next_topic, cycles_per_topic)
                
                # Step 4: Brief analysis
                self._analyze_results(next_topic)
                
                # Step 5: Progress to next topic/category
                self._progress_topics()
                
                # Step 6: Show status
                self._show_status()
                
                # Step 7: Brief pause
                console.print("[dim]Pausing before next topic...[/dim]")
                time.sleep(10)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]🛑 Training director stopped by user[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            
    def _analyze_ai_state(self) -> dict:
        """Analyze current AI state"""
        state = {
            'consciousness_level': 1.0,
            'knowledge_count': 0,
            'recent_topics': [],
            'summary': 'Analyzing...'
        }

        try:
            # Check knowledge base (with better error handling)
            if os.path.exists("memory/knowledge_base.json"):
                try:
                    # Get file size first
                    file_size = os.path.getsize("memory/knowledge_base.json")

                    if file_size > 50 * 1024 * 1024:  # If file is larger than 50MB
                        console.print("[yellow]Knowledge base is very large, using quick analysis...[/yellow]")
                        # Quick analysis without loading full file
                        state['knowledge_count'] = self._quick_count_knowledge_entries()
                        state['recent_topics'] = ['continuing_learning']
                    else:
                        # Normal analysis
                        with open("memory/knowledge_base.json", 'r', encoding='utf-8', errors='ignore') as f:
                            knowledge = json.load(f)
                            state['knowledge_count'] = len(knowledge)

                            # Get recent topics
                            recent_topics = []
                            for entry in list(knowledge.values())[-3:]:
                                topic = entry.get('topic', 'unknown')
                                if topic not in recent_topics:
                                    recent_topics.append(topic)
                            state['recent_topics'] = recent_topics

                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    console.print(f"[yellow]Large file detected, using fallback analysis[/yellow]")
                    state['knowledge_count'] = self._quick_count_knowledge_entries()
                    state['recent_topics'] = ['continuing_learning']

            # Check consciousness
            if os.path.exists("memory/self_awareness.json"):
                try:
                    with open("memory/self_awareness.json", 'r', encoding='utf-8', errors='ignore') as f:
                        awareness = json.load(f)
                        state['consciousness_level'] = awareness.get('consciousness_level', 1.0)
                except Exception:
                    state['consciousness_level'] = 1.0  # Default

            state['summary'] = f"Knowledge: {state['knowledge_count']}, Consciousness: {state['consciousness_level']:.2f}"

        except Exception as e:
            console.print(f"[yellow]Using fallback analysis due to: {str(e)[:100]}...[/yellow]")
            state['summary'] = "AI is learning (analysis limited due to large data)"

        return state

    def _quick_count_knowledge_entries(self) -> int:
        """Quick count of knowledge entries without loading full file"""
        try:
            with open("memory/knowledge_base.json", 'r', encoding='utf-8', errors='ignore') as f:
                # Read first few lines to estimate
                content = f.read(10000)  # Read first 10KB
                # Count opening braces as rough estimate
                brace_count = content.count('"id":')
                # Estimate total based on file size
                file_size = os.path.getsize("memory/knowledge_base.json")
                estimated_total = int((brace_count / 10000) * file_size)
                return max(100, estimated_total)  # At least 100
        except Exception:
            return 100  # Fallback estimate
        
    def _select_next_topic(self) -> str:
        """Select next topic based on progression"""
        current_category = self.progression_path[self.current_category_index]
        available_topics = self.topic_categories[current_category]
        
        # Select topic (could be random or sequential)
        selected_topic = random.choice(available_topics)
        
        return selected_topic
        
    def _run_ai_on_topic(self, topic: str, cycles: int):
        """Run AI on specific topic"""
        console.print(f"[cyan]🚀 Running {cycles} cycles on: {topic}[/cyan]")
        
        try:
            # Import AI and run focused learning
            from main_ai import PersonalityAI
            
            ai = PersonalityAI()
            
            for cycle in range(cycles):
                console.print(f"[blue]  Cycle {cycle + 1}/{cycles}[/blue]")
                ai._single_learning_cycle_focused(topic)
                
                # Brief pause between cycles
                if cycle < cycles - 1:
                    time.sleep(3)
                    
            console.print(f"[green]✅ Completed {cycles} cycles on {topic}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error running AI: {e}[/red]")
            # Fallback: run regular AI
            console.print("[yellow]Trying fallback method...[/yellow]")
            os.system(f"python main_ai.py {cycles}")
            
    def _analyze_results(self, topic: str):
        """Analyze results of learning session"""
        try:
            # Simple analysis - check if knowledge increased
            if os.path.exists("memory/knowledge_base.json"):
                file_size = os.path.getsize("memory/knowledge_base.json")

                if file_size > 50 * 1024 * 1024:  # Large file
                    console.print(f"[yellow]📈 Knowledge base is very large ({file_size // (1024*1024)}MB)[/yellow]")
                    console.print(f"[green]✅ Continuing to learn about {topic}[/green]")
                else:
                    try:
                        with open("memory/knowledge_base.json", 'r', encoding='utf-8', errors='ignore') as f:
                            knowledge = json.load(f)
                            knowledge_count = len(knowledge)

                        console.print(f"[yellow]📈 Knowledge entries: {knowledge_count}[/yellow]")

                        # Check if topic appears in recent knowledge
                        recent_entries = list(knowledge.values())[-5:]
                        topic_found = any(topic.lower() in entry.get('topic', '').lower() for entry in recent_entries)

                        if topic_found:
                            console.print(f"[green]✅ Successfully learned about {topic}[/green]")
                        else:
                            console.print(f"[yellow]⚠️ Topic {topic} may need more focus[/yellow]")
                    except Exception:
                        console.print(f"[green]✅ Learning session completed for {topic}[/green]")

        except Exception as e:
            console.print(f"[green]✅ Learning session completed for {topic}[/green]")
            
    def _progress_topics(self):
        """Progress to next topic/category"""
        self.topics_completed += 1
        self.session_count += 1
        
        # Move to next category after 3 topics
        if self.topics_completed >= 3:
            self.topics_completed = 0
            self.current_category_index = (self.current_category_index + 1) % len(self.progression_path)
            
            new_category = self.progression_path[self.current_category_index]
            console.print(f"[magenta]📚 Advanced to category: {new_category}[/magenta]")
            
    def _show_status(self):
        """Show current training status"""
        current_category = self.progression_path[self.current_category_index]
        
        table = Table(title="🎯 Training Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Session", str(self.session_count))
        table.add_row("Current Category", current_category)
        table.add_row("Topics in Category", str(self.topics_completed))
        
        console.print(table)
        console.print()


def main():
    """Main function"""
    console.print("[bold blue]🎯 Simple AI Training Director[/bold blue]")
    console.print("[green]Automatic topic progression for continuous AI learning[/green]")
    console.print()
    
    try:
        response = input("Start automatic training? (y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            console.print("[yellow]Cancelled[/yellow]")
            return
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        return
    
    console.print()
    console.print("[cyan]🚀 Starting automatic training...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    console.print()
    
    director = SimpleAIDirector()
    director.start_intelligent_training(cycles_per_topic=2)


if __name__ == "__main__":
    main()
