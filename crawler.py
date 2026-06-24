"""
Website Crawler Module
Crawls websites and extracts content for analysis
"""

from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


class WebsiteCrawler:
    """Crawls websites and extracts page content"""
    
    def __init__(self, max_pages=5, timeout=30000):
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited = set()
        self.pages_data = []
    
    def _is_same_domain(self, url, base_url):
        """Check if URL belongs to the same domain"""
        return urlparse(url).netloc == urlparse(base_url).netloc
    
    def _normalize_url(self, url):
        """Remove fragments and trailing slashes"""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return normalized.rstrip('/')
    
    def _extract_page_data(self, page, url):
        """Extract relevant data from a page"""
        try:
            content = page.content()
            soup = BeautifulSoup(content, 'lxml')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=' ', strip=True)
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.string if title else ''
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''
            
            # Extract headings
            headings = {
                'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
                'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
                'h3': [h.get_text(strip=True) for h in soup.find_all('h3')],
            }
            
            # Extract images
            images = []
            for img in soup.find_all('img'):
                images.append({
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'has_alt': bool(img.get('alt'))
                })
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                links.append({
                    'url': absolute_url,
                    'text': link.get_text(strip=True),
                    'internal': self._is_same_domain(absolute_url, url)
                })
            
            return {
                'url': url,
                'title': title_text,
                'description': description,
                'headings': headings,
                'images': images,
                'links': links,
                'text_content': text[:5000],  # First 5000 chars
                'word_count': len(text.split()),
                'html': content
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }
    
    def crawl(self, start_url):
        """Crawl website starting from start_url"""
        start_url = self._normalize_url(start_url)
        to_visit = [start_url]
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (compatible; BusinessAuditBot/1.0)'
            )
            
            while to_visit and len(self.pages_data) < self.max_pages:
                url = to_visit.pop(0)
                
                if url in self.visited:
                    continue
                
                self.visited.add(url)
                
                try:
                    page = context.new_page()
                    page.goto(url, timeout=self.timeout, wait_until='networkidle')
                    time.sleep(1)  # Let JS settle
                    
                    page_data = self._extract_page_data(page, url)
                    self.pages_data.append(page_data)
                    
                    # Find more internal links to crawl
                    if 'links' in page_data:
                        for link in page_data['links']:
                            link_url = self._normalize_url(link['url'])
                            if (link['internal'] and 
                                link_url not in self.visited and 
                                link_url not in to_visit):
                                to_visit.append(link_url)
                    
                    page.close()
                    
                except Exception as e:
                    print(f"  ⚠️  Failed to crawl {url}: {e}")
            
            browser.close()
        
        return {
            'pages': self.pages_data,
            'total_pages': len(self.pages_data),
            'start_url': start_url
        }
