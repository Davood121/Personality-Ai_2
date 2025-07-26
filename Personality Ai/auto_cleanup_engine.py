"""
Automatic Cleanup Engine - Keeps the AI project clean automatically
"""
import os
import shutil
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from config import *

console = Console()

class AutoCleanupEngine:
    def __init__(self):
        self.cleanup_history = []
        self.background_service_running = False
        self.background_thread = None
        self.cleanup_rules = {
            'cache_files': {
                'enabled': True,
                'frequency_hours': 6,  # Clean every 6 hours
                'patterns': ['__pycache__', '*.pyc', '*.pyo', '*.pyd'],
                'last_cleanup': None
            },
            'temp_files': {
                'enabled': True,
                'frequency_hours': 12,  # Clean every 12 hours
                'patterns': ['*.tmp', '*.temp', '*~', '.DS_Store'],
                'last_cleanup': None
            },
            'log_rotation': {
                'enabled': True,
                'frequency_hours': 24,  # Clean daily
                'max_log_files': 10,
                'max_log_size_mb': 50,
                'last_cleanup': None
            },
            'duplicate_detection': {
                'enabled': True,
                'frequency_hours': 48,  # Check every 2 days
                'auto_remove': False,  # Don't auto-remove, just report
                'last_cleanup': None
            },
            'memory_optimization': {
                'enabled': True,
                'frequency_hours': 24,  # Daily memory cleanup
                'max_memory_entries': 1000,
                'compress_old_data': True,
                'last_cleanup': None
            }
        }
        
        self.load_cleanup_data()
    
    def should_run_cleanup(self, cleanup_type: str) -> bool:
        """Check if a cleanup type should run based on frequency"""
        rule = self.cleanup_rules.get(cleanup_type, {})
        if not rule.get('enabled', False):
            return False
        
        last_cleanup = rule.get('last_cleanup')
        if not last_cleanup:
            return True
        
        last_time = datetime.fromisoformat(last_cleanup)
        frequency_hours = rule.get('frequency_hours', 24)
        
        return datetime.now() - last_time >= timedelta(hours=frequency_hours)
    
    def auto_cleanup_cache_files(self) -> Dict[str, Any]:
        """Automatically clean cache files"""
        if not self.should_run_cleanup('cache_files'):
            return {'skipped': True, 'reason': 'Not due for cleanup'}
        
        console.print("[dim]🧹 Auto-cleaning cache files...[/dim]")
        
        cleaned_items = []
        
        # Remove __pycache__ directories
        for pycache_dir in Path('.').rglob('__pycache__'):
            try:
                shutil.rmtree(pycache_dir)
                cleaned_items.append(str(pycache_dir))
            except Exception as e:
                console.print(f"[dim red]Warning: Could not remove {pycache_dir}: {e}[/dim red]")
        
        # Remove .pyc files
        for pyc_file in Path('.').rglob('*.pyc'):
            try:
                pyc_file.unlink()
                cleaned_items.append(str(pyc_file))
            except Exception as e:
                console.print(f"[dim red]Warning: Could not remove {pyc_file}: {e}[/dim red]")
        
        # Update last cleanup time
        self.cleanup_rules['cache_files']['last_cleanup'] = datetime.now().isoformat()
        
        result = {
            'type': 'cache_files',
            'timestamp': datetime.now().isoformat(),
            'items_cleaned': len(cleaned_items),
            'items': cleaned_items[:10],  # Store first 10 for logging
            'success': True
        }
        
        if cleaned_items:
            console.print(f"[dim green]✅ Auto-cleaned {len(cleaned_items)} cache files[/dim green]")
        
        return result
    
    def auto_cleanup_temp_files(self) -> Dict[str, Any]:
        """Automatically clean temporary files"""
        if not self.should_run_cleanup('temp_files'):
            return {'skipped': True, 'reason': 'Not due for cleanup'}
        
        console.print("[dim]🧹 Auto-cleaning temporary files...[/dim]")
        
        cleaned_items = []
        temp_patterns = ['*.tmp', '*.temp', '*~', '.DS_Store']
        
        for pattern in temp_patterns:
            for temp_file in Path('.').rglob(pattern):
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                        cleaned_items.append(str(temp_file))
                except Exception as e:
                    console.print(f"[dim red]Warning: Could not remove {temp_file}: {e}[/dim red]")
        
        self.cleanup_rules['temp_files']['last_cleanup'] = datetime.now().isoformat()
        
        result = {
            'type': 'temp_files',
            'timestamp': datetime.now().isoformat(),
            'items_cleaned': len(cleaned_items),
            'items': cleaned_items,
            'success': True
        }
        
        if cleaned_items:
            console.print(f"[dim green]✅ Auto-cleaned {len(cleaned_items)} temporary files[/dim green]")
        
        return result
    
    def auto_rotate_logs(self) -> Dict[str, Any]:
        """Automatically rotate and clean old log files"""
        if not self.should_run_cleanup('log_rotation'):
            return {'skipped': True, 'reason': 'Not due for cleanup'}
        
        console.print("[dim]📋 Auto-rotating log files...[/dim]")
        
        logs_dir = Path('logs')
        if not logs_dir.exists():
            logs_dir.mkdir(exist_ok=True)
        
        cleaned_items = []
        max_files = self.cleanup_rules['log_rotation']['max_log_files']
        max_size_mb = self.cleanup_rules['log_rotation']['max_log_size_mb']
        
        # Get all log files sorted by modification time
        log_files = list(logs_dir.glob('*.log'))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove excess log files
        if len(log_files) > max_files:
            for old_log in log_files[max_files:]:
                try:
                    old_log.unlink()
                    cleaned_items.append(f"Removed old log: {old_log.name}")
                except Exception as e:
                    console.print(f"[dim red]Warning: Could not remove {old_log}: {e}[/dim red]")
        
        # Check file sizes and compress large ones
        for log_file in log_files[:max_files]:
            try:
                size_mb = log_file.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    # Simple compression: keep only last 50% of file
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    keep_lines = lines[len(lines)//2:]
                    with open(log_file, 'w', encoding='utf-8') as f:
                        f.writelines(keep_lines)
                    
                    cleaned_items.append(f"Compressed large log: {log_file.name}")
            except Exception as e:
                console.print(f"[dim red]Warning: Could not process {log_file}: {e}[/dim red]")
        
        self.cleanup_rules['log_rotation']['last_cleanup'] = datetime.now().isoformat()
        
        result = {
            'type': 'log_rotation',
            'timestamp': datetime.now().isoformat(),
            'actions_taken': len(cleaned_items),
            'actions': cleaned_items,
            'success': True
        }
        
        if cleaned_items:
            console.print(f"[dim green]✅ Auto-rotated logs: {len(cleaned_items)} actions[/dim green]")
        
        return result
    
    def auto_optimize_memory(self) -> Dict[str, Any]:
        """Automatically optimize memory files"""
        if not self.should_run_cleanup('memory_optimization'):
            return {'skipped': True, 'reason': 'Not due for cleanup'}
        
        console.print("[dim]🧠 Auto-optimizing memory files...[/dim]")
        
        optimized_items = []
        max_entries = self.cleanup_rules['memory_optimization']['max_memory_entries']
        
        memory_files = [
            'memory/knowledge_base.json',
            'memory/questions_archive.json',
            'memory/learning_history.json'
        ]
        
        for memory_file in memory_files:
            if not Path(memory_file).exists():
                continue
            
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                original_size = len(str(data))
                
                # Optimize based on file type
                if 'knowledge_base' in memory_file and isinstance(data, dict):
                    if len(data) > max_entries:
                        # Keep most recent entries
                        sorted_items = sorted(data.items(), 
                                            key=lambda x: x[1].get('information', {}).get('timestamp', 0), 
                                            reverse=True)
                        data = dict(sorted_items[:max_entries])
                
                elif 'questions_archive' in memory_file and isinstance(data, list):
                    if len(data) > max_entries:
                        # Keep most recent questions
                        data = sorted(data, 
                                    key=lambda x: x.get('generated_at', ''), 
                                    reverse=True)[:max_entries]
                
                elif 'learning_history' in memory_file and isinstance(data, list):
                    if len(data) > max_entries:
                        # Keep most recent learning sessions
                        data = data[-max_entries:]
                
                # Save optimized data
                with open(memory_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                new_size = len(str(data))
                if new_size < original_size:
                    optimized_items.append({
                        'file': memory_file,
                        'size_reduction': original_size - new_size,
                        'entries_kept': len(data) if isinstance(data, (list, dict)) else 'unknown'
                    })
            
            except Exception as e:
                console.print(f"[dim red]Warning: Could not optimize {memory_file}: {e}[/dim red]")
        
        self.cleanup_rules['memory_optimization']['last_cleanup'] = datetime.now().isoformat()
        
        result = {
            'type': 'memory_optimization',
            'timestamp': datetime.now().isoformat(),
            'files_optimized': len(optimized_items),
            'optimizations': optimized_items,
            'success': True
        }
        
        if optimized_items:
            total_saved = sum(item['size_reduction'] for item in optimized_items)
            console.print(f"[dim green]✅ Auto-optimized memory: {len(optimized_items)} files, saved {total_saved} bytes[/dim green]")
        
        return result
    
    def run_auto_cleanup(self) -> Dict[str, Any]:
        """Run all automatic cleanup tasks that are due"""
        console.print("[dim]🤖 Running automatic cleanup...[/dim]")
        
        cleanup_results = []
        
        # Run each cleanup type
        cleanup_functions = [
            self.auto_cleanup_cache_files,
            self.auto_cleanup_temp_files,
            self.auto_rotate_logs,
            self.auto_optimize_memory
        ]
        
        for cleanup_func in cleanup_functions:
            try:
                result = cleanup_func()
                if not result.get('skipped', False):
                    cleanup_results.append(result)
            except Exception as e:
                console.print(f"[dim red]Error in {cleanup_func.__name__}: {e}[/dim red]")
        
        # Record cleanup session
        session = {
            'timestamp': datetime.now().isoformat(),
            'results': cleanup_results,
            'total_actions': sum(r.get('items_cleaned', r.get('actions_taken', r.get('files_optimized', 0))) for r in cleanup_results)
        }
        
        self.cleanup_history.append(session)
        
        # Keep only last 50 cleanup sessions
        if len(self.cleanup_history) > 50:
            self.cleanup_history = self.cleanup_history[-50:]
        
        # Save cleanup data
        self.save_cleanup_data()
        
        if cleanup_results:
            total_actions = session['total_actions']
            console.print(f"[dim green]✅ Auto-cleanup complete: {total_actions} actions across {len(cleanup_results)} categories[/dim green]")
        
        return session
    
    def get_cleanup_status(self) -> Dict[str, Any]:
        """Get current cleanup status"""
        status = {
            'last_cleanup': self.cleanup_history[-1]['timestamp'] if self.cleanup_history else None,
            'total_cleanups': len(self.cleanup_history),
            'rules': {}
        }
        
        for rule_name, rule_config in self.cleanup_rules.items():
            next_cleanup = None
            if rule_config.get('last_cleanup'):
                last_time = datetime.fromisoformat(rule_config['last_cleanup'])
                next_time = last_time + timedelta(hours=rule_config['frequency_hours'])
                next_cleanup = next_time.isoformat()
            
            status['rules'][rule_name] = {
                'enabled': rule_config['enabled'],
                'frequency_hours': rule_config['frequency_hours'],
                'last_cleanup': rule_config.get('last_cleanup'),
                'next_cleanup': next_cleanup,
                'due_now': self.should_run_cleanup(rule_name)
            }
        
        return status
    
    def load_cleanup_data(self):
        """Load cleanup configuration and history"""
        try:
            cleanup_file = "memory/auto_cleanup.json"
            if os.path.exists(cleanup_file):
                with open(cleanup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cleanup_history = data.get('cleanup_history', [])
                    
                    # Update rules with saved last_cleanup times
                    saved_rules = data.get('cleanup_rules', {})
                    for rule_name, saved_rule in saved_rules.items():
                        if rule_name in self.cleanup_rules:
                            self.cleanup_rules[rule_name]['last_cleanup'] = saved_rule.get('last_cleanup')
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load cleanup data: {e}[/dim yellow]")
    
    def save_cleanup_data(self):
        """Save cleanup configuration and history"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            cleanup_file = "memory/auto_cleanup.json"
            
            data = {
                'cleanup_rules': self.cleanup_rules,
                'cleanup_history': self.cleanup_history,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(cleanup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[dim red]Error saving cleanup data: {e}[/dim red]")

    def start_background_service(self):
        """Start the background cleanup service"""
        if self.background_service_running:
            return

        self.background_service_running = True
        self.background_thread = threading.Thread(target=self._background_cleanup_loop, daemon=True)
        self.background_thread.start()
        console.print("[dim green]🤖 Background cleanup service started[/dim green]")

    def stop_background_service(self):
        """Stop the background cleanup service"""
        self.background_service_running = False
        if self.background_thread:
            self.background_thread.join(timeout=1)
        console.print("[dim yellow]🛑 Background cleanup service stopped[/dim yellow]")

    def _background_cleanup_loop(self):
        """Background loop that runs cleanup tasks"""
        while self.background_service_running:
            try:
                # Check every 30 minutes if any cleanup is due
                time.sleep(1800)  # 30 minutes

                if not self.background_service_running:
                    break

                # Run cleanup if any task is due
                due_tasks = [name for name in self.cleanup_rules.keys()
                           if self.should_run_cleanup(name)]

                if due_tasks:
                    console.print(f"[dim]🤖 Background cleanup: {len(due_tasks)} tasks due[/dim]")
                    self.run_auto_cleanup()

            except Exception as e:
                console.print(f"[dim red]Background cleanup error: {e}[/dim red]")
                time.sleep(300)  # Wait 5 minutes before retrying

    def force_cleanup_now(self):
        """Force immediate cleanup of all tasks regardless of schedule"""
        console.print("[yellow]🔥 Forcing immediate cleanup of all tasks...[/yellow]")

        # Temporarily reset all last_cleanup times to force execution
        original_times = {}
        for rule_name in self.cleanup_rules:
            original_times[rule_name] = self.cleanup_rules[rule_name].get('last_cleanup')
            self.cleanup_rules[rule_name]['last_cleanup'] = None

        # Run cleanup
        result = self.run_auto_cleanup()

        # Restore original times (but keep the new ones from the cleanup)
        # This is handled automatically by run_auto_cleanup()

        return result
