"""
SEO and Accessibility Analysis Modules
"""

from collections import Counter


class SEOAnalyzer:
    """Analyzes SEO issues in crawled pages"""
    
    def analyze(self, crawl_results):
        """Run SEO analysis on crawled pages"""
        issues = []
        pages = crawl_results['pages']
        
        for page in pages:
            url = page['url']
            
            # Check title
            if not page.get('title'):
                issues.append({
                    'url': url,
                    'type': 'missing_title',
                    'severity': 'high',
                    'message': 'Missing page title'
                })
            elif len(page['title']) < 30:
                issues.append({
                    'url': url,
                    'type': 'short_title',
                    'severity': 'medium',
                    'message': f'Title too short ({len(page["title"])} chars, recommended 50-60)'
                })
            elif len(page['title']) > 60:
                issues.append({
                    'url': url,
                    'type': 'long_title',
                    'severity': 'low',
                    'message': f'Title too long ({len(page["title"])} chars, recommended 50-60)'
                })
            
            # Check meta description
            if not page.get('description'):
                issues.append({
                    'url': url,
                    'type': 'missing_description',
                    'severity': 'high',
                    'message': 'Missing meta description'
                })
            elif len(page['description']) < 120:
                issues.append({
                    'url': url,
                    'type': 'short_description',
                    'severity': 'medium',
                    'message': f'Description too short ({len(page["description"])} chars, recommended 150-160)'
                })
            
            # Check H1 headings
            h1_count = len(page['headings']['h1'])
            if h1_count == 0:
                issues.append({
                    'url': url,
                    'type': 'missing_h1',
                    'severity': 'high',
                    'message': 'Missing H1 heading'
                })
            elif h1_count > 1:
                issues.append({
                    'url': url,
                    'type': 'multiple_h1',
                    'severity': 'medium',
                    'message': f'Multiple H1 headings found ({h1_count})'
                })
            
            # Check heading hierarchy
            if len(page['headings']['h2']) == 0 and len(page['headings']['h3']) > 0:
                issues.append({
                    'url': url,
                    'type': 'heading_hierarchy',
                    'severity': 'low',
                    'message': 'H3 used without H2'
                })
            
            # Check content length
            if page.get('word_count', 0) < 300:
                issues.append({
                    'url': url,
                    'type': 'thin_content',
                    'severity': 'medium',
                    'message': f'Thin content ({page.get("word_count", 0)} words, recommended 300+)'
                })
        
        # Analyze site-wide issues
        all_titles = [p.get('title', '') for p in pages]
        duplicate_titles = [title for title, count in Counter(all_titles).items() if count > 1 and title]
        
        for title in duplicate_titles:
            duplicate_urls = [p['url'] for p in pages if p.get('title') == title]
            issues.append({
                'url': 'site-wide',
                'type': 'duplicate_titles',
                'severity': 'high',
                'message': f'Duplicate title "{title}" on {len(duplicate_urls)} pages',
                'affected_urls': duplicate_urls
            })
        
        return {
            'issues': issues,
            'total_issues': len(issues),
            'by_severity': {
                'high': len([i for i in issues if i['severity'] == 'high']),
                'medium': len([i for i in issues if i['severity'] == 'medium']),
                'low': len([i for i in issues if i['severity'] == 'low'])
            }
        }


class AccessibilityAnalyzer:
    """Analyzes accessibility issues in crawled pages"""
    
    def analyze(self, crawl_results):
        """Run accessibility analysis on crawled pages"""
        issues = []
        pages = crawl_results['pages']
        
        for page in pages:
            url = page['url']
            
            # Check images for alt text
            if 'images' in page:
                images_without_alt = [img for img in page['images'] if not img['has_alt']]
                if images_without_alt:
                    issues.append({
                        'url': url,
                        'type': 'missing_alt_text',
                        'severity': 'high',
                        'message': f'{len(images_without_alt)} image(s) missing alt text',
                        'count': len(images_without_alt)
                    })
            
            # Check for empty links
            if 'links' in page:
                empty_links = [l for l in page['links'] if not l['text'].strip()]
                if empty_links:
                    issues.append({
                        'url': url,
                        'type': 'empty_links',
                        'severity': 'medium',
                        'message': f'{len(empty_links)} link(s) with no text',
                        'count': len(empty_links)
                    })
            
            # Check heading structure
            if page['headings']['h1'] and not page['headings']['h1'][0]:
                issues.append({
                    'url': url,
                    'type': 'empty_h1',
                    'severity': 'high',
                    'message': 'H1 heading is empty'
                })
        
        return {
            'issues': issues,
            'total_issues': len(issues),
            'by_severity': {
                'high': len([i for i in issues if i['severity'] == 'high']),
                'medium': len([i for i in issues if i['severity'] == 'medium']),
                'low': len([i for i in issues if i['severity'] == 'low'])
            }
        }
