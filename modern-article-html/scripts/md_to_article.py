#!/usr/bin/env python3
"""
Convert Markdown to Modern HTML Article
- Proper markdown to HTML conversion
- Section dividers (---)
- Auto-generate subtitle from content
- No meta field
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug
    Only use English characters and numbers
    For non-English text, this will return empty string
    """
    # Remove all non-ASCII characters first
    slug = re.sub(r'[^\x00-\x7F]+', '', text)
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def build_heading_map(content: str) -> dict:
    """
    Build a map of heading text to slug IDs
    This ensures TOC and HTML content use the same IDs
    Returns dict: {heading_text: slug_id}
    """
    heading_map = {}
    pattern = r'^(#{2,3})\s+(.+)$'
    counter = 0
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        text = match.group(2).strip()
        
        # Try to create slug from text
        slug = slugify(text)
        
        # If slug is empty or too short (non-English text), use numbered slug
        if not slug or len(slug) < 3:
            counter += 1
            slug = f'section-{counter}'
        
        # Store in map (text -> slug)
        heading_map[text] = slug
    
    return heading_map

def extract_headings(content: str, heading_map: dict) -> List[Tuple[int, str, str]]:
    """
    Extract headings from markdown content using pre-built heading map
    Returns list of tuples: (level, text, slug)
    """
    headings = []
    pattern = r'^(#{2,3})\s+(.+)$'
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2).strip()
        slug = heading_map.get(text, f'section-unknown')
        headings.append((level, text, slug))
    
    return headings

def generate_toc_html(headings: List[Tuple[int, str, str]]) -> str:
    """Generate TOC HTML from headings (only h2 level)"""
    if not headings:
        return '<li>ไม่มีหัวข้อ</li>'
    
    toc_items = []
    for level, text, slug in headings:
        if level == 2:
            toc_items.append(f'<li><a href="#{slug}">{text}</a></li>')
    
    return '\n                '.join(toc_items) if toc_items else '<li>ไม่มีหัวข้อ</li>'

def generate_subtitle(content: str, max_length: int = 100) -> str:
    """
    Generate a short subtitle from the first paragraph of content
    """
    # Remove markdown syntax
    clean_content = re.sub(r'#{1,6}\s+', '', content)  # Remove headings
    clean_content = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_content)  # Remove bold
    clean_content = re.sub(r'\*(.+?)\*', r'\1', clean_content)  # Remove italic
    clean_content = re.sub(r'`([^`]+)`', r'\1', clean_content)  # Remove code
    clean_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_content)  # Remove links
    clean_content = re.sub(r'---+', '', clean_content)  # Remove horizontal rules
    
    # Get first meaningful paragraph
    paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
    
    if not paragraphs:
        return "บทความน่าสนใจ"
    
    first_para = paragraphs[0]
    
    # Truncate to max_length
    if len(first_para) > max_length:
        first_para = first_para[:max_length].rsplit(' ', 1)[0] + '...'
    
    return first_para

def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;'))

def markdown_table_to_html(table_text: str) -> str:
    """
    Convert Markdown table to HTML table with modern styling
    
    Markdown format:
    | Header 1 | Header 2 | Header 3 |
    |----------|----------|----------|
    | Cell 1   | Cell 2   | Cell 3   |
    | Cell 4   | Cell 5   | Cell 6   |
    """
    lines = [line.strip() for line in table_text.strip().split('\n') if line.strip()]
    
    if len(lines) < 3:  # Need at least header, separator, and one data row
        return table_text
    
    # Parse header
    header_line = lines[0]
    if not header_line.startswith('|') or not header_line.endswith('|'):
        return table_text
    
    headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
    
    # Skip separator line (lines[1])
    
    # Parse data rows
    data_rows = []
    for line in lines[2:]:
        if line.startswith('|') and line.endswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            data_rows.append(cells)
    
    # Generate HTML table
    html = '<div class="table-wrapper">\n<table>\n<thead>\n<tr>\n'
    
    # Add headers
    for header in headers:
        html += f'<th>{header}</th>\n'
    
    html += '</tr>\n</thead>\n<tbody>\n'
    
    # Add data rows
    for row in data_rows:
        html += '<tr>\n'
        for cell in row:
            html += f'<td>{cell}</td>\n'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n</div>'
    
    return html

