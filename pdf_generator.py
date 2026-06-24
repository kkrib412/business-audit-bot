"""
PDF Report Generator
Generates branded PDF reports from audit results
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


class PDFReportGenerator:
    """Generates PDF reports from audit results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=24,
            fontName='Helvetica-Bold'
        ))
        
        # Issue style
        self.styles.add(ParagraphStyle(
            name='Issue',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))
    
    def _create_title_page(self, url):
        """Create the title page"""
        story = []
        
        # Add spacing
        story.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph("Website Audit Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # URL
        url_text = Paragraph(f"<b>{url}</b>", self.styles['Subtitle'])
        story.append(url_text)
        story.append(Spacer(1, 0.5*inch))
        
        # Date
        date_text = Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Subtitle']
        )
        story.append(date_text)
        
        story.append(PageBreak())
        return story
    
    def _create_summary_section(self, crawl_results, seo_results, a11y_results):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Pages Analyzed', str(crawl_results['total_pages'])],
            ['SEO Issues Found', str(seo_results['total_issues'])],
            ['Accessibility Issues', str(a11y_results['total_issues'])],
            ['High Priority Issues', str(seo_results['by_severity']['high'] + a11y_results['by_severity']['high'])],
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def _create_seo_section(self, seo_results):
        """Create SEO issues section"""
        story = []
        
        story.append(Paragraph("SEO Analysis", self.styles['SectionHeading']))
        
        if seo_results['total_issues'] == 0:
            story.append(Paragraph("✅ No SEO issues found!", self.styles['Normal']))
        else:
            # Group by severity
            for severity in ['high', 'medium', 'low']:
                issues = [i for i in seo_results['issues'] if i['severity'] == severity]
                if issues:
                    severity_title = f"{severity.upper()} Priority ({len(issues)} issues)"
                    story.append(Paragraph(severity_title, self.styles['Heading3']))
                    
                    for issue in issues[:10]:  # Limit to first 10 per severity
                        issue_text = f"• <b>{issue['type'].replace('_', ' ').title()}</b>: {issue['message']}"
                        if issue['url'] != 'site-wide':
                            issue_text += f"<br/>&nbsp;&nbsp;URL: <i>{issue['url']}</i>"
                        story.append(Paragraph(issue_text, self.styles['Issue']))
                    
                    if len(issues) > 10:
                        story.append(Paragraph(
                            f"... and {len(issues) - 10} more {severity} priority issues",
                            self.styles['Issue']
                        ))
                    story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _create_accessibility_section(self, a11y_results):
        """Create accessibility issues section"""
        story = []
        
        story.append(Paragraph("Accessibility Analysis", self.styles['SectionHeading']))
        
        if a11y_results['total_issues'] == 0:
            story.append(Paragraph("✅ No accessibility issues found!", self.styles['Normal']))
        else:
            for severity in ['high', 'medium', 'low']:
                issues = [i for i in a11y_results['issues'] if i['severity'] == severity]
                if issues:
                    severity_title = f"{severity.upper()} Priority ({len(issues)} issues)"
                    story.append(Paragraph(severity_title, self.styles['Heading3']))
                    
                    for issue in issues[:10]:
                        issue_text = f"• <b>{issue['type'].replace('_', ' ').title()}</b>: {issue['message']}"
                        if 'count' in issue:
                            issue_text += f" (Count: {issue['count']})"
                        if issue['url'] != 'site-wide':
                            issue_text += f"<br/>&nbsp;&nbsp;URL: <i>{issue['url']}</i>"
                        story.append(Paragraph(issue_text, self.styles['Issue']))
                    
                    if len(issues) > 10:
                        story.append(Paragraph(
                            f"... and {len(issues) - 10} more {severity} priority issues",
                            self.styles['Issue']
                        ))
                    story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _create_ai_recommendations_section(self, ai_recommendations):
        """Create AI recommendations section"""
        story = []
        
        if not ai_recommendations:
            return story
        
        story.append(Paragraph("AI-Powered Recommendations", self.styles['SectionHeading']))
        
        # Priority fixes
        if ai_recommendations.get('priority_fixes'):
            story.append(Paragraph("🎯 Priority Fixes", self.styles['Heading3']))
            for fix in ai_recommendations['priority_fixes']:
                fix_text = f"• <b>{fix['title']}</b><br/>&nbsp;&nbsp;{fix['description']}<br/>&nbsp;&nbsp;<i>Impact: {fix['impact']}</i>"
                story.append(Paragraph(fix_text, self.styles['Issue']))
            story.append(Spacer(1, 0.2*inch))
        
        # Quick wins
        if ai_recommendations.get('quick_wins'):
            story.append(Paragraph("⚡ Quick Wins", self.styles['Heading3']))
            for win in ai_recommendations['quick_wins']:
                win_text = f"• <b>{win['title']}</b><br/>&nbsp;&nbsp;{win['description']}<br/>&nbsp;&nbsp;<i>Impact: {win['impact']}</i>"
                story.append(Paragraph(win_text, self.styles['Issue']))
            story.append(Spacer(1, 0.2*inch))
        
        # Long-term recommendations
        if ai_recommendations.get('long_term'):
            story.append(Paragraph("🔮 Long-term Recommendations", self.styles['Heading3']))
            for rec in ai_recommendations['long_term']:
                rec_text = f"• <b>{rec['title']}</b><br/>&nbsp;&nbsp;{rec['description']}<br/>&nbsp;&nbsp;<i>Impact: {rec['impact']}</i>"
                story.append(Paragraph(rec_text, self.styles['Issue']))
        
        # Fallback for raw text
        if ai_recommendations.get('raw_text') and not any([
            ai_recommendations.get('priority_fixes'),
            ai_recommendations.get('quick_wins'),
            ai_recommendations.get('long_term')
        ]):
            story.append(Paragraph(ai_recommendations['raw_text'], self.styles['Normal']))
        
        return story
    
    def generate(self, output_path, url, crawl_results, seo_results, a11y_results, ai_recommendations=None):
        """Generate the complete PDF report"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        story = []
        
        # Build the document
        story.extend(self._create_title_page(url))
        story.extend(self._create_summary_section(crawl_results, seo_results, a11y_results))
        story.extend(self._create_seo_section(seo_results))
        story.append(PageBreak())
        story.extend(self._create_accessibility_section(a11y_results))
        
        if ai_recommendations:
            story.append(PageBreak())
            story.extend(self._create_ai_recommendations_section(ai_recommendations))
        
        # Build PDF
        doc.build(story)
