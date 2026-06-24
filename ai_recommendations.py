"""
AI Recommendation Engine
Generates personalized improvement recommendations using OpenAI
"""

import os
import json
from openai import OpenAI


class AIRecommendationEngine:
    """Generates AI-powered recommendations for website improvements"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def _format_issues_summary(self, seo_results, a11y_results):
        """Format issues into a summary for the AI"""
        summary = {
            'seo': {
                'total': seo_results['total_issues'],
                'high_severity': seo_results['by_severity']['high'],
                'medium_severity': seo_results['by_severity']['medium'],
                'low_severity': seo_results['by_severity']['low'],
                'issue_types': list(set(i['type'] for i in seo_results['issues']))
            },
            'accessibility': {
                'total': a11y_results['total_issues'],
                'high_severity': a11y_results['by_severity']['high'],
                'medium_severity': a11y_results['by_severity']['medium'],
                'low_severity': a11y_results['by_severity']['low'],
                'issue_types': list(set(i['type'] for i in a11y_results['issues']))
            }
        }
        return json.dumps(summary, indent=2)
    
    def generate(self, url, seo_results, a11y_results, crawl_results):
        """Generate AI recommendations based on audit results"""
        
        issues_summary = self._format_issues_summary(seo_results, a11y_results)
        
        # Get a sample page for context
        sample_page = crawl_results['pages'][0] if crawl_results['pages'] else {}
        
        prompt = f"""You are an expert web consultant analyzing a website audit for {url}.

Audit Summary:
{issues_summary}

Sample Page Data:
- Title: {sample_page.get('title', 'N/A')}
- Description: {sample_page.get('description', 'N/A')}
- H1 Count: {len(sample_page.get('headings', {}).get('h1', []))}
- Word Count: {sample_page.get('word_count', 0)}

Based on this audit, provide:
1. Top 3 priority fixes (most impactful for SEO and user experience)
2. Quick wins (easy improvements with good ROI)
3. Long-term recommendations for ongoing improvement

Keep your response concise, actionable, and focused on business impact.
Format as JSON with keys: priority_fixes (array), quick_wins (array), long_term (array).
Each item should have: title, description, impact (high/medium/low)."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a web optimization expert providing actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            
            recommendations = json.loads(content)
            return recommendations
            
        except json.JSONDecodeError:
            # Fallback to raw text if JSON parsing fails
            return {
                'raw_text': content,
                'priority_fixes': [],
                'quick_wins': [],
                'long_term': []
            }
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