def markdown_to_html(md_content: str, heading_map: dict) -> str:
    """
    Convert markdown content to HTML with proper formatting
    --- becomes a section divider (not shown in HTML, just splits content)
    heading_map: pre-built map of heading text to slug IDs
    """
    # Split by --- (horizontal rule / section divider)
    sections = re.split(r'^---+$', md_content, flags=re.MULTILINE)
    
    html_sections = []
    
    for section in sections:
        if not section.strip():
            continue
            
        html = section
        
        # Step 1: Process code blocks FIRST (before any other processing)
        # Store code blocks temporarily to protect them
        code_blocks = {}
        code_block_counter = [0]
        
        def save_code_block(match):
            lang = match.group(1) or ''
            code = match.group(2)
            # Escape HTML in code
            escaped_code = escape_html(code)
            placeholder = f'XYZCODEBLOCKREPLACE{code_block_counter[0]}XYZ'
            code_blocks[placeholder] = f'<pre><code>{escaped_code}</code></pre>'
            code_block_counter[0] += 1
            return placeholder
        
        html = re.sub(r'```(\w+)?\n(.*?)```', save_code_block, html, flags=re.DOTALL)
        
        # Step 2: Process inline code (before text formatting)
        inline_codes = {}
        inline_code_counter = [0]
        
        def save_inline_code(match):
            code = match.group(1)
            # Escape HTML in inline code
            escaped_code = escape_html(code)
            placeholder = f'XYZINLINECODEREPLACE{inline_code_counter[0]}XYZ'
            inline_codes[placeholder] = f'<code>{escaped_code}</code>'
            inline_code_counter[0] += 1
            return placeholder
        
        html = re.sub(r'`([^`]+)`', save_inline_code, html)
        
        # Step 2.5: Process tables (before headers and formatting)
        tables = {}
        table_counter = [0]
        
        def save_table(match):
            table_text = match.group(0)
            table_html = markdown_table_to_html(table_text)
            placeholder = f'XYZTABLEREPLACE{table_counter[0]}XYZ'
            tables[placeholder] = table_html
            table_counter[0] += 1
            return placeholder
        
        # Match markdown tables (must start with |, have separator line, and at least one data row)
        table_pattern = r'(?:^\|.+\|$\n)+^\|[\s:|-]+\|$\n(?:^\|.+\|$\n?)+'
        html = re.sub(table_pattern, save_table, html, flags=re.MULTILINE)
        
        # Step 3: Headers with IDs for anchor links
        # Use pre-built heading_map for consistent IDs
        
        def create_h2_with_id(match):
            text = match.group(1)
            slug = heading_map.get(text, f'section-{text[:10]}')
            return f'<h2 id="{slug}">{text}</h2>'
        
        def create_h3_with_id(match):
            text = match.group(1)
            slug = heading_map.get(text, f'section-{text[:10]}')
            return f'<h3 id="{slug}">{text}</h3>'
        
        html = re.sub(r'^#### (.+)$', lambda m: f'<h4>{m.group(1)}</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', create_h3_with_id, html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', create_h2_with_id, html, flags=re.MULTILINE)
        
        # Step 4: Bold (must come before italic)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        
        # Step 5: Italic
        html = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'_([^_]+?)_', r'<em>\1</em>', html)
        
        # Step 6: Links (before images to avoid conflicts)
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
        
        # Step 7: Images
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', html)
        
        # Step 8: Blockquotes - handle multi-line
        lines = html.split('\n')
        in_blockquote = False
        result = []
        blockquote_lines = []
        
        for line in lines:
            if line.strip().startswith('>'):
                if not in_blockquote:
                    in_blockquote = True
                blockquote_lines.append(line.strip().lstrip('> '))
            else:
                if in_blockquote:
                    result.append('<blockquote>' + ' '.join(blockquote_lines) + '</blockquote>')
                    in_blockquote = False
                    blockquote_lines = []
                result.append(line)
        
        if in_blockquote:
            result.append('<blockquote>' + ' '.join(blockquote_lines) + '</blockquote>')
        
        html = '\n'.join(result)
        
        # Step 9: Unordered lists
        html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\+ (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Step 10: Ordered lists
        html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Step 11: Wrap consecutive <li> in <ul>
        html = re.sub(
            r'(<li>.*?</li>(?:\n<li>.*?</li>)*)',
            lambda m: '<ul>\n' + m.group(1) + '\n</ul>',
            html,
            flags=re.DOTALL
        )
        
        # Step 12: Paragraphs
        lines = html.split('\n')
        result = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                # Check if line is already wrapped in a tag or is a placeholder
                is_tag = any(
                    stripped.startswith(f'<{tag}') or stripped.startswith(f'</{tag}')
                    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 
                               'blockquote', 'pre', 'div', 'img', 'p']
                )
                is_placeholder = (stripped.startswith('XYZCODEBLOCKREPLACE') or 
                                stripped.startswith('XYZINLINECODEREPLACE') or
                                stripped.startswith('XYZTABLEREPLACE'))
                
                if not is_tag and not is_placeholder and not stripped.endswith('>'):
                    result.append(f'<p>{stripped}</p>')
                else:
                    result.append(line)
            else:
                result.append(line)
        
        html = '\n'.join(result)
        
        # Step 13: Restore tables first (before inline codes)
        for placeholder, table_html in tables.items():
            html = html.replace(placeholder, table_html)
        
        # Step 14: Restore inline codes (they might be inside other elements)
        for placeholder, code_html in inline_codes.items():
            html = html.replace(placeholder, code_html)
        
        # Step 15: Restore code blocks last (they are block-level elements)
        for placeholder, code_html in code_blocks.items():
            html = html.replace(placeholder, code_html)
        
        html_sections.append(html.strip())
    
    # Wrap each section in a content-box div
    wrapped_sections = []
    for i, section_html in enumerate(html_sections):
        # Add special class for first box if needed
        box_class = 'content-box'
        if i == 0:
            box_class += ' first-box'
        
        wrapped_sections.append(f'<div class="{box_class} fade-in">\n{section_html}\n</div>')
    
    # Join sections
    return '\n\n'.join(wrapped_sections)

