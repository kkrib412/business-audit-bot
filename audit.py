#!/usr/bin/env python3
"""
Business Audit Bot - CLI Entry Point
Audits websites for SEO, accessibility, and performance issues.
"""

import argparse
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from crawler import WebsiteCrawler
from analyzers import SEOAnalyzer, AccessibilityAnalyzer
from ai_recommendations import AIRecommendationEngine
from pdf_generator import PDFReportGenerator

load_dotenv()


def validate_url(url):
    """Basic URL validation"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def main():
    parser = argparse.ArgumentParser(
        description='Audit websites for SEO, accessibility, and performance'
    )
    parser.add_argument('url', help='Website URL to audit')
    parser.add_argument(
        '-o', '--output',
        default='reports',
        help='Output directory for reports (default: reports/)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=5,
        help='Maximum pages to crawl (default: 5)'
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Skip AI recommendations'
    )
    
    args = parser.parse_args()
    
    # Validate OpenAI API key if AI is enabled
    if not args.no_ai and not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment")
        print("Either set it in .env file or use --no-ai flag")
        sys.exit(1)
    
    url = validate_url(args.url)
    
    print(f"\n🔍 Starting audit for: {url}")
    print(f"📊 Will analyze up to {args.max_pages} pages\n")
    
    # Step 1: Crawl the website
    print("⏳ Crawling website...")
    crawler = WebsiteCrawler(max_pages=args.max_pages)
    try:
        crawl_results = crawler.crawl(url)
        print(f"✅ Crawled {len(crawl_results['pages'])} pages\n")
    except Exception as e:
        print(f"❌ Crawling failed: {e}")
        sys.exit(1)
    
    # Step 2: Analyze SEO
    print("⏳ Analyzing SEO...")
    seo_analyzer = SEOAnalyzer()
    seo_results = seo_analyzer.analyze(crawl_results)
    print(f"✅ Found {seo_results['total_issues']} SEO issues\n")
    
    # Step 3: Analyze Accessibility
    print("⏳ Analyzing accessibility...")
    a11y_analyzer = AccessibilityAnalyzer()
    a11y_results = a11y_analyzer.analyze(crawl_results)
    print(f"✅ Found {a11y_results['total_issues']} accessibility issues\n")
    
    # Step 4: Generate AI recommendations
    ai_recommendations = None
    if not args.no_ai:
        print("⏳ Generating AI recommendations...")
        try:
            ai_engine = AIRecommendationEngine()
            ai_recommendations = ai_engine.generate(
                url=url,
                seo_results=seo_results,
                a11y_results=a11y_results,
                crawl_results=crawl_results
            )
            print("✅ AI recommendations generated\n")
        except Exception as e:
            print(f"⚠️  AI recommendations failed: {e}\n")
    
    # Step 5: Generate PDF report
    print("⏳ Generating PDF report...")
    os.makedirs(args.output, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    domain = url.split('//')[1].split('/')[0].replace('www.', '')
    output_file = os.path.join(args.output, f"{domain}_audit_{timestamp}.pdf")
    
    pdf_gen = PDFReportGenerator()
    try:
        pdf_gen.generate(
            output_path=output_file,
            url=url,
            crawl_results=crawl_results,
            seo_results=seo_results,
            a11y_results=a11y_results,
            ai_recommendations=ai_recommendations
        )
        print(f"✅ Report generated: {output_file}\n")
        print(f"🎉 Audit complete!")
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
