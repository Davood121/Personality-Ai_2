"""
Advanced Search Engine - Comprehensive multi-source intelligent search system
"""
import json
import os
import re
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
from rich.console import Console
from config import *

console = Console()

class AdvancedSearchEngine:
    def __init__(self):
        self.search_history = []
        self.search_cache = {}
        self.source_reliability = {
            'wikipedia': 0.9,
            'academic': 0.95,
            'news': 0.8,
            'government': 0.9,
            'educational': 0.85,
            'technical_docs': 0.9,
            'general_web': 0.6
        }
        
        # Advanced search sources
        self.search_sources = {
            'wikipedia': {
                'base_url': 'https://en.wikipedia.org/api/rest_v1/page/summary/',
                'search_url': 'https://en.wikipedia.org/w/api.php',
                'enabled': True
            },
            'duckduckgo': {
                'base_url': 'https://duckduckgo.com/',
                'enabled': True
            },
            'arxiv': {
                'base_url': 'http://export.arxiv.org/api/query',
                'enabled': True
            },
            'github': {
                'base_url': 'https://api.github.com/search/',
                'enabled': True
            },
            'stackoverflow': {
                'base_url': 'https://api.stackexchange.com/2.3/search',
                'enabled': True
            },
            'reddit': {
                'base_url': 'https://www.reddit.com/search.json',
                'enabled': True
            },
            'news_api': {
                'base_url': 'https://newsapi.org/v2/',
                'enabled': False  # Requires API key
            }
        }
        
        self.load_search_data()
    
    def comprehensive_search(self, query: str, search_type: str = 'general') -> Dict[str, Any]:
        """Perform comprehensive multi-source search"""
        console.print(f"[yellow]🔍 Advanced search: {query}[/yellow]")
        
        # Check cache first
        cache_key = f"{query}:{search_type}"
        if cache_key in self.search_cache:
            cached_result = self.search_cache[cache_key]
            if self._is_cache_valid(cached_result):
                console.print("[dim]📋 Using cached results[/dim]")
                return cached_result
        
        search_results = {
            'query': query,
            'search_type': search_type,
            'timestamp': datetime.now().isoformat(),
            'sources': {},
            'synthesized_results': {},
            'confidence_score': 0.0,
            'total_sources': 0
        }
        
        # Search multiple sources based on type
        if search_type == 'academic':
            search_results['sources'].update(self._search_academic_sources(query))
        elif search_type == 'technical':
            search_results['sources'].update(self._search_technical_sources(query))
        elif search_type == 'news':
            search_results['sources'].update(self._search_news_sources(query))
        elif search_type == 'code':
            search_results['sources'].update(self._search_code_sources(query))
        else:
            # General comprehensive search
            search_results['sources'].update(self._search_all_sources(query))
        
        # Synthesize and analyze results
        search_results['synthesized_results'] = self._synthesize_search_results(search_results['sources'])
        search_results['confidence_score'] = self._calculate_confidence_score(search_results['sources'])
        search_results['total_sources'] = len([s for s in search_results['sources'].values() if s.get('results')])
        
        # Cache results
        self.search_cache[cache_key] = search_results
        
        # Record search
        self.search_history.append({
            'query': query,
            'type': search_type,
            'timestamp': datetime.now().isoformat(),
            'sources_found': search_results['total_sources'],
            'confidence': search_results['confidence_score']
        })
        
        console.print(f"[green]✅ Found results from {search_results['total_sources']} sources (confidence: {search_results['confidence_score']:.2f})[/green]")
        
        self.save_search_data()
        return search_results
    
    def _search_all_sources(self, query: str) -> Dict[str, Any]:
        """Search all available sources"""
        results = {}
        
        # Wikipedia search
        results['wikipedia'] = self._search_wikipedia(query)
        time.sleep(0.5)
        
        # DuckDuckGo search
        results['duckduckgo'] = self._search_duckduckgo(query)
        time.sleep(0.5)
        
        # Academic papers
        results['arxiv'] = self._search_arxiv(query)
        time.sleep(0.5)
        
        # GitHub repositories
        results['github'] = self._search_github(query)
        time.sleep(0.5)
        
        # Stack Overflow
        results['stackoverflow'] = self._search_stackoverflow(query)
        time.sleep(0.5)
        
        # Reddit discussions
        results['reddit'] = self._search_reddit(query)
        time.sleep(0.5)
        
        return results
    
    def _search_academic_sources(self, query: str) -> Dict[str, Any]:
        """Search academic and research sources"""
        results = {}
        results['arxiv'] = self._search_arxiv(query)
        results['wikipedia'] = self._search_wikipedia(query)
        return results
    
    def _search_technical_sources(self, query: str) -> Dict[str, Any]:
        """Search technical documentation and resources"""
        results = {}
        results['stackoverflow'] = self._search_stackoverflow(query)
        results['github'] = self._search_github(query)
        results['wikipedia'] = self._search_wikipedia(query)
        return results
    
    def _search_news_sources(self, query: str) -> Dict[str, Any]:
        """Search news and current events"""
        results = {}
        results['duckduckgo'] = self._search_duckduckgo(f"{query} news")
        results['reddit'] = self._search_reddit(query)
        return results
    
    def _search_code_sources(self, query: str) -> Dict[str, Any]:
        """Search code repositories and examples"""
        results = {}
        results['github'] = self._search_github(query)
        results['stackoverflow'] = self._search_stackoverflow(query)
        return results
    
    def _search_wikipedia(self, query: str) -> Dict[str, Any]:
        """Enhanced Wikipedia search"""
        try:
            # First, search for pages
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 5
            }
            
            response = requests.get(self.search_sources['wikipedia']['search_url'], 
                                  params=search_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for page in data.get('query', {}).get('search', []):
                    # Get page summary
                    summary_url = f"{self.search_sources['wikipedia']['base_url']}{page['title']}"
                    summary_response = requests.get(summary_url, timeout=10)
                    
                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        results.append({
                            'title': summary_data.get('title', ''),
                            'extract': summary_data.get('extract', ''),
                            'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            'source_type': 'encyclopedia',
                            'reliability': self.source_reliability['wikipedia']
                        })
                
                return {'results': results, 'source': 'wikipedia', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]Wikipedia search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'wikipedia', 'success': False}
    
    def _search_duckduckgo(self, query: str) -> Dict[str, Any]:
        """Enhanced DuckDuckGo search with web scraping"""
        try:
            # Use DuckDuckGo instant answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get('https://api.duckduckgo.com/', params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Abstract (main answer)
                if data.get('Abstract'):
                    results.append({
                        'title': data.get('AbstractText', 'DuckDuckGo Answer'),
                        'extract': data.get('Abstract', ''),
                        'url': data.get('AbstractURL', ''),
                        'source_type': 'web_answer',
                        'reliability': self.source_reliability['general_web']
                    })
                
                # Related topics
                for topic in data.get('RelatedTopics', [])[:3]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        results.append({
                            'title': topic.get('Text', '')[:50] + '...',
                            'extract': topic.get('Text', ''),
                            'url': topic.get('FirstURL', ''),
                            'source_type': 'related_topic',
                            'reliability': self.source_reliability['general_web']
                        })
                
                return {'results': results, 'source': 'duckduckgo', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]DuckDuckGo search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'duckduckgo', 'success': False}
    
    def _search_arxiv(self, query: str) -> Dict[str, Any]:
        """Search arXiv for academic papers"""
        try:
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': 5,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }
            
            response = requests.get(self.search_sources['arxiv']['base_url'], 
                                  params=params, timeout=15)
            
            if response.status_code == 200:
                # Parse XML response
                from xml.etree import ElementTree as ET
                root = ET.fromstring(response.content)
                
                results = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:5]:
                    title = entry.find('{http://www.w3.org/2005/Atom}title')
                    summary = entry.find('{http://www.w3.org/2005/Atom}summary')
                    link = entry.find('{http://www.w3.org/2005/Atom}id')
                    
                    if title is not None and summary is not None:
                        results.append({
                            'title': title.text.strip(),
                            'extract': summary.text.strip()[:500] + '...',
                            'url': link.text if link is not None else '',
                            'source_type': 'academic_paper',
                            'reliability': self.source_reliability['academic']
                        })
                
                return {'results': results, 'source': 'arxiv', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]arXiv search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'arxiv', 'success': False}
    
    def _search_github(self, query: str) -> Dict[str, Any]:
        """Search GitHub repositories"""
        try:
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 5
            }
            
            response = requests.get(f"{self.search_sources['github']['base_url']}repositories", 
                                  params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for repo in data.get('items', [])[:5]:
                    results.append({
                        'title': repo.get('full_name', ''),
                        'extract': repo.get('description', '') or 'No description available',
                        'url': repo.get('html_url', ''),
                        'source_type': 'code_repository',
                        'reliability': self.source_reliability['technical_docs'],
                        'stars': repo.get('stargazers_count', 0),
                        'language': repo.get('language', 'Unknown')
                    })
                
                return {'results': results, 'source': 'github', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]GitHub search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'github', 'success': False}
    
    def _search_stackoverflow(self, query: str) -> Dict[str, Any]:
        """Search Stack Overflow questions"""
        try:
            params = {
                'order': 'desc',
                'sort': 'relevance',
                'intitle': query,
                'site': 'stackoverflow',
                'pagesize': 5
            }
            
            response = requests.get(self.search_sources['stackoverflow']['base_url'], 
                                  params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', [])[:5]:
                    results.append({
                        'title': item.get('title', ''),
                        'extract': f"Score: {item.get('score', 0)}, Views: {item.get('view_count', 0)}, Answers: {item.get('answer_count', 0)}",
                        'url': item.get('link', ''),
                        'source_type': 'qa_forum',
                        'reliability': self.source_reliability['technical_docs'],
                        'score': item.get('score', 0),
                        'answered': item.get('is_answered', False)
                    })
                
                return {'results': results, 'source': 'stackoverflow', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]Stack Overflow search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'stackoverflow', 'success': False}
    
    def _search_reddit(self, query: str) -> Dict[str, Any]:
        """Search Reddit discussions"""
        try:
            params = {
                'q': query,
                'sort': 'relevance',
                'limit': 5,
                'type': 'link'
            }
            
            headers = {'User-Agent': 'AdvancedSearchBot/1.0'}
            response = requests.get(self.search_sources['reddit']['base_url'], 
                                  params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for post in data.get('data', {}).get('children', [])[:5]:
                    post_data = post.get('data', {})
                    results.append({
                        'title': post_data.get('title', ''),
                        'extract': post_data.get('selftext', '')[:300] + '...' if post_data.get('selftext') else 'Discussion thread',
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'source_type': 'discussion_forum',
                        'reliability': self.source_reliability['general_web'],
                        'score': post_data.get('score', 0),
                        'subreddit': post_data.get('subreddit', '')
                    })
                
                return {'results': results, 'source': 'reddit', 'success': True}
        
        except Exception as e:
            console.print(f"[dim red]Reddit search failed: {e}[/dim red]")
        
        return {'results': [], 'source': 'reddit', 'success': False}
    
    def _synthesize_search_results(self, sources: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple sources"""
        synthesis = {
            'key_concepts': [],
            'definitions': [],
            'technical_details': [],
            'discussions': [],
            'code_examples': [],
            'academic_insights': [],
            'source_summary': {}
        }
        
        for source_name, source_data in sources.items():
            if not source_data.get('success') or not source_data.get('results'):
                continue
            
            source_count = len(source_data['results'])
            synthesis['source_summary'][source_name] = source_count
            
            for result in source_data['results']:
                source_type = result.get('source_type', 'general')
                
                if source_type in ['encyclopedia', 'web_answer']:
                    synthesis['definitions'].append({
                        'text': result.get('extract', ''),
                        'source': source_name,
                        'reliability': result.get('reliability', 0.5)
                    })
                elif source_type == 'academic_paper':
                    synthesis['academic_insights'].append({
                        'title': result.get('title', ''),
                        'text': result.get('extract', ''),
                        'source': source_name,
                        'reliability': result.get('reliability', 0.5)
                    })
                elif source_type == 'code_repository':
                    synthesis['code_examples'].append({
                        'title': result.get('title', ''),
                        'description': result.get('extract', ''),
                        'language': result.get('language', 'Unknown'),
                        'stars': result.get('stars', 0),
                        'url': result.get('url', '')
                    })
                elif source_type in ['discussion_forum', 'qa_forum']:
                    synthesis['discussions'].append({
                        'title': result.get('title', ''),
                        'text': result.get('extract', ''),
                        'score': result.get('score', 0),
                        'source': source_name
                    })
        
        return synthesis
    
    def _calculate_confidence_score(self, sources: Dict[str, Any]) -> float:
        """Calculate confidence score based on source quality and quantity"""
        total_score = 0.0
        total_weight = 0.0
        
        for source_name, source_data in sources.items():
            if not source_data.get('success'):
                continue
            
            source_reliability = self.source_reliability.get(
                self._get_source_category(source_name), 0.5
            )
            
            result_count = len(source_data.get('results', []))
            weight = source_reliability * result_count
            
            total_score += weight
            total_weight += result_count
        
        return min(total_score / max(total_weight, 1), 1.0)
    
    def _get_source_category(self, source_name: str) -> str:
        """Get reliability category for source"""
        categories = {
            'wikipedia': 'wikipedia',
            'arxiv': 'academic',
            'github': 'technical_docs',
            'stackoverflow': 'technical_docs',
            'duckduckgo': 'general_web',
            'reddit': 'general_web'
        }
        return categories.get(source_name, 'general_web')
    
    def _is_cache_valid(self, cached_result: Dict[str, Any]) -> bool:
        """Check if cached result is still valid"""
        try:
            cache_time = datetime.fromisoformat(cached_result['timestamp'])
            age_hours = (datetime.now() - cache_time).total_seconds() / 3600
            return age_hours < 24  # Cache valid for 24 hours
        except:
            return False
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        return {
            'total_searches': len(self.search_history),
            'cache_size': len(self.search_cache),
            'average_confidence': sum(s.get('confidence', 0) for s in self.search_history) / max(len(self.search_history), 1),
            'source_usage': {source: sum(1 for s in self.search_history if s.get('sources_found', 0) > 0) for source in self.search_sources.keys()},
            'recent_searches': self.search_history[-5:] if self.search_history else []
        }
    
    def load_search_data(self):
        """Load search engine data"""
        try:
            search_file = "memory/advanced_search.json"
            if os.path.exists(search_file):
                with open(search_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.search_history = data.get('search_history', [])
                    # Don't load cache - let it rebuild fresh
        except Exception as e:
            console.print(f"[dim yellow]Warning: Could not load search data: {e}[/dim yellow]")
    
    def save_search_data(self):
        """Save search engine data"""
        try:
            os.makedirs(MEMORY_DIR, exist_ok=True)
            search_file = "memory/advanced_search.json"
            
            data = {
                'search_history': self.search_history[-100:],  # Keep last 100 searches
                'last_updated': datetime.now().isoformat()
            }
            
            with open(search_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[dim red]Error saving search data: {e}[/dim red]")