def create_article_html(
    title: str,
    subtitle: str,
    content: str,
    template_path: str = None
) -> str:
    """
    Create complete HTML article from components
    
    Args:
        title: Article title
        subtitle: Article subtitle (auto-generated if empty)
        content: Article content (markdown)
        template_path: Path to HTML template file
    """
    # Load template
    if template_path is None:
        template_path = Path(__file__).parent.parent / 'assets' / 'article-template.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Build heading map first (ensures consistent IDs)
    heading_map = build_heading_map(content)
    
    # Extract headings using the map
    headings = extract_headings(content, heading_map)
    
    # Auto-generate subtitle if not provided
    if not subtitle:
        subtitle = generate_subtitle(content)
    
    # Convert markdown to HTML using the same map
    html_content = markdown_to_html(content, heading_map)
    
    # Generate TOC
    toc_html = generate_toc_html(headings)
    
    # Replace placeholders
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{SUBTITLE}}', subtitle)
    html = html.replace('{{TOC_ITEMS}}', toc_html)
    html = html.replace('{{CONTENT}}', html_content)
    
    return html

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python md_to_article.py <input.md> [output.html]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.html')
    
    if not input_file.exists():
        print(f"Error: File {input_file} not found")
        sys.exit(1)
    
    # Read markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extract title from first # heading or use filename
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        # Remove the title line from content
        md_content = re.sub(r'^#\s+.+$\n?', '', md_content, count=1, flags=re.MULTILINE)
    else:
        title = input_file.stem.replace('-', ' ').replace('_', ' ').title()
    
    # Auto-generate subtitle from content
    subtitle = generate_subtitle(md_content)
    
    # Generate HTML
    html_output = create_article_html(title, subtitle, md_content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"✅ Created: {output_file}")
    print(f"📊 Size: {len(html_output):,} bytes")
    print(f"📝 Title: {title}")
    print(f"💬 Subtitle: {subtitle}")

if __name__ == "__main__":
    main()
