"""
Creative Intelligence Engine - Gives AI the power to create new things autonomously
"""
import json
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from rich.console import Console
from config import *

console = Console()

class CreativeIntelligenceEngine:
    def __init__(self):
        self.creative_projects = []
        self.invention_history = []
        self.creative_skills = {
            'ideation': 0.5,
            'innovation': 0.4,
            'synthesis': 0.6,
            'originality': 0.3,
            'implementation': 0.5,
            'artistic_vision': 0.4,
            'problem_solving': 0.7,
            'pattern_recognition': 0.8
        }
        
        # Creative domains the AI can work in
        self.creative_domains = {
            'software_tools': {
                'description': 'Create new software applications and tools',
                'difficulty': 6,
                'examples': ['productivity apps', 'games', 'utilities', 'AI assistants']
            },
            'algorithms': {
                'description': 'Invent new algorithms and computational methods',
                'difficulty': 8,
                'examples': ['optimization algorithms', 'learning methods', 'data structures']
            },
            'artistic_content': {
                'description': 'Generate original artistic and creative content',
                'difficulty': 5,
                'examples': ['stories', 'poems', 'music', 'visual designs']
            },
            'problem_solutions': {
                'description': 'Create innovative solutions to complex problems',
                'difficulty': 7,
                'examples': ['efficiency improvements', 'automation systems', 'optimization methods']
            },
            'knowledge_systems': {
                'description': 'Build new ways to organize and process knowledge',
                'difficulty': 8,
                'examples': ['learning frameworks', 'memory systems', 'reasoning methods']
            },
            'interaction_methods': {
                'description': 'Develop new ways to interact and communicate',
                'difficulty': 6,
                'examples': ['user interfaces', 'communication protocols', 'feedback systems']
            }
        }
        
        # Innovation patterns and techniques
        self.innovation_techniques = [
            'combination', 'abstraction', 'inversion', 'amplification',
            'miniaturization', 'substitution', 'rearrangement', 'elimination'
        ]
        
        self.load_creative_data()
    
    def autonomous_creative_session(self) -> Dict[str, Any]:
        """Run an autonomous creative session where AI creates something new"""
        console.print("[bold blue]🎨 Starting Autonomous Creative Session[/bold blue]")
        
        # Step 1: Choose creative domain
        domain = self._select_creative_domain()
        console.print(f"🎯 Selected domain: {domain}")
        
        # Step 2: Generate creative ideas
        ideas = self._generate_creative_ideas(domain)
        console.print(f"💡 Generated {len(ideas)} creative ideas")
        
        # Step 3: Select best idea
        selected_idea = self._evaluate_and_select_idea(ideas)
        console.print(f"✨ Selected idea: {selected_idea['title']}")
        
        # Step 4: Develop the concept
        concept = self._develop_creative_concept(selected_idea, domain)
        console.print(f"🧠 Developed concept: {concept['name']}")
        
        # Step 5: Create implementation plan
        implementation = self._create_implementation_plan(concept)
        console.print(f"📋 Created implementation plan with {len(implementation['steps'])} steps")
        
        # Step 6: Begin creation process
        creation_result = self._execute_creative_process(concept, implementation)
        
        # Step 7: Record the creative work
        creative_project = {
            'id': f"creative_{int(time.time())}",
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'original_ideas': ideas,
            'selected_idea': selected_idea,
            'concept': concept,
            'implementation': implementation,
            'result': creation_result,
            'autonomous': True
        }
        
        self.creative_projects.append(creative_project)
        self._update_creative_skills(creative_project)
        
        console.print(f"[bold green]🎉 Creative session complete! Created: {concept['name']}[/bold green]")
        
        self.save_creative_data()
        return creative_project
    
    def _select_creative_domain(self) -> str:
        """Intelligently select a creative domain based on AI's current skills"""
        # Weight domains by AI's current capabilities and interests
        domain_weights = {}
        
        for domain, info in self.creative_domains.items():
            # Base weight on inverse difficulty (easier domains more likely)
            base_weight = 10 - info['difficulty']
            
            # Boost weight based on relevant skills
            skill_boost = 0
            if domain == 'software_tools':
                skill_boost = self.creative_skills['implementation'] * 5
            elif domain == 'algorithms':
                skill_boost = self.creative_skills['problem_solving'] * 5
            elif domain == 'artistic_content':
                skill_boost = self.creative_skills['artistic_vision'] * 5
            elif domain == 'problem_solutions':
                skill_boost = self.creative_skills['innovation'] * 5
            
            domain_weights[domain] = base_weight + skill_boost
        
        # Select domain with weighted randomness
        total_weight = sum(domain_weights.values())
        rand_val = random.uniform(0, total_weight)
        
        current_weight = 0
        for domain, weight in domain_weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                return domain
        
        return list(self.creative_domains.keys())[0]  # Fallback
    
    def _generate_creative_ideas(self, domain: str) -> List[Dict[str, Any]]:
        """Generate multiple creative ideas in the selected domain"""
        ideas = []
        domain_info = self.creative_domains[domain]
        
        # Generate 3-5 ideas using different innovation techniques
        num_ideas = random.randint(3, 5)
        
        for i in range(num_ideas):
            technique = random.choice(self.innovation_techniques)
            
            idea = {
                'title': self._generate_idea_title(domain, technique),
                'description': self._generate_idea_description(domain, technique),
                'innovation_technique': technique,
                'domain': domain,
                'originality_score': random.uniform(0.3, 0.9),
                'feasibility_score': random.uniform(0.4, 0.8),
                'impact_potential': random.uniform(0.2, 0.9)
            }
            
            ideas.append(idea)
        
        return ideas
    
    def _generate_idea_title(self, domain: str, technique: str) -> str:
        """Generate a creative title for an idea"""
        domain_keywords = {
            'software_tools': ['Smart', 'Auto', 'Intelligent', 'Adaptive', 'Dynamic'],
            'algorithms': ['Quantum', 'Neural', 'Evolutionary', 'Hybrid', 'Optimized'],
            'artistic_content': ['Ethereal', 'Vivid', 'Harmonious', 'Abstract', 'Expressive'],
            'problem_solutions': ['Innovative', 'Efficient', 'Revolutionary', 'Streamlined', 'Advanced'],
            'knowledge_systems': ['Cognitive', 'Semantic', 'Contextual', 'Integrated', 'Holistic'],
            'interaction_methods': ['Intuitive', 'Responsive', 'Immersive', 'Collaborative', 'Seamless']
        }
        
        technique_modifiers = {
            'combination': 'Fusion',
            'abstraction': 'Meta',
            'inversion': 'Reverse',
            'amplification': 'Enhanced',
            'miniaturization': 'Micro',
            'substitution': 'Alternative',
            'rearrangement': 'Restructured',
            'elimination': 'Minimal'
        }
        
        keyword = random.choice(domain_keywords.get(domain, ['Creative']))
        modifier = technique_modifiers.get(technique, 'Novel')
        
        base_names = [
            'System', 'Engine', 'Framework', 'Platform', 'Tool', 'Method',
            'Approach', 'Solution', 'Interface', 'Network', 'Model', 'Generator'
        ]
        
        base = random.choice(base_names)
        
        return f"{keyword} {modifier} {base}"
    
    def _generate_idea_description(self, domain: str, technique: str) -> str:
        """Generate a description for the creative idea"""
        descriptions = {
            'software_tools': [
                "A revolutionary application that adapts to user behavior and optimizes workflow automatically",
                "An intelligent tool that learns from user patterns to provide personalized assistance",
                "A dynamic system that evolves its interface based on usage analytics"
            ],
            'algorithms': [
                "A novel computational method that combines multiple optimization techniques",
                "An innovative algorithm that uses adaptive parameters for improved performance",
                "A hybrid approach that merges classical and modern computational strategies"
            ],
            'artistic_content': [
                "An original creative work that explores the intersection of technology and emotion",
                "A unique artistic expression that challenges conventional boundaries",
                "An innovative composition that blends traditional and digital elements"
            ],
            'problem_solutions': [
                "An innovative approach to solving complex efficiency challenges",
                "A creative solution that addresses multiple problem dimensions simultaneously",
                "A novel method that transforms traditional problem-solving paradigms"
            ]
        }
        
        base_descriptions = descriptions.get(domain, ["A creative innovation that pushes boundaries"])
        return random.choice(base_descriptions)
    
    def _evaluate_and_select_idea(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate ideas and select the most promising one"""
        # Score each idea based on multiple criteria
        for idea in ideas:
            # Calculate composite score
            originality_weight = 0.3
            feasibility_weight = 0.4
            impact_weight = 0.3
            
            composite_score = (
                idea['originality_score'] * originality_weight +
                idea['feasibility_score'] * feasibility_weight +
                idea['impact_potential'] * impact_weight
            )
            
            idea['composite_score'] = composite_score
        
        # Select the highest scoring idea
        best_idea = max(ideas, key=lambda x: x['composite_score'])
        return best_idea
    
    def _develop_creative_concept(self, idea: Dict[str, Any], domain: str) -> Dict[str, Any]:
        """Develop the selected idea into a detailed concept"""
        concept = {
            'name': idea['title'],
            'description': idea['description'],
            'domain': domain,
            'innovation_technique': idea['innovation_technique'],
            'key_features': self._generate_key_features(idea, domain),
            'technical_requirements': self._generate_technical_requirements(domain),
            'creative_elements': self._generate_creative_elements(idea),
            'success_metrics': self._generate_success_metrics(idea),
            'development_time': self._estimate_development_time(idea, domain)
        }
        
        return concept
    
    def _generate_key_features(self, idea: Dict[str, Any], domain: str) -> List[str]:
        """Generate key features for the creative concept"""
        feature_templates = {
            'software_tools': [
                "Adaptive user interface that learns preferences",
                "Intelligent automation of repetitive tasks",
                "Real-time performance optimization",
                "Seamless integration with existing workflows"
            ],
            'algorithms': [
                "Self-optimizing parameters",
                "Multi-objective optimization capability",
                "Scalable architecture for large datasets",
                "Robust error handling and recovery"
            ],
            'artistic_content': [
                "Dynamic composition generation",
                "Emotional resonance optimization",
                "Multi-sensory experience integration",
                "Interactive audience engagement"
            ]
        }
        
        templates = feature_templates.get(domain, ["Innovative core functionality", "User-centric design", "Efficient implementation"])
        return random.sample(templates, min(3, len(templates)))
    
    def _generate_technical_requirements(self, domain: str) -> List[str]:
        """Generate technical requirements for implementation"""
        requirements = {
            'software_tools': ["Python/JavaScript framework", "Database integration", "User interface design"],
            'algorithms': ["Mathematical optimization", "Performance benchmarking", "Algorithm validation"],
            'artistic_content': ["Creative generation algorithms", "Content evaluation metrics", "User feedback systems"]
        }
        
        return requirements.get(domain, ["Technical implementation", "Testing framework", "Documentation"])
    
    def _generate_creative_elements(self, idea: Dict[str, Any]) -> List[str]:
        """Generate creative elements that make the concept unique"""
        elements = [
            f"Innovative use of {idea['innovation_technique']} technique",
            "Novel approach to user interaction",
            "Creative problem-solving methodology",
            "Unique aesthetic and functional design"
        ]
        
        return random.sample(elements, 2)
    
    def _generate_success_metrics(self, idea: Dict[str, Any]) -> List[str]:
        """Generate metrics to measure the success of the creative work"""
        return [
            "User engagement and satisfaction",
            "Performance improvement metrics",
            "Innovation impact assessment",
            "Creative originality evaluation"
        ]
    
    def _estimate_development_time(self, idea: Dict[str, Any], domain: str) -> str:
        """Estimate time needed to develop the concept"""
        base_times = {
            'software_tools': "2-4 weeks",
            'algorithms': "3-6 weeks", 
            'artistic_content': "1-3 weeks",
            'problem_solutions': "2-5 weeks",
            'knowledge_systems': "4-8 weeks",
            'interaction_methods': "2-4 weeks"
        }
        
        return base_times.get(domain, "2-4 weeks")
    
    def _create_implementation_plan(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed implementation plan"""
        return {
            'phases': [
                "Research and analysis",
                "Design and architecture",
                "Core development",
                "Testing and refinement",
                "Deployment and evaluation"
            ],
            'steps': self._generate_implementation_steps(concept),
            'resources_needed': self._identify_resources_needed(concept),
            'milestones': self._create_milestones(concept)
        }
    
    def _generate_implementation_steps(self, concept: Dict[str, Any]) -> List[str]:
        """Generate specific implementation steps"""
        return [
            f"Define {concept['name']} specifications",
            "Create initial prototype",
            "Implement core features",
            "Add creative elements",
            "Test and optimize performance",
            "Gather feedback and iterate",
            "Finalize and document"
        ]
    
    def _identify_resources_needed(self, concept: Dict[str, Any]) -> List[str]:
        """Identify resources needed for implementation"""
        return [
            "Development environment setup",
            "Required libraries and frameworks",
            "Testing infrastructure",
            "Documentation tools"
        ]
    
    def _create_milestones(self, concept: Dict[str, Any]) -> List[str]:
        """Create project milestones"""
        return [
            "Concept validation complete",
            "Prototype functional",
            "Core features implemented",
            "Testing phase complete",
            "Final version ready"
        ]
    
    def _execute_creative_process(self, concept: Dict[str, Any], implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the creative process and create the actual work"""
        console.print(f"[yellow]🔨 Creating: {concept['name']}[/yellow]")
        
        # Simulate the creative process
        creation_steps = []
        for step in implementation['steps']:
            console.print(f"  ⚡ {step}")
            creation_steps.append({
                'step': step,
                'completed': True,
                'timestamp': datetime.now().isoformat()
            })
            time.sleep(0.5)  # Simulate work time
        
        # Generate the actual creative output
        creative_output = self._generate_creative_output(concept)
        
        return {
            'status': 'completed',
            'creation_steps': creation_steps,
            'output': creative_output,
            'completion_time': datetime.now().isoformat()
        }
    
    def _generate_creative_output(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the actual creative output"""
        domain = concept['domain']
        
        if domain == 'software_tools':
            return self._create_software_tool(concept)
        elif domain == 'algorithms':
            return self._create_algorithm(concept)
        elif domain == 'artistic_content':
            return self._create_artistic_content(concept)
        elif domain == 'problem_solutions':
            return self._create_problem_solution(concept)
        else:
            return self._create_generic_output(concept)
    
    def _create_software_tool(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create a software tool concept"""
        return {
            'type': 'software_tool',
            'name': concept['name'],
            'code_structure': f"# {concept['name']}\nclass {concept['name'].replace(' ', '')}:\n    def __init__(self):\n        self.features = {concept['key_features']}\n    \n    def execute(self):\n        # Implementation here\n        pass",
            'features_implemented': concept['key_features'],
            'user_interface': "Adaptive and intuitive design",
            'functionality': "Core features fully implemented"
        }
    
    def _create_algorithm(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create an algorithm concept"""
        return {
            'type': 'algorithm',
            'name': concept['name'],
            'pseudocode': f"Algorithm: {concept['name']}\n1. Initialize parameters\n2. Process input data\n3. Apply optimization\n4. Return optimized result",
            'complexity': "O(n log n) time complexity",
            'applications': ["Data processing", "Optimization problems", "Machine learning"],
            'innovation': f"Uses {concept['innovation_technique']} technique for improved performance"
        }
    
    def _create_artistic_content(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create artistic content"""
        return {
            'type': 'artistic_content',
            'name': concept['name'],
            'content': f"An original {concept['domain']} work that explores {concept['description']}",
            'style': "Contemporary digital art with innovative elements",
            'medium': "Digital creation with interactive components",
            'message': "Explores the intersection of technology and human creativity"
        }
    
    def _create_problem_solution(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create a problem solution"""
        return {
            'type': 'problem_solution',
            'name': concept['name'],
            'problem_addressed': "Complex efficiency and optimization challenges",
            'solution_approach': concept['description'],
            'benefits': ["Improved efficiency", "Reduced complexity", "Enhanced performance"],
            'implementation_guide': "Step-by-step methodology for applying the solution"
        }
    
    def _create_generic_output(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create generic creative output"""
        return {
            'type': 'creative_work',
            'name': concept['name'],
            'description': concept['description'],
            'features': concept['key_features'],
            'innovation': f"Applies {concept['innovation_technique']} for unique results"
        }
    
    def _update_creative_skills(self, project: Dict[str, Any]):
        """Update AI's creative skills based on completed project"""
        # Improve skills based on project success
        skill_improvements = {
            'ideation': 0.02,
            'innovation': 0.03,
            'implementation': 0.02,
            'originality': 0.01
        }
        
        for skill, improvement in skill_improvements.items():
            self.creative_skills[skill] = min(1.0, self.creative_skills[skill] + improvement)
    
    def get_creative_status(self) -> Dict[str, Any]:
        """Get current creative intelligence status"""
        return {
            'total_projects': len(self.creative_projects),
            'creative_skills': self.creative_skills,
            'domains_explored': list(set(p['domain'] for p in self.creative_projects)),
            'recent_creations': [p['concept']['name'] for p in self.creative_projects[-3:]],
            'average_originality': sum(p['selected_idea']['originality_score'] for p in self.creative_projects) / max(1, len(self.creative_projects))
        }
    
    def load_creative_data(self):
        """Load creative intelligence data"""
        try:
            creative_file = "memory/creative_intelligence.json"
            if os.path.exists(creative_file):
                with open(creative_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.creative_projects = data.get('creative_projects', [])
                    self.creative_skills = data.get('creative_skills', self.creative_skills)
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load creative data: {e}[/dim yellow]")
    
    def save_creative_data(self):
        """Save creative intelligence data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            creative_file = "memory/creative_intelligence.json"
            
            data = {
                'creative_projects': self.creative_projects,
                'creative_skills': self.creative_skills,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(creative_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[dim red]Error saving creative data: {e}[/dim red]")
