# Business Audit Bot

AI-powered website audit tool that analyzes SEO, accessibility, and generates actionable PDF reports with personalized recommendations.

## Features

- 🔍 **Automated Website Crawling** - Intelligently crawls up to N pages from any website
- 📊 **SEO Analysis** - Detects missing titles, meta descriptions, heading issues, thin content, and duplicate titles
- ♿ **Accessibility Checks** - Finds missing alt text, empty links, and heading structure problems
- 🤖 **AI-Powered Recommendations** - Uses OpenAI to generate priority fixes, quick wins, and long-term strategies
- 📄 **Professional PDF Reports** - Clean, branded reports ready to send to clients

## Installation

### Prerequisites
- Python 3.9+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kkrib412/business-audit-bot.git
cd business-audit-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

5. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Basic Audit
```bash
python audit.py https://example.com
```

### Advanced Options
```bash
# Audit more pages
python audit.py https://example.com --max-pages 10

# Custom output directory
python audit.py https://example.com --output ./my-reports

# Skip AI recommendations (no API key needed)
python audit.py https://example.com --no-ai
```

### Output
Reports are saved to `./reports/` by default with the format:
```
domain.com_audit_20260624_143022.pdf
```

## Example Report Contents

1. **Executive Summary** - High-level metrics and issue counts
2. **SEO Analysis** - Detailed breakdown of SEO issues by priority
3. **Accessibility Analysis** - WCAG-related issues and recommendations
4. **AI Recommendations** - Personalized action plan with priority fixes, quick wins, and long-term strategies

## Project Structure

```
business-audit-bot/
├── audit.py                 # CLI entry point
├── crawler.py              # Website crawling logic
├── analyzers.py            # SEO and accessibility analysis
├── ai_recommendations.py   # OpenAI integration
├── pdf_generator.py        # PDF report generation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── reports/               # Generated reports (gitignored)
```

## Technologies Used

- **Playwright** - Headless browser automation for crawling
- **BeautifulSoup4** - HTML parsing and content extraction
- **OpenAI API** - AI-powered recommendations
- **ReportLab** - PDF generation
- **Python 3.11+** - Core runtime

## Roadmap

- [ ] Lighthouse performance integration
- [ ] Support for additional AI providers (Anthropic, local models)
- [ ] HTML report output option
- [ ] Scheduled audits with email delivery
- [ ] Comparison reports (before/after tracking)
- [ ] WordPress plugin integration

## Contributing

Contributions welcome! Please open an issue first to discuss major changes.

## License

MIT License - see LICENSE file for details

## Author

Kenny Kriberney - [GitHub](https://github.com/kkrib412)

---

Built with ❤️ for helping local businesses improve their web presence
