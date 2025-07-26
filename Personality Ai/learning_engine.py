"""
Self-Learning and Reinforcement Engine
Evaluates learning progress and adapts strategies
"""
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
import os
from config import *
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

class LearningEngine:
    def __init__(self):
        self.learning_metrics = {
            'questions_answered': 0,
            'knowledge_gained': 0,
            'search_success_rate': 0.0,
            'learning_efficiency': 0.0,
            'curiosity_satisfaction': 0.0,
            'knowledge_retention': 0.0
        }
        
        self.search_strategies = {
            'broad_exploration': {'weight': 0.4, 'success_rate': 0.0, 'uses': 0},
            'deep_dive': {'weight': 0.3, 'success_rate': 0.0, 'uses': 0},
            'connection_based': {'weight': 0.2, 'success_rate': 0.0, 'uses': 0},
            'random_discovery': {'weight': 0.1, 'success_rate': 0.0, 'uses': 0}
        }
        
        self.learning_goals = {
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
        
        self.performance_history = []
        self.adaptation_log = []
        self.curiosity_drivers = defaultdict(float)
        self.load_learning_state()
        
    def evaluate_learning_session(self, questions_asked: List[Dict], 
                                 knowledge_gained: List[Dict], 
                                 search_results: List[Dict]) -> Dict[str, float]:
        """Evaluate the effectiveness of a learning session"""
        
        evaluation = {
            'session_timestamp': datetime.now().isoformat(),
            'questions_quality': self._evaluate_questions_quality(questions_asked),
            'knowledge_quality': self._evaluate_knowledge_quality(knowledge_gained),
            'search_effectiveness': self._evaluate_search_effectiveness(search_results),
            'learning_progress': self._calculate_learning_progress(knowledge_gained),
            'curiosity_fulfillment': self._measure_curiosity_fulfillment(questions_asked, knowledge_gained)
        }
        
        # Calculate overall session score
        weights = {
            'questions_quality': 0.2,
            'knowledge_quality': 0.3,
            'search_effectiveness': 0.2,
            'learning_progress': 0.2,
            'curiosity_fulfillment': 0.1
        }
        
        overall_score = sum(evaluation[metric] * weight for metric, weight in weights.items())
        evaluation['overall_score'] = overall_score
        
        # Store performance history
        self.performance_history.append(evaluation)
        
        # Update learning metrics
        self._update_learning_metrics(evaluation)
        
        console.print(f"📊 Learning session evaluated: [green]{overall_score:.2f}/1.0[/green]")
        return evaluation
        
    def _evaluate_questions_quality(self, questions: List[Dict]) -> float:
        """Evaluate the quality of questions asked"""
        if not questions:
            return 0.0
            
        quality_score = 0.0
        for question in questions:
            # Complexity bonus
            complexity = question.get('complexity', 1.0)
            quality_score += min(1.0, complexity / 3.0) * 0.3
            
            # Category diversity bonus
            category = question.get('category', '')
            if category in ['research', 'advanced_analysis', 'philosophical']:
                quality_score += 0.2
            elif category in ['relationships', 'applications']:
                quality_score += 0.15
            else:
                quality_score += 0.1
                
            # Follow-up question bonus
            if question.get('is_follow_up', False):
                quality_score += 0.1
                
        return min(1.0, quality_score / len(questions))
        
    def _evaluate_knowledge_quality(self, knowledge_list: List[Dict]) -> float:
        """Evaluate the quality of knowledge gained"""
        if not knowledge_list:
            return 0.0
            
        total_quality = 0.0
        for knowledge in knowledge_list:
            info = knowledge.get('information', {})
            
            # Content richness
            content_score = 0.0
            if info.get('definitions'):
                content_score += len(info['definitions']) * 0.1
            if info.get('examples'):
                content_score += len(info['examples']) * 0.08
            if info.get('interesting_facts'):
                content_score += len(info['interesting_facts']) * 0.12
            if info.get('key_concepts'):
                content_score += len(info['key_concepts']) * 0.06
                
            # Source reliability
            sources = info.get('sources', [])
            source_score = min(1.0, len(sources) * 0.1)
            
            # Combine scores
            knowledge_quality = min(1.0, content_score + source_score)
            total_quality += knowledge_quality
            
        return total_quality / len(knowledge_list)
        
    def _evaluate_search_effectiveness(self, search_results: List[Dict]) -> float:
        """Evaluate how effective the search strategies were"""
        if not search_results:
            return 0.0
            
        effectiveness = 0.0
        for result in search_results:
            # Result relevance (based on content length and source type)
            content_length = len(result.get('content', ''))
            if content_length > 500:
                effectiveness += 0.3
            elif content_length > 200:
                effectiveness += 0.2
            else:
                effectiveness += 0.1
                
            # Source credibility
            source = result.get('source', '')
            if source == 'wikipedia':
                effectiveness += 0.2
            elif source == 'google':
                effectiveness += 0.15
            else:
                effectiveness += 0.1
                
        return min(1.0, effectiveness / len(search_results))
        
    def _calculate_learning_progress(self, knowledge_gained: List[Dict]) -> float:
        """Calculate learning progress based on knowledge complexity and connections"""
        if not knowledge_gained:
            return 0.0
            
        progress = 0.0
        for knowledge in knowledge_gained:
            # Complexity progression
            topic = knowledge.get('topic', '')
            if any(advanced_topic in topic.lower() for advanced_topic in ADVANCED_TOPICS):
                progress += 0.3
            elif any(core_topic in topic.lower() for core_topic in CORE_PERSONALITY_TOPICS):
                progress += 0.2
            else:
                progress += 0.1
                
            # Connection potential
            info = knowledge.get('information', {})
            if info.get('key_concepts'):
                progress += len(info['key_concepts']) * 0.02
                
        return min(1.0, progress / len(knowledge_gained))
        
    def _measure_curiosity_fulfillment(self, questions: List[Dict], knowledge: List[Dict]) -> float:
        """Measure how well curiosity was satisfied"""
        if not questions:
            return 0.0
            
        # Simple heuristic: ratio of knowledge gained to questions asked
        fulfillment = len(knowledge) / len(questions) if questions else 0.0
        
        # Bonus for getting interesting facts
        interesting_facts_count = sum(
            len(k.get('information', {}).get('interesting_facts', [])) 
            for k in knowledge
        )
        fulfillment += interesting_facts_count * 0.1
        
        return min(1.0, fulfillment)
        
    def _update_learning_metrics(self, evaluation: Dict[str, float]):
        """Update overall learning metrics based on session evaluation"""
        # Update with exponential moving average
        alpha = 0.3  # Learning rate
        
        self.learning_metrics['questions_answered'] += 1
        self.learning_metrics['knowledge_gained'] += 1
        
        # Update rates with moving average
        self.learning_metrics['search_success_rate'] = (
            (1 - alpha) * self.learning_metrics['search_success_rate'] + 
            alpha * evaluation['search_effectiveness']
        )
        
        self.learning_metrics['learning_efficiency'] = (
            (1 - alpha) * self.learning_metrics['learning_efficiency'] + 
            alpha * evaluation['overall_score']
        )
        
        self.learning_metrics['curiosity_satisfaction'] = (
            (1 - alpha) * self.learning_metrics['curiosity_satisfaction'] + 
            alpha * evaluation['curiosity_fulfillment']
        )
        
    def adapt_search_strategy(self, recent_performance: List[Dict]) -> str:
        """Adapt search strategy based on recent performance"""
        if len(recent_performance) < 3:
            return 'broad_exploration'  # Default for new learners
            
        # Analyze recent performance by strategy
        strategy_performance = defaultdict(list)
        
        for session in recent_performance[-10:]:  # Last 10 sessions
            strategy_used = session.get('strategy_used', 'broad_exploration')
            score = session.get('overall_score', 0.0)
            strategy_performance[strategy_used].append(score)
            
        # Update strategy success rates
        for strategy, scores in strategy_performance.items():
            if strategy in self.search_strategies and scores:
                avg_score = sum(scores) / len(scores)
                self.search_strategies[strategy]['success_rate'] = avg_score
                self.search_strategies[strategy]['uses'] += len(scores)
                
        # Adapt strategy weights based on performance
        self._rebalance_strategy_weights()
        
        # Choose strategy based on weighted probabilities
        strategies = list(self.search_strategies.keys())
        weights = [self.search_strategies[s]['weight'] for s in strategies]
        
        # Add some randomness for exploration
        if random.random() < 0.1:  # 10% chance of random exploration
            chosen_strategy = random.choice(strategies)
        else:
            chosen_strategy = random.choices(strategies, weights=weights)[0]
            
        console.print(f"🎯 Adapted search strategy: [cyan]{chosen_strategy}[/cyan]")
        
        # Log adaptation
        self.adaptation_log.append({
            'timestamp': datetime.now().isoformat(),
            'old_weights': {s: data['weight'] for s, data in self.search_strategies.items()},
            'chosen_strategy': chosen_strategy,
            'reason': 'performance_based_adaptation'
        })
        
        return chosen_strategy
        
    def _rebalance_strategy_weights(self):
        """Rebalance strategy weights based on success rates"""
        total_success = sum(
            max(0.1, data['success_rate']) for data in self.search_strategies.values()
        )
        
        if total_success > 0:
            for strategy, data in self.search_strategies.items():
                # Normalize success rate to weight
                normalized_success = max(0.1, data['success_rate']) / total_success
                
                # Smooth transition (don't change weights too drastically)
                current_weight = data['weight']
                new_weight = 0.7 * current_weight + 0.3 * normalized_success
                
                self.search_strategies[strategy]['weight'] = new_weight
                
    def generate_learning_goals(self, current_knowledge: Dict[str, Any], 
                              complexity_level: float) -> Dict[str, List[str]]:
        """Generate adaptive learning goals based on current state"""
        
        goals = {
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
        
        # Analyze knowledge gaps
        covered_topics = set(current_knowledge.keys())
        
        # Short-term goals (next 1-3 sessions)
        remaining_core = [t for t in CORE_PERSONALITY_TOPICS if t not in covered_topics]
        if remaining_core:
            goals['short_term'].extend(remaining_core[:3])
        else:
            # Focus on deepening existing knowledge
            most_basic_topics = [
                topic for topic, data in current_knowledge.items()
                if self._assess_topic_depth(data) < 0.5
            ]
            goals['short_term'].extend(most_basic_topics[:3])
            
        # Medium-term goals (next 5-10 sessions)
        if complexity_level > 1.5:
            remaining_advanced = [t for t in ADVANCED_TOPICS if t not in covered_topics]
            goals['medium_term'].extend(remaining_advanced[:5])
        else:
            goals['medium_term'].extend(remaining_core[3:8])
            
        # Long-term goals (aspirational)
        goals['long_term'] = [
            "Master advanced personality psychology theories",
            "Understand cross-cultural personality differences",
            "Develop expertise in personality assessment",
            "Explore personality-behavior prediction models",
            "Investigate personality change mechanisms"
        ]
        
        self.learning_goals = goals
        return goals
        
    def _assess_topic_depth(self, topic_data: Any) -> float:
        """Assess how deeply a topic has been learned"""
        if not isinstance(topic_data, dict):
            return 0.0
            
        depth_indicators = 0.0
        
        # Check for different types of knowledge
        info = topic_data.get('information', {})
        if info.get('definitions'):
            depth_indicators += 0.2
        if info.get('examples'):
            depth_indicators += 0.2
        if info.get('interesting_facts'):
            depth_indicators += 0.3
        if info.get('key_concepts'):
            depth_indicators += 0.2
        if len(info.get('sources', [])) > 3:
            depth_indicators += 0.1
            
        return min(1.0, depth_indicators)
        
    def recommend_next_actions(self, current_state: Dict[str, Any]) -> List[str]:
        """Recommend next learning actions based on current state"""
        recommendations = []
        
        # Analyze current performance
        recent_performance = self.performance_history[-5:] if self.performance_history else []
        avg_performance = sum(p['overall_score'] for p in recent_performance) / len(recent_performance) if recent_performance else 0.5
        
        if avg_performance < 0.4:
            recommendations.append("Focus on simpler, foundational topics to build confidence")
            recommendations.append("Use more Wikipedia sources for reliable basic information")
        elif avg_performance < 0.7:
            recommendations.append("Balance broad exploration with deep dives into interesting topics")
            recommendations.append("Generate more follow-up questions to deepen understanding")
        else:
            recommendations.append("Explore advanced and interdisciplinary topics")
            recommendations.append("Focus on connecting different areas of knowledge")
            
        # Check learning goals progress
        if self.learning_goals['short_term']:
            recommendations.append(f"Work on short-term goal: {self.learning_goals['short_term'][0]}")
            
        # Curiosity-driven recommendations
        if self.learning_metrics['curiosity_satisfaction'] < 0.5:
            recommendations.append("Ask more diverse types of questions to satisfy curiosity")
            
        return recommendations
        
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about learning patterns and progress"""
        insights = {
            'current_metrics': self.learning_metrics.copy(),
            'strategy_effectiveness': {
                strategy: {
                    'success_rate': data['success_rate'],
                    'usage_count': data['uses'],
                    'current_weight': data['weight']
                }
                for strategy, data in self.search_strategies.items()
            },
            'learning_trajectory': self._analyze_learning_trajectory(),
            'strengths': self._identify_strengths(),
            'improvement_areas': self._identify_improvement_areas(),
            'next_milestones': self._predict_next_milestones()
        }
        
        return insights
        
    def _analyze_learning_trajectory(self) -> Dict[str, Any]:
        """Analyze learning trajectory over time"""
        if len(self.performance_history) < 2:
            return {'trend': 'insufficient_data'}
            
        recent_scores = [p['overall_score'] for p in self.performance_history[-10:]]
        early_scores = [p['overall_score'] for p in self.performance_history[:5]]
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        early_avg = sum(early_scores) / len(early_scores)
        
        improvement = recent_avg - early_avg
        
        return {
            'trend': 'improving' if improvement > 0.1 else 'stable' if improvement > -0.1 else 'declining',
            'improvement_rate': improvement,
            'recent_average': recent_avg,
            'sessions_analyzed': len(self.performance_history)
        }
        
    def _identify_strengths(self) -> List[str]:
        """Identify learning strengths"""
        strengths = []
        
        if self.learning_metrics['search_success_rate'] > 0.7:
            strengths.append("Effective information searching")
        if self.learning_metrics['learning_efficiency'] > 0.7:
            strengths.append("High learning efficiency")
        if self.learning_metrics['curiosity_satisfaction'] > 0.6:
            strengths.append("Good curiosity-driven learning")
            
        # Analyze strategy strengths
        best_strategy = max(self.search_strategies.items(), key=lambda x: x[1]['success_rate'])
        if best_strategy[1]['success_rate'] > 0.6:
            strengths.append(f"Strong performance with {best_strategy[0]} strategy")
            
        return strengths
        
    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        if self.learning_metrics['search_success_rate'] < 0.5:
            improvements.append("Search strategy optimization needed")
        if self.learning_metrics['learning_efficiency'] < 0.5:
            improvements.append("Learning efficiency could be improved")
        if self.learning_metrics['curiosity_satisfaction'] < 0.4:
            improvements.append("Need more engaging and satisfying learning experiences")
            
        return improvements
        
    def _predict_next_milestones(self) -> List[str]:
        """Predict upcoming learning milestones"""
        milestones = []
        
        current_efficiency = self.learning_metrics['learning_efficiency']
        
        if current_efficiency < 0.5:
            milestones.append("Reach 50% learning efficiency")
        elif current_efficiency < 0.7:
            milestones.append("Achieve 70% learning efficiency")
        else:
            milestones.append("Maintain high performance while exploring advanced topics")
            
        milestones.append("Complete all core personality topics")
        milestones.append("Begin advanced interdisciplinary learning")
        
        return milestones
        
    def save_learning_state(self):
        """Save learning engine state"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            
            state = {
                'learning_metrics': self.learning_metrics,
                'search_strategies': self.search_strategies,
                'learning_goals': self.learning_goals,
                'performance_history': self.performance_history[-100:],  # Keep last 100
                'adaptation_log': self.adaptation_log[-50:],  # Keep last 50
                'curiosity_drivers': dict(self.curiosity_drivers)
            }
            
            with open(f"{MEMORY_DIR}/learning_state.json", 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[red]Error saving learning state: {e}[/red]")
            
    def load_learning_state(self):
        """Load learning engine state"""
        try:
            state_file = f"{MEMORY_DIR}/learning_state.json"
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    
                self.learning_metrics.update(state.get('learning_metrics', {}))
                self.search_strategies.update(state.get('search_strategies', {}))
                self.learning_goals.update(state.get('learning_goals', {}))
                self.performance_history = state.get('performance_history', [])
                self.adaptation_log = state.get('adaptation_log', [])
                self.curiosity_drivers = defaultdict(float, state.get('curiosity_drivers', {}))
                
        except Exception as e:
            console.print(f"[yellow]Could not load learning state: {e}[/yellow]")
