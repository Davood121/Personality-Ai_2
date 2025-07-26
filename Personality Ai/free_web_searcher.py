"""
Free Web Search Module - No API keys required!
Uses free sources like Wikipedia, DuckDuckGo, and direct web scraping
"""
import requests
import time
import json
import random
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import wikipedia
from urllib.parse import urljoin, urlparse, quote
from config import *
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class FreeWebSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.search_history = []
        
    def search_duckduckgo(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search DuckDuckGo (free, no API key needed)"""
        try:
            console.print(f"🦆 Searching DuckDuckGo for: [cyan]{query}[/cyan]")
            
            # DuckDuckGo instant answer API (free)
            ddg_url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            
            response = self.session.get(ddg_url, timeout=TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Get abstract if available
            if data.get('Abstract'):
                results.append({
                    'url': data.get('AbstractURL', ''),
                    'title': data.get('Heading', query),
                    'content': data.get('Abstract', ''),
                    'source': 'duckduckgo'
                })
            
            # Get related topics
            for topic in data.get('RelatedTopics', [])[:3]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'url': topic.get('FirstURL', ''),
                        'title': topic.get('Text', '')[:100],
                        'content': topic.get('Text', ''),
                        'source': 'duckduckgo'
                    })
            
            return results
            
        except Exception as e:
            console.print(f"[yellow]DuckDuckGo search error: {e}[/yellow]")
            return []
            
    def search_wikipedia_advanced(self, query: str) -> List[Dict[str, str]]:
        """Enhanced Wikipedia search with multiple strategies"""
        try:
            console.print(f"📚 Searching Wikipedia for: [cyan]{query}[/cyan]")
            
            results = []
            
            # Strategy 1: Direct search
            try:
                search_results = wikipedia.search(query, results=5)
                
                for title in search_results[:3]:
                    try:
                        page = wikipedia.page(title)
                        results.append({
                            'url': page.url,
                            'title': page.title,
                            'content': page.summary[:1500],  # More content
                            'source': 'wikipedia'
                        })
                        time.sleep(0.5)  # Be respectful
                    except wikipedia.exceptions.DisambiguationError as e:
                        # Try first disambiguation option
                        try:
                            page = wikipedia.page(e.options[0])
                            results.append({
                                'url': page.url,
                                'title': page.title,
                                'content': page.summary[:1500],
                                'source': 'wikipedia'
                            })
                        except:
                            continue
                    except:
                        continue
                        
            except Exception as e:
                console.print(f"[yellow]Wikipedia search error: {e}[/yellow]")
            
            # Strategy 2: Search for related terms
            related_terms = self._generate_related_terms(query)
            for term in related_terms[:2]:
                try:
                    search_results = wikipedia.search(term, results=2)
                    if search_results:
                        page = wikipedia.page(search_results[0])
                        results.append({
                            'url': page.url,
                            'title': page.title,
                            'content': page.summary[:1000],
                            'source': 'wikipedia'
                        })
                        time.sleep(0.5)
                except:
                    continue
                    
            return results
            
        except Exception as e:
            console.print(f"[red]Wikipedia advanced search error: {e}[/red]")
            return []
            
    def _generate_related_terms(self, query: str) -> List[str]:
        """Generate related search terms"""
        base_terms = query.lower().split()
        
        # Psychology-related expansions
        psychology_terms = {
            'personality': ['personality psychology', 'personality traits', 'personality theory'],
            'behavior': ['human behavior', 'behavioral psychology', 'behavior patterns'],
            'emotion': ['emotional psychology', 'emotions and behavior', 'emotional intelligence'],
            'social': ['social psychology', 'social behavior', 'social interaction'],
            'cognitive': ['cognitive psychology', 'cognitive behavior', 'cognitive science'],
            'development': ['developmental psychology', 'human development', 'psychological development']
        }
        
        related = []
        for term in base_terms:
            if term in psychology_terms:
                related.extend(psychology_terms[term])
                
        # Add general psychology terms
        if not related:
            related = [f"{query} psychology", f"{query} theory", f"{query} research"]
            
        return related[:3]
        
    def scrape_psychology_websites(self, query: str) -> List[Dict[str, str]]:
        """Scrape free psychology websites"""
        try:
            console.print(f"🌐 Scraping psychology websites for: [cyan]{query}[/cyan]")
            
            results = []
            
            # Psychology Today search
            try:
                pt_url = f"https://www.psychologytoday.com/us/basics/{query.replace(' ', '-').lower()}"
                response = self.session.get(pt_url, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract main content
                    content_div = soup.find('div', class_='content') or soup.find('article')
                    if content_div:
                        text = content_div.get_text().strip()[:1000]
                        if len(text) > 100:
                            results.append({
                                'url': pt_url,
                                'title': f"Psychology Today: {query}",
                                'content': text,
                                'source': 'psychology_today'
                            })
                            
                time.sleep(2)  # Be respectful
                
            except Exception as e:
                console.print(f"[yellow]Psychology Today scraping failed: {e}[/yellow]")
            
            # Simply Psychology search
            try:
                sp_query = query.replace(' ', '-').lower()
                sp_url = f"https://www.simplypsychology.org/{sp_query}.html"
                response = self.session.get(sp_url, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract main content
                    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                    if main_content:
                        # Remove navigation and ads
                        for unwanted in main_content.find_all(['nav', 'aside', 'footer']):
                            unwanted.decompose()
                            
                        text = main_content.get_text().strip()[:1000]
                        if len(text) > 100:
                            results.append({
                                'url': sp_url,
                                'title': f"Simply Psychology: {query}",
                                'content': text,
                                'source': 'simply_psychology'
                            })
                            
                time.sleep(2)  # Be respectful
                
            except Exception as e:
                console.print(f"[yellow]Simply Psychology scraping failed: {e}[/yellow]")
                
            return results
            
        except Exception as e:
            console.print(f"[red]Website scraping error: {e}[/red]")
            return []
            
    def search_free_sources(self, query: str) -> List[Dict[str, str]]:
        """Search all free sources"""
        all_results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Search Wikipedia (always free)
            task1 = progress.add_task("Searching Wikipedia...", total=None)
            wiki_results = self.search_wikipedia_advanced(query)
            all_results.extend(wiki_results)
            progress.remove_task(task1)
            
            # Search DuckDuckGo (free)
            task2 = progress.add_task("Searching DuckDuckGo...", total=None)
            ddg_results = self.search_duckduckgo(query)
            all_results.extend(ddg_results)
            progress.remove_task(task2)
            
            # Scrape psychology websites (free)
            if not USE_WIKIPEDIA_ONLY:
                task3 = progress.add_task("Scraping psychology sites...", total=None)
                web_results = self.scrape_psychology_websites(query)
                all_results.extend(web_results)
                progress.remove_task(task3)
        
        # Record search in history
        self.search_history.append({
            'query': query,
            'timestamp': time.time(),
            'results_count': len(all_results),
            'sources_used': 'free_only'
        })
        
        console.print(f"✅ Found {len(all_results)} results for: [green]{query}[/green] (FREE)")
        return all_results
        
    def extract_key_information(self, search_results: List[Dict[str, str]], topic: str) -> Dict[str, Any]:
        """Extract and organize key information from search results"""
        key_info = {
            'topic': topic,
            'definitions': [],
            'key_concepts': [],
            'examples': [],
            'interesting_facts': [],
            'sources': [],
            'timestamp': time.time(),
            'search_method': 'free_sources'
        }
        
        for result in search_results:
            content = result.get('content', '').lower()
            title = result.get('title', '')
            
            # Extract definitions (sentences with "is", "are", "means", "refers to")
            sentences = content.split('.')
            for sentence in sentences:
                if any(word in sentence for word in ['is', 'are', 'means', 'refers to', 'defined as']):
                    if len(sentence.strip()) > 20 and len(sentence.strip()) < 300:
                        key_info['definitions'].append(sentence.strip())
                        
            # Extract key concepts (capitalized words, technical terms)
            words = content.split()
            for i, word in enumerate(words):
                if word.istitle() and len(word) > 3:
                    context = ' '.join(words[max(0, i-2):i+3])
                    if len(context) > 10:
                        key_info['key_concepts'].append(context)
                        
            # Look for examples
            for sentence in sentences:
                if any(word in sentence for word in ['example', 'for instance', 'such as', 'including']):
                    if len(sentence.strip()) > 20:
                        key_info['examples'].append(sentence.strip())
                        
            # Collect interesting facts (sentences with numbers, percentages, studies)
            for sentence in sentences:
                if any(indicator in sentence for indicator in ['%', 'study', 'research', 'found that', 'discovered']):
                    if len(sentence.strip()) > 30:
                        key_info['interesting_facts'].append(sentence.strip())
                        
            # Record source
            key_info['sources'].append({
                'title': title,
                'url': result.get('url', ''),
                'source_type': result.get('source', 'unknown'),
                'is_free': True
            })
            
        # Remove duplicates and limit results
        key_info['definitions'] = list(set(key_info['definitions']))[:5]
        key_info['key_concepts'] = list(set(key_info['key_concepts']))[:10]
        key_info['examples'] = list(set(key_info['examples']))[:5]
        key_info['interesting_facts'] = list(set(key_info['interesting_facts']))[:5]
        
        return key_info
        
    def get_offline_knowledge(self, topic: str) -> Dict[str, Any]:
        """Get pre-loaded offline knowledge for completely free operation"""
        offline_knowledge = {
            'personality': {
                'definitions': [
                    'Personality refers to individual differences in characteristic patterns of thinking, feeling and behaving.',
                    'Personality psychology is the study of individual differences in behavior, cognition, and emotion.'
                ],
                'key_concepts': ['Big Five traits', 'personality development', 'individual differences', 'behavioral patterns'],
                'interesting_facts': [
                    'The Big Five personality traits are openness, conscientiousness, extraversion, agreeableness, and neuroticism.',
                    'Personality traits are relatively stable across the lifespan but can change gradually.'
                ],
                'examples': ['Extraverts tend to be more social and outgoing', 'Conscientious people are typically organized and disciplined']
            },
            'behavior': {
                'definitions': [
                    'Human behavior refers to the range of actions and mannerisms made by individuals, families, groups and species.',
                    'Behavior is influenced by genetics, environment, thoughts, emotions, and social context.'
                ],
                'key_concepts': ['behavioral psychology', 'conditioning', 'social learning', 'motivation'],
                'interesting_facts': [
                    'Human behavior is approximately 50% influenced by genetics and 50% by environment.',
                    'Social learning theory suggests we learn behaviors by observing others.'
                ],
                'examples': ['Classical conditioning in learning', 'Social modeling in children']
            },
            'psychology': {
                'definitions': [
                    'Psychology is the scientific study of mind and behavior.',
                    'Psychology encompasses the study of conscious and unconscious phenomena, feelings and thoughts.'
                ],
                'key_concepts': ['cognitive psychology', 'behavioral psychology', 'social psychology', 'developmental psychology'],
                'interesting_facts': [
                    'Psychology became a scientific discipline in the late 19th century.',
                    'There are over 50 different subfields within psychology.'
                ],
                'examples': ['Cognitive behavioral therapy', 'Psychological assessment and testing']
            }
        }
        
        topic_lower = topic.lower()
        for key, data in offline_knowledge.items():
            if key in topic_lower or topic_lower in key:
                return {
                    'topic': topic,
                    'definitions': data['definitions'],
                    'key_concepts': data['key_concepts'],
                    'examples': data['examples'],
                    'interesting_facts': data['interesting_facts'],
                    'sources': [{'title': 'Offline Knowledge Base', 'url': 'local', 'source_type': 'offline', 'is_free': True}],
                    'timestamp': time.time(),
                    'search_method': 'offline'
                }
        
        # Default response for unknown topics
        return {
            'topic': topic,
            'definitions': [f'{topic} is an important concept in psychology and human behavior.'],
            'key_concepts': [topic, 'psychology', 'human behavior'],
            'examples': [f'Examples of {topic} can be found in everyday life.'],
            'interesting_facts': [f'{topic} is studied by researchers to better understand human nature.'],
            'sources': [{'title': 'General Knowledge', 'url': 'local', 'source_type': 'offline', 'is_free': True}],
            'timestamp': time.time(),
            'search_method': 'offline'
        }
        
    def comprehensive_search(self, query: str) -> List[Dict[str, str]]:
        """Main search method that uses only free sources"""
        if ENABLE_OFFLINE_MODE:
            # Offline mode - use pre-loaded knowledge
            console.print(f"📚 Using offline knowledge for: [cyan]{query}[/cyan]")
            offline_info = self.get_offline_knowledge(query)
            return [{
                'url': 'offline',
                'title': f"Offline Knowledge: {query}",
                'content': str(offline_info),
                'source': 'offline'
            }]
        else:
            # Online free search
            return self.search_free_sources(query)
            
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics"""
        free_searches = len([s for s in self.search_history if s.get('sources_used') == 'free_only'])
        
        return {
            'total_searches': len(self.search_history),
            'free_searches': free_searches,
            'recent_searches': self.search_history[-5:] if self.search_history else [],
            'average_results_per_search': sum(s['results_count'] for s in self.search_history) / len(self.search_history) if self.search_history else 0,
            'cost': 0.0  # Always free!
        }
