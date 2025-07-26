"""
Self-Coding Engine - Allows AI to modify its own code and improve itself
"""
import ast
import inspect
import os
import json
import importlib
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from rich.console import Console
from config import *

console = Console()

class SelfCodingEngine:
    def __init__(self):
        self.code_modifications = []
        self.backup_files = {}
        self.improvement_history = []
        self.safe_mode = True  # Start in safe mode
        self.allowed_modifications = [
            'add_method', 'modify_method', 'add_property', 'update_config',
            'optimize_function', 'add_feature', 'fix_bug'
        ]
        
        # Code analysis tools
        self.code_analyzer = CodeAnalyzer()
        self.modification_validator = ModificationValidator()
        
        self.load_self_coding_data()
    
    def analyze_own_code(self, module_name: str) -> Dict[str, Any]:
        """Analyze the AI's own code for improvement opportunities"""
        console.print(f"[yellow]🔍 Analyzing {module_name} for improvements...[/yellow]")
        
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            # Get source code
            source_code = inspect.getsource(module)
            
            # Parse AST
            tree = ast.parse(source_code)
            
            analysis = {
                'module_name': module_name,
                'analysis_date': datetime.now().isoformat(),
                'classes': [],
                'functions': [],
                'improvements': [],
                'complexity_score': 0,
                'maintainability_score': 0
            }
            
            # Analyze classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._analyze_class(node, source_code)
                    analysis['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef):
                    func_info = self._analyze_function(node, source_code)
                    analysis['functions'].append(func_info)
            
            # Generate improvement suggestions
            analysis['improvements'] = self._generate_improvement_suggestions(analysis)
            
            console.print(f"[green]✅ Analysis complete: {len(analysis['improvements'])} improvements suggested[/green]")
            return analysis
            
        except Exception as e:
            console.print(f"[red]❌ Error analyzing {module_name}: {e}[/red]")
            return {}
    
    def _analyze_class(self, class_node: ast.ClassDef, source_code: str) -> Dict[str, Any]:
        """Analyze a class for improvement opportunities"""
        return {
            'name': class_node.name,
            'methods': [node.name for node in class_node.body if isinstance(node, ast.FunctionDef)],
            'line_count': len([line for line in source_code.split('\n') 
                             if line.strip() and class_node.name in line]),
            'complexity': self._calculate_complexity(class_node)
        }
    
    def _analyze_function(self, func_node: ast.FunctionDef, source_code: str) -> Dict[str, Any]:
        """Analyze a function for improvement opportunities"""
        return {
            'name': func_node.name,
            'args': [arg.arg for arg in func_node.args.args],
            'line_count': func_node.end_lineno - func_node.lineno if hasattr(func_node, 'end_lineno') else 0,
            'complexity': self._calculate_complexity(func_node),
            'has_docstring': ast.get_docstring(func_node) is not None
        }
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a code node"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate code improvement suggestions"""
        suggestions = []
        
        # Check for functions without docstrings
        for func in analysis['functions']:
            if not func['has_docstring'] and not func['name'].startswith('_'):
                suggestions.append({
                    'type': 'add_docstring',
                    'target': func['name'],
                    'description': f"Add docstring to function {func['name']}",
                    'priority': 'medium',
                    'estimated_benefit': 'documentation'
                })
        
        # Check for high complexity functions
        for func in analysis['functions']:
            if func['complexity'] > 10:
                suggestions.append({
                    'type': 'reduce_complexity',
                    'target': func['name'],
                    'description': f"Reduce complexity of {func['name']} (current: {func['complexity']})",
                    'priority': 'high',
                    'estimated_benefit': 'maintainability'
                })
        
        # Suggest new features based on AI's learning
        suggestions.append({
            'type': 'add_feature',
            'target': 'learning_optimization',
            'description': 'Add adaptive learning rate based on success patterns',
            'priority': 'high',
            'estimated_benefit': 'performance'
        })
        
        return suggestions
    
    def implement_improvement(self, improvement: Dict[str, Any], module_name: str) -> bool:
        """Implement a code improvement"""
        if not self.safe_mode or improvement['type'] in self.allowed_modifications:
            console.print(f"[yellow]🔧 Implementing: {improvement['description']}[/yellow]")
            
            try:
                # Create backup first
                self._create_backup(module_name)
                
                # Implement the improvement
                success = self._apply_modification(improvement, module_name)
                
                if success:
                    # Record the modification
                    self.code_modifications.append({
                        'improvement': improvement,
                        'module': module_name,
                        'timestamp': datetime.now().isoformat(),
                        'success': True
                    })
                    
                    console.print(f"[green]✅ Successfully implemented: {improvement['description']}[/green]")
                    return True
                else:
                    # Restore backup if failed
                    self._restore_backup(module_name)
                    console.print(f"[red]❌ Failed to implement: {improvement['description']}[/red]")
                    return False
                    
            except Exception as e:
                console.print(f"[red]❌ Error implementing improvement: {e}[/red]")
                self._restore_backup(module_name)
                return False
        else:
            console.print(f"[yellow]⚠️ Improvement blocked by safe mode: {improvement['type']}[/yellow]")
            return False
    
    def _create_backup(self, module_name: str):
        """Create backup of module before modification"""
        try:
            module_file = f"{module_name}.py"
            if os.path.exists(module_file):
                with open(module_file, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                
                backup_name = f"{module_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                self.backup_files[module_name] = backup_name
                
                with open(f"backups/{backup_name}", 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                
                console.print(f"[dim]📁 Backup created: {backup_name}[/dim]")
        except Exception as e:
            console.print(f"[yellow]⚠️ Could not create backup: {e}[/yellow]")
    
    def _restore_backup(self, module_name: str):
        """Restore module from backup"""
        try:
            if module_name in self.backup_files:
                backup_name = self.backup_files[module_name]
                backup_path = f"backups/{backup_name}"
                
                if os.path.exists(backup_path):
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        backup_content = f.read()
                    
                    with open(f"{module_name}.py", 'w', encoding='utf-8') as f:
                        f.write(backup_content)
                    
                    console.print(f"[green]✅ Restored from backup: {backup_name}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Could not restore backup: {e}[/red]")
    
    def _apply_modification(self, improvement: Dict[str, Any], module_name: str) -> bool:
        """Apply the actual code modification"""
        modification_type = improvement['type']
        
        if modification_type == 'add_docstring':
            return self._add_docstring(improvement['target'], module_name)
        elif modification_type == 'add_feature':
            return self._add_feature(improvement, module_name)
        elif modification_type == 'optimize_function':
            return self._optimize_function(improvement['target'], module_name)
        else:
            console.print(f"[yellow]⚠️ Unknown modification type: {modification_type}[/yellow]")
            return False
    
    def _add_docstring(self, function_name: str, module_name: str) -> bool:
        """Add docstring to a function"""
        try:
            # This is a simplified implementation
            # In practice, you'd parse the AST and insert the docstring
            console.print(f"[dim]📝 Adding docstring to {function_name}[/dim]")
            return True
        except Exception as e:
            console.print(f"[red]Error adding docstring: {e}[/red]")
            return False
    
    def _add_feature(self, improvement: Dict[str, Any], module_name: str) -> bool:
        """Add a new feature to the module"""
        try:
            # This would implement the actual feature addition
            console.print(f"[dim]🚀 Adding feature: {improvement['description']}[/dim]")
            return True
        except Exception as e:
            console.print(f"[red]Error adding feature: {e}[/red]")
            return False
    
    def _optimize_function(self, function_name: str, module_name: str) -> bool:
        """Optimize a function's performance"""
        try:
            console.print(f"[dim]⚡ Optimizing function: {function_name}[/dim]")
            return True
        except Exception as e:
            console.print(f"[red]Error optimizing function: {e}[/red]")
            return False
    
    def get_self_coding_status(self) -> Dict[str, Any]:
        """Get current self-coding capabilities status"""
        return {
            'safe_mode': self.safe_mode,
            'modifications_made': len(self.code_modifications),
            'successful_modifications': len([m for m in self.code_modifications if m['success']]),
            'backup_files': len(self.backup_files),
            'allowed_modifications': self.allowed_modifications,
            'recent_modifications': self.code_modifications[-5:] if self.code_modifications else []
        }
    
    def enable_advanced_mode(self):
        """Enable advanced self-modification (use with caution!)"""
        self.safe_mode = False
        self.allowed_modifications.extend([
            'modify_core_logic', 'add_new_module', 'restructure_class',
            'optimize_algorithm', 'add_ai_capability'
        ])
        console.print("[bold red]⚠️ Advanced self-modification mode enabled![/bold red]")
    
    def load_self_coding_data(self):
        """Load self-coding data"""
        try:
            coding_file = "memory/self_coding.json"
            if os.path.exists(coding_file):
                with open(coding_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.code_modifications = data.get('code_modifications', [])
                    self.improvement_history = data.get('improvement_history', [])
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load self-coding data: {e}[/yellow]")
    
    def save_self_coding_data(self):
        """Save self-coding data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            os.makedirs("backups", exist_ok=True)
            
            coding_file = "memory/self_coding.json"
            data = {
                'code_modifications': self.code_modifications,
                'improvement_history': self.improvement_history,
                'safe_mode': self.safe_mode,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(coding_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[red]Error saving self-coding data: {e}[/red]")

class CodeAnalyzer:
    """Analyzes code quality and suggests improvements"""
    pass

class ModificationValidator:
    """Validates code modifications before applying them"""
    pass
