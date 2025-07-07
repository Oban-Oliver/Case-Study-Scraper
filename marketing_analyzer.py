#!/usr/bin/env python3
"""
Marketing Metrics Analyzer
Scrapes URLs and analyzes marketing content using OpenAI GPT-4o-mini
"""

import requests
import re
import json
import os
from typing import Dict, List, Tuple
from openai import OpenAI

class MarketingAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the analyzer with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Define jargon terms for AI/ML
        self.jargon_terms = [
            'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
            'algorithm', 'automation', 'predictive', 'optimization', 'analytics',
            'data science', 'big data', 'AI-powered', 'ML-driven', 'intelligent',
            'cognitive', 'NLP', 'computer vision', 'reinforcement learning',
            'supervised learning', 'unsupervised learning', 'model training',
            'feature engineering', 'data mining', 'pattern recognition'
        ]
        
        # Define vague/buzzword terms
        self.vague_terms = [
            'innovative', 'cutting-edge', 'revolutionary', 'game-changing',
            'breakthrough', 'next-generation', 'state-of-the-art', 'world-class',
            'industry-leading', 'best-in-class', 'synergy', 'leverage',
            'scalable', 'robust', 'seamless', 'holistic', 'strategic',
            'transformative', 'disruptive', 'paradigm', 'ecosystem'
        ]
        
        # Action verbs for process clarity
        self.action_verbs = [
            'analyze', 'build', 'create', 'develop', 'implement', 'execute',
            'generate', 'process', 'optimize', 'automate', 'integrate',
            'deploy', 'configure', 'customize', 'train', 'validate',
            'test', 'monitor', 'evaluate', 'measure', 'track'
        ]

    def scrape_url(self, url: str) -> str:
        """Scrape content from URL and extract text"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Check for bot detection indicators
            html_content = response.text
            bot_indicators = [
                'access denied', 'blocked', 'forbidden', 'captcha', 'cloudflare',
                'bot detected', 'please verify', 'security check', 'rate limit',
                'too many requests', 'suspicious activity', 'anti-bot'
            ]
            
            html_lower = html_content.lower()
            for indicator in bot_indicators:
                if indicator in html_lower:
                    raise Exception(f"🚫 BOT RESTRICTION DETECTED: The website appears to be blocking automated access. Found '{indicator}' in response.")
            
            # Remove script and style elements
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Remove HTML tags
            text_content = re.sub(r'<[^>]+>', '', html_content)
            
            # Clean up whitespace
            text_content = re.sub(r'\s+', ' ', text_content)
            text_content = text_content.strip()
            
            # Check if we got meaningful content
            if len(text_content) < 100:
                raise Exception(f"🚫 POSSIBLE BOT RESTRICTION: Very little content extracted ({len(text_content)} characters). The site may be blocking automated access.")
            
            # Check for common bot-blocking page patterns
            if len(text_content) < 500 and any(word in text_content.lower() for word in ['javascript', 'enable', 'browser', 'verify']):
                raise Exception(f"🚫 BOT RESTRICTION LIKELY: Page seems to require JavaScript or manual verification. Content: {text_content[:200]}...")
            
            return text_content
            
        except requests.RequestException as e:
            if "403" in str(e):
                raise Exception(f"🚫 BOT RESTRICTION: 403 Forbidden - The website is blocking automated access.")
            elif "429" in str(e):
                raise Exception(f"🚫 RATE LIMITED: 429 Too Many Requests - The website is rate limiting requests.")
            else:
                raise Exception(f"Failed to scrape URL: {str(e)}")

    def count_words(self, text: str) -> int:
        """Count words in text"""
        return len(re.findall(r'\b\w+\b', text.lower()))

    def calculate_jargon_density(self, text: str) -> float:
        """Calculate jargon density (AI/ML terms per 500 words)"""
        text_lower = text.lower()
        jargon_count = 0
        
        for term in self.jargon_terms:
            jargon_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
        
        word_count = self.count_words(text)
        return (jargon_count / word_count) * 500 if word_count > 0 else 0

    def calculate_process_clarity(self, text: str) -> float:
        """Calculate process clarity (action verb percentage)"""
        text_lower = text.lower()
        action_verb_count = 0
        
        for verb in self.action_verbs:
            action_verb_count += len(re.findall(r'\b' + re.escape(verb) + r'\b', text_lower))
        
        word_count = self.count_words(text)
        return (action_verb_count / word_count) * 100 if word_count > 0 else 0

    def calculate_vague_terms(self, text: str) -> float:
        """Calculate vague terms count (buzzwords per 1000 words)"""
        text_lower = text.lower()
        vague_count = 0
        
        for term in self.vague_terms:
            vague_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
        
        word_count = self.count_words(text)
        return (vague_count / word_count) * 1000 if word_count > 0 else 0

    def calculate_statistics_usage(self, text: str) -> int:
        """Calculate statistics usage (quantitative data sentences)"""
        # Look for numbers, percentages, and statistical terms
        stat_patterns = [
            r'\b\d+%\b',  # percentages
            r'\b\d+\.\d+%\b',  # decimal percentages
            r'\b\d+x\b',  # multipliers
            r'\b\d+\s*(times|fold)\b',  # fold increases
            r'\b\d+\s*(million|billion|thousand)\b',  # large numbers
            r'\b\d+\s*(percent|percentage)\b',  # percent spelled out
            r'\b(increase|decrease|improve|reduction)\s+of\s+\d+\b',  # improvements
        ]
        
        stat_count = 0
        for pattern in stat_patterns:
            stat_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        return stat_count

    def calculate_future_past_ratio(self, text: str) -> float:
        """Calculate future vs past focus ratio"""
        future_terms = ['will', 'shall', 'going to', 'future', 'upcoming', 'next', 'tomorrow', 'plan', 'intend']
        past_terms = ['was', 'were', 'had', 'did', 'previous', 'last', 'ago', 'before', 'earlier', 'historical']
        
        text_lower = text.lower()
        
        future_count = 0
        for term in future_terms:
            future_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
        
        past_count = 0
        for term in past_terms:
            past_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text_lower))
        
        return future_count / past_count if past_count > 0 else future_count

    def get_openai_analysis(self, text: str) -> Dict:
        """Get enhanced analysis from OpenAI GPT-4o-mini"""
        prompt = f"""
        Analyze the following marketing content and provide a JSON response with these metrics:

        1. readability_score (1-10): How easy is it to understand?
        2. persuasiveness_score (1-10): How persuasive is the content?
        3. credibility_score (1-10): How credible does it sound?
        4. engagement_score (1-10): How engaging is the content?
        5. call_to_action_strength (1-10): How strong are the calls to action?
        6. key_themes (list): Top 3-5 main themes
        7. tone_analysis (string): Overall tone (professional, casual, technical, etc.)
        8. target_audience (string): Who is the intended audience?

        Content to analyze:
        {text[:3000]}...

        Respond with valid JSON only.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing content analyst. Provide accurate, objective analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "Could not parse JSON from OpenAI response"}
                
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

    def calculate_marketing_effectiveness_score(self, metrics: Dict) -> float:
        """Calculate overall marketing effectiveness score (0-100)"""
        # Weights for different metrics
        weights = {
            'jargon_density': -0.5,  # Too much jargon is bad
            'process_clarity': 1.0,  # Good process clarity is good
            'vague_terms': -0.3,  # Too many vague terms is bad
            'statistics_usage': 0.8,  # Statistics add credibility
            'future_past_ratio': 0.2,  # Slight preference for future focus
        }
        
        score = 50  # Base score
        
        # Apply basic metrics
        score += min(metrics['process_clarity'], 10) * weights['process_clarity']
        score += min(metrics['jargon_density'], 20) * weights['jargon_density']
        score += min(metrics['vague_terms'], 15) * weights['vague_terms']
        score += min(metrics['statistics_usage'], 10) * weights['statistics_usage']
        score += min(metrics['future_past_ratio'], 5) * weights['future_past_ratio']
        
        # Apply OpenAI metrics if available
        if 'openai_analysis' in metrics and 'error' not in metrics['openai_analysis']:
            openai_metrics = metrics['openai_analysis']
            score += openai_metrics.get('readability_score', 5) * 2
            score += openai_metrics.get('persuasiveness_score', 5) * 2.5
            score += openai_metrics.get('credibility_score', 5) * 2
            score += openai_metrics.get('engagement_score', 5) * 1.5
            score += openai_metrics.get('call_to_action_strength', 5) * 1.5
        
        return max(0, min(100, score))

    def analyze_url(self, url: str) -> Dict:
        """Analyze a URL and return comprehensive metrics"""
        print(f"Scraping URL: {url}")
        text = self.scrape_url(url)
        
        print(f"Extracted {len(text)} characters, {self.count_words(text)} words")
        
        print("Calculating basic metrics...")
        metrics = {
            'url': url,
            'word_count': self.count_words(text),
            'character_count': len(text),
            'jargon_density': self.calculate_jargon_density(text),
            'process_clarity': self.calculate_process_clarity(text),
            'vague_terms': self.calculate_vague_terms(text),
            'statistics_usage': self.calculate_statistics_usage(text),
            'future_past_ratio': self.calculate_future_past_ratio(text),
        }
        
        print("Getting OpenAI analysis...")
        metrics['openai_analysis'] = self.get_openai_analysis(text)
        
        print("Calculating marketing effectiveness score...")
        metrics['marketing_effectiveness_score'] = self.calculate_marketing_effectiveness_score(metrics)
        
        return metrics

    def print_analysis(self, metrics: Dict):
        """Print formatted analysis results"""
        print("\n" + "="*60)
        print("MARKETING METRICS ANALYSIS")
        print("="*60)
        print(f"URL: {metrics['url']}")
        print(f"Word Count: {metrics['word_count']:,}")
        print(f"Character Count: {metrics['character_count']:,}")
        print()
        
        print("BASIC METRICS:")
        print(f"  Jargon Density: {metrics['jargon_density']:.2f} AI/ML terms per 500 words")
        print(f"  Process Clarity: {metrics['process_clarity']:.2f}% action verbs")
        print(f"  Vague Terms: {metrics['vague_terms']:.2f} buzzwords per 1000 words")
        print(f"  Statistics Usage: {metrics['statistics_usage']} quantitative data points")
        print(f"  Future/Past Ratio: {metrics['future_past_ratio']:.2f}")
        print()
        
        if 'error' not in metrics['openai_analysis']:
            openai = metrics['openai_analysis']
            print("OPENAI ANALYSIS:")
            print(f"  Readability Score: {openai.get('readability_score', 'N/A')}/10")
            print(f"  Persuasiveness Score: {openai.get('persuasiveness_score', 'N/A')}/10")
            print(f"  Credibility Score: {openai.get('credibility_score', 'N/A')}/10")
            print(f"  Engagement Score: {openai.get('engagement_score', 'N/A')}/10")
            print(f"  Call-to-Action Strength: {openai.get('call_to_action_strength', 'N/A')}/10")
            print(f"  Tone: {openai.get('tone_analysis', 'N/A')}")
            print(f"  Target Audience: {openai.get('target_audience', 'N/A')}")
            if 'key_themes' in openai:
                print(f"  Key Themes: {', '.join(openai['key_themes'])}")
        else:
            print("OPENAI ANALYSIS:")
            print(f"  Error: {metrics['openai_analysis']['error']}")
        
        print()
        print(f"MARKETING EFFECTIVENESS SCORE: {metrics['marketing_effectiveness_score']:.1f}/100")
        
        # Score interpretation
        score = metrics['marketing_effectiveness_score']
        if score >= 80:
            interpretation = "Excellent - Highly effective marketing content"
        elif score >= 65:
            interpretation = "Good - Effective with room for improvement"
        elif score >= 50:
            interpretation = "Average - Needs significant improvement"
        elif score >= 35:
            interpretation = "Below Average - Major issues to address"
        else:
            interpretation = "Poor - Requires complete overhaul"
        
        print(f"Interpretation: {interpretation}")
        print("="*60)


def main():
    """Main function to run the analyzer"""
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OpenAI API key not found!")
        print("Please set the OPENAI_API_KEY environment variable.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Test URL
    test_url = "https://tomoro.ai/insights/practical-examples-of-customised-rag-solutions"
    
    try:
        analyzer = MarketingAnalyzer(api_key)
        metrics = analyzer.analyze_url(test_url)
        analyzer.print_analysis(metrics)
        
        # Save results to JSON file
        with open('marketing_analysis_results.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"\nResults saved to: marketing_analysis_results.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()