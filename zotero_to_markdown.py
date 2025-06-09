#!/usr/bin/env python3
"""
Zotero to Markdown Converter
Imports various file types from Zotero and converts them to Markdown format.
"""

import os
import json
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import pypandoc
import mammoth
import PyPDF2
from pyzotero import zotero
import rispy
from datetime import datetime
from urllib.parse import urlparse
import time
from bs4 import BeautifulSoup
import re
import configparser
import base64

class ZoteroToMarkdownConverter:
    def __init__(self, library_id, library_type, api_key, output_dir="metadata"):
        """
        Initialize the converter with Zotero credentials.
        
        Args:
            library_id (str): Your Zotero library ID
            library_type (str): 'user' or 'group'
            api_key (str): Your Zotero API key
            output_dir (str): Directory to save markdown files
        """
        self.zot = zotero.Zotero(library_id, library_type, api_key)
        self.output_dir = Path(output_dir)
        self.full_text_dir = Path("full_text")
        self.output_dir.mkdir(exist_ok=True)
        self.full_text_dir.mkdir(exist_ok=True)

    def download_pdf_from_url(self, url, title):
        """Download PDF from URL with enhanced error handling and retries."""
        try:
            # Clean the title for filename
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title[:50]  # Limit length
            
            # Add delay to be respectful to servers
            time.sleep(2)
            
            # First try to get the page content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Handle common academic paper URL patterns
            if 'doi.org' in url:
                try:
                    doi_response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
                    if doi_response.status_code == 200:
                        url = doi_response.url
                except Exception as e:
                    print(f"    ⚠️  Error following DOI: {e}")
            
            # Check for common academic repositories
            if 'arxiv.org' in url:
                # Convert to PDF URL if it's not already
                if not url.endswith('.pdf'):
                    url = url.replace('/abs/', '/pdf/') + '.pdf'
            
            # Try to access the URL
            try:
                response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
                
                if response.status_code != 200:
                    print(f"    ❌ Failed to access URL: {url}")
                    return None
                
                # Check if the response is already a PDF
                content_type = response.headers.get('content-type', '').lower()
                if 'application/pdf' in content_type:
                    # Save PDF temporarily
                    temp_pdf_path = self.full_text_dir / f"{clean_title}_temp.pdf"
                    with open(temp_pdf_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Convert to markdown
                    markdown_content = self.pdf_to_markdown(temp_pdf_path)
                    
                    # Save markdown
                    markdown_path = self.full_text_dir / f"{clean_title}.md"
                    with open(markdown_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    # Remove temporary PDF
                    temp_pdf_path.unlink()
                    
                    return markdown_path
                
                # Try to find PDF link in the page
                soup = BeautifulSoup(response.text, 'html.parser')
                pdf_links = []
                
                # Look for common PDF link patterns
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    link_text = link.get_text().lower()
                    
                    # Check for PDF links
                    if href.lower().endswith('.pdf'):
                        pdf_links.append(href)
                    elif 'pdf' in href.lower() or 'download' in href.lower():
                        pdf_links.append(href)
                    elif 'pdf' in link_text or 'download' in link_text:
                        pdf_links.append(href)
                
                # Also look for meta tags that might contain PDF links
                for meta in soup.find_all('meta'):
                    if meta.get('name', '').lower() in ['citation_pdf_url', 'pdf_url']:
                        pdf_url = meta.get('content')
                        if pdf_url:
                            pdf_links.append(pdf_url)
                
                if not pdf_links:
                    print(f"    ❌ No PDF links found on page: {url}")
                    return None
                
                # Try each PDF link
                for pdf_link in pdf_links:
                    try:
                        # Handle relative URLs
                        if not pdf_link.startswith(('http://', 'https://')):
                            parsed_url = urlparse(url)
                            pdf_link = f"{parsed_url.scheme}://{parsed_url.netloc}{pdf_link}"
                        
                        pdf_response = requests.get(pdf_link, headers=headers, allow_redirects=True, timeout=30)
                        
                        if pdf_response.status_code == 200:
                            content_type = pdf_response.headers.get('content-type', '').lower()
                            if 'application/pdf' in content_type:
                                # Save PDF temporarily
                                temp_pdf_path = self.full_text_dir / f"{clean_title}_temp.pdf"
                                with open(temp_pdf_path, 'wb') as f:
                                    f.write(pdf_response.content)
                                
                                # Convert to markdown
                                markdown_content = self.pdf_to_markdown(temp_pdf_path)
                                
                                # Save markdown
                                markdown_path = self.full_text_dir / f"{clean_title}.md"
                                with open(markdown_path, 'w', encoding='utf-8') as f:
                                    f.write(markdown_content)
                                
                                # Remove temporary PDF
                                temp_pdf_path.unlink()
                                
                                return markdown_path
                    except Exception as e:
                        continue
                
                print(f"    ❌ Could not find downloadable PDF on page: {url}")
                return None
                
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Network error accessing URL {url}: {e}")
                return None
            
        except Exception as e:
            print(f"    ❌ Error processing URL {url}: {e}")
            return None

    def fetch_all_items(self):
        """Fetch all items from Zotero library."""
        try:
            items = self.zot.everything(self.zot.items())
            print(f"Fetched {len(items)} items from Zotero")
            return items
        except Exception as e:
            print(f"Error fetching items: {e}")
            return []
    
    def download_attachment(self, attachment_key, filename):
        """Download attachment file from Zotero."""
        try:
            file_content = self.zot.file(attachment_key)
            file_path = self.output_dir / "attachments" / filename
            file_path.parent.mkdir(exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            return file_path
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return None
    
    def pdf_to_markdown(self, pdf_path):
        """Convert PDF to markdown with enhanced text extraction."""
        try:
            # Try multiple PDF extraction methods for better results
            text_content = ""
            
            # Method 1: PyPDF2 (basic extraction)
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content += f"\n## Page {page_num + 1}\n\n{page_text}\n"
            except Exception as e:
                print(f"PyPDF2 extraction failed for {pdf_path}: {e}")
            
            # Method 2: Try pypandoc as fallback
            if not text_content.strip():
                try:
                    text_content = pypandoc.convert_file(str(pdf_path), 'md')
                except Exception as e:
                    print(f"Pypandoc PDF conversion failed for {pdf_path}: {e}")
            
            # Clean and format the content
            if text_content.strip():
                # Remove excessive whitespace and clean up formatting
                lines = [line.strip() for line in text_content.split('\n')]
                cleaned_lines = []
                
                for line in lines:
                    if line:  # Skip empty lines
                        # Try to identify headers and format them
                        if len(line) < 100 and line.isupper():
                            cleaned_lines.append(f"## {line.title()}")
                        elif line.endswith(':') and len(line) < 80:
                            cleaned_lines.append(f"### {line}")
                        else:
                            cleaned_lines.append(line)
                    elif cleaned_lines and cleaned_lines[-1] != "":
                        cleaned_lines.append("")  # Preserve paragraph breaks
                
                return "\n".join(cleaned_lines)
            else:
                return f"# PDF Document\n\n*Content could not be extracted from {pdf_path.name}*"
                
        except Exception as e:
            print(f"Error converting PDF {pdf_path}: {e}")
            return f"# PDF Document\n\n*Error extracting content: {str(e)}*"
    
    def docx_to_markdown(self, docx_path):
        """Convert DOCX to markdown with enhanced formatting preservation."""
        try:
            with open(docx_path, "rb") as docx_file:
                # Use mammoth with custom style map for better formatting
                style_map = """
                p[style-name='Heading 1'] => h1:fresh
                p[style-name='Heading 2'] => h2:fresh
                p[style-name='Heading 3'] => h3:fresh
                p[style-name='Heading 4'] => h4:fresh
                p[style-name='Title'] => h1:fresh
                p[style-name='Subtitle'] => h2:fresh
                """
                
                result = mammoth.convert_to_markdown(
                    docx_file,
                    style_map=style_map,
                    convert_image=mammoth.images.img_element(self._save_docx_image)
                )
                
                # Clean up the markdown
                markdown = result.value
                if result.messages:
                    print(f"Mammoth conversion messages for {docx_path.name}: {result.messages}")
                
                # Post-process markdown for better formatting
                lines = markdown.split('\n')
                cleaned_lines = []
                
                for line in lines:
                    # Fix common formatting issues
                    line = line.strip()
                    if line:
                        # Convert bold/italic markers
                        line = line.replace('**', '**').replace('*', '_')
                        cleaned_lines.append(line)
                    else:
                        if cleaned_lines and cleaned_lines[-1] != "":
                            cleaned_lines.append("")
                
                return '\n'.join(cleaned_lines)
                
        except Exception as e:
            print(f"Error converting DOCX {docx_path}: {e}")
            return f"# Document Content\n\n*Error extracting content: {str(e)}*"
    
    def _save_docx_image(self, image):
        """Save images from DOCX files."""
        try:
            image_dir = self.output_dir / "images"
            image_dir.mkdir(exist_ok=True)
            
            with image.open() as image_bytes:
                image_filename = f"image_{hash(image_bytes.read())}.png"
                image_path = image_dir / image_filename
                
                with open(image_path, 'wb') as f:
                    image_bytes.seek(0)
                    f.write(image_bytes.read())
                
                return {"src": f"images/{image_filename}"}
        except Exception as e:
            print(f"Error saving image: {e}")
            return {"src": ""}  # Return empty src if image saving fails
    
    def txt_to_markdown(self, txt_path):
        """Convert TXT to markdown."""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"# Text Document\n\n{content}"
        except Exception as e:
            print(f"Error converting TXT {txt_path}: {e}")
            return None
    
    def html_to_markdown(self, html_path):
        """Convert HTML to markdown using pypandoc."""
        try:
            return pypandoc.convert_file(html_path, 'md')
        except Exception as e:
            print(f"Error converting HTML {html_path}: {e}")
            return None
    
    def bibtex_to_markdown(self, bibtex_content):
        """Convert BibTeX to markdown."""
        try:
            parser = BibTexParser(common_strings=True)
            parser.customization = convert_to_unicode
            bib_database = bibtexparser.loads(bibtex_content, parser=parser)
            
            markdown_content = "# Bibliography\n\n"
            for entry in bib_database.entries:
                markdown_content += f"## {entry.get('title', 'No Title')}\n\n"
                markdown_content += f"**Authors:** {entry.get('author', 'Unknown')}\n\n"
                markdown_content += f"**Year:** {entry.get('year', 'Unknown')}\n\n"
                if 'abstract' in entry:
                    markdown_content += f"**Abstract:** {entry['abstract']}\n\n"
                markdown_content += "---\n\n"
            
            return markdown_content
        except Exception as e:
            print(f"Error converting BibTeX: {e}")
            return None
    
    def ris_to_markdown(self, ris_content):
        """Convert RIS to markdown."""
        try:
            entries = rispy.loads(ris_content)
            markdown_content = "# RIS Bibliography\n\n"
            
            for entry in entries:
                title = entry.get('title', entry.get('primary_title', 'No Title'))
                markdown_content += f"## {title}\n\n"
                
                if 'authors' in entry:
                    authors = ', '.join(entry['authors'])
                    markdown_content += f"**Authors:** {authors}\n\n"
                
                if 'publication_year' in entry:
                    markdown_content += f"**Year:** {entry['publication_year']}\n\n"
                
                if 'abstract' in entry:
                    markdown_content += f"**Abstract:** {entry['abstract']}\n\n"
                
                markdown_content += "---\n\n"
            
            return markdown_content
        except Exception as e:
            print(f"Error converting RIS: {e}")
            return None
    
    def xml_to_markdown(self, xml_content, format_type="generic"):
        """Convert XML to markdown."""
        try:
            root = ET.fromstring(xml_content)
            markdown_content = f"# {format_type.upper()} Data\n\n"
            
            # Generic XML to markdown conversion
            def xml_to_text(element, level=0):
                text = ""
                indent = "  " * level
                
                if element.text and element.text.strip():
                    text += f"{indent}- **{element.tag}:** {element.text.strip()}\n"
                elif len(element) > 0:
                    text += f"{indent}- **{element.tag}:**\n"
                
                for child in element:
                    text += xml_to_text(child, level + 1)
                
                return text
            
            markdown_content += xml_to_text(root)
            return markdown_content
        except Exception as e:
            print(f"Error converting XML: {e}")
            return None
    
    def json_to_markdown(self, json_content):
        """Convert JSON to markdown."""
        try:
            data = json.loads(json_content)
            markdown_content = "# JSON Data\n\n"
            
            if isinstance(data, list):
                for i, item in enumerate(data):
                    markdown_content += f"## Item {i+1}\n\n"
                    markdown_content += self._dict_to_markdown(item)
                    markdown_content += "\n---\n\n"
            elif isinstance(data, dict):
                markdown_content += self._dict_to_markdown(data)
            
            return markdown_content
        except Exception as e:
            print(f"Error converting JSON: {e}")
            return None
    
    def _dict_to_markdown(self, data, level=0):
        """Helper function to convert dictionary to markdown."""
        markdown = ""
        indent = "  " * level
        
        for key, value in data.items():
            if isinstance(value, dict):
                markdown += f"{indent}- **{key}:**\n"
                markdown += self._dict_to_markdown(value, level + 1)
            elif isinstance(value, list):
                markdown += f"{indent}- **{key}:** {', '.join(map(str, value))}\n"
            else:
                markdown += f"{indent}- **{key}:** {value}\n"
        
        return markdown
    
    def create_item_markdown(self, item):
        """Create markdown for a Zotero item with its metadata."""
        title = item['data'].get('title', 'Untitled')
        authors = []
        
        # Extract authors
        if 'creators' in item['data']:
            for creator in item['data']['creators']:
                if 'name' in creator:
                    authors.append(creator['name'])
                else:
                    name_parts = []
                    if 'firstName' in creator:
                        name_parts.append(creator['firstName'])
                    if 'lastName' in creator:
                        name_parts.append(creator['lastName'])
                    authors.append(' '.join(name_parts))
        
        # Create markdown header
        markdown_content = f"# {title}\n\n"
        
        if authors:
            markdown_content += f"**Authors:** {', '.join(authors)}\n\n"
        
        if 'date' in item['data']:
            markdown_content += f"**Date:** {item['data']['date']}\n\n"
        
        if 'itemType' in item['data']:
            markdown_content += f"**Type:** {item['data']['itemType']}\n\n"
        
        if 'abstractNote' in item['data']:
            markdown_content += f"**Abstract:**\n{item['data']['abstractNote']}\n\n"
        
        if 'url' in item['data']:
            markdown_content += f"**URL:** {item['data']['url']}\n\n"
        
        # Add tags if present
        if 'tags' in item['data'] and item['data']['tags']:
            tags = [tag['tag'] for tag in item['data']['tags']]
            markdown_content += f"**Tags:** {', '.join(tags)}\n\n"
        
        markdown_content += "---\n\n"
        
        return markdown_content
    
    def process_attachments(self, item):
        """Process attachments for an item with enhanced content extraction."""
        attachments_markdown = ""
        
        # Get child items (attachments)
        try:
            children = self.zot.children(item['key'])
            attachment_count = 0
            
            for child in children:
                if child['data']['itemType'] == 'attachment':
                    filename = child['data'].get('filename', f'attachment_{attachment_count}')
                    attachment_key = child['key']
                    attachment_count += 1
                    
                    print(f"  Processing attachment: {filename}")
                    
                    # Download attachment
                    file_path = self.download_attachment(attachment_key, filename)
                    if file_path and file_path.exists():
                        # Convert based on file extension
                        file_ext = file_path.suffix.lower()
                        content = None
                        
                        print(f"    Converting {file_ext} file...")
                        
                        if file_ext == '.pdf':
                            content = self.pdf_to_markdown(file_path)
                        elif file_ext in ['.docx', '.doc']:
                            content = self.docx_to_markdown(file_path)
                        elif file_ext == '.txt':
                            content = self.txt_to_markdown(file_path)
                        elif file_ext in ['.html', '.htm']:
                            content = self.html_to_markdown(file_path)
                        elif file_ext == '.rtf':
                            content = self.rtf_to_markdown(file_path)
                        else:
                            # Try to read as text for other formats
                            content = self.generic_text_extraction(file_path)
                        
                        if content and content.strip():
                            attachments_markdown += f"\n\n# 📎 Attachment: {filename}\n\n"
                            attachments_markdown += content + "\n\n"
                            attachments_markdown += "---\n\n"
                            print(f"    ✅ Successfully converted {filename}")
                        else:
                            attachments_markdown += f"\n\n# 📎 Attachment: {filename}\n\n"
                            attachments_markdown += f"*Could not extract content from {filename}*\n\n"
                            attachments_markdown += "---\n\n"
                            print(f"    ⚠️  Could not extract content from {filename}")
                    else:
                        print(f"    ❌ Failed to download {filename}")
        
        except Exception as e:
            print(f"Error processing attachments: {e}")
            attachments_markdown += f"\n\n*Error processing attachments: {str(e)}*\n\n"
        
        return attachments_markdown
    
    def rtf_to_markdown(self, rtf_path):
        """Convert RTF to markdown."""
        try:
            # Try using pypandoc for RTF conversion
            return pypandoc.convert_file(str(rtf_path), 'md')
        except Exception as e:
            print(f"Error converting RTF {rtf_path}: {e}")
            return self.generic_text_extraction(rtf_path)
    
    def generic_text_extraction(self, file_path):
        """Generic text extraction for unknown file types."""
        try:
            # Try reading as UTF-8 text
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return f"# Text Content\n\n```\n{content}\n```"
        except UnicodeDecodeError:
            try:
                # Try reading with different encoding
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    return f"# Text Content\n\n```\n{content}\n```"
            except Exception as e:
                return f"# File Content\n\n*Could not extract text from {file_path.name}: {str(e)}*"
        except Exception as e:
            return f"# File Content\n\n*Error reading {file_path.name}: {str(e)}*"
    
    def process_url_attachments(self, item):
        """Process URLs in item metadata to download PDFs."""
        url_markdown = ""
        
        if 'url' in item['data'] and item['data']['url']:
            url = item['data']['url']
            title = item['data'].get('title', 'untitled')
            
            markdown_path = self.download_pdf_from_url(url, title)
            
            if markdown_path and markdown_path.exists():
                print(f"    ✅ Successfully downloaded and converted content from URL")
                with open(markdown_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content and content.strip():
                    url_markdown += f"\n\n# 📄 Full Text from URL\n\n"
                    url_markdown += content + "\n\n"
                    url_markdown += "---\n\n"
                else:
                    url_markdown += f"\n\n# 📄 Full Text from URL\n\n"
                    url_markdown += f"*Could not extract content from downloaded document*\n\n"
                    url_markdown += "---\n\n"
                    print(f"    ⚠️  Could not extract content from downloaded document")
        else:
            print(f"    ℹ️  No URL found for this item")
        
        return url_markdown

    def convert_all_to_markdown(self):
        """Main function to convert all Zotero items to markdown with full document content."""
        items = self.fetch_all_items()
        
        if not items:
            print("No items found in Zotero library!")
            return
        
        # print(f"\n🔄 Starting conversion of {len(items)} items...\n")
        
        for i, item in enumerate(items):
            try:
                print(f"\n📄 Processing item {i+1}/{len(items)}: ", end="")
                
                # Create markdown for item metadata
                item_markdown = self.create_item_markdown(item)
                
                title = item['data'].get('title', f'item_{i}')
                print(f"'{title[:50]}{'...' if len(title) > 50 else ''}'")
                
                # Process attachments with full content extraction
                attachments_markdown = self.process_attachments(item)
                
                # Process URLs to download PDFs
                url_markdown = self.process_url_attachments(item)
                
                # Combine content
                full_markdown = item_markdown
                if attachments_markdown.strip():
                    full_markdown += "\n\n# 📚 Full Document Content\n\n"
                    full_markdown += attachments_markdown
                if url_markdown.strip():
                    full_markdown += url_markdown
                if not attachments_markdown.strip() and not url_markdown.strip():
                    full_markdown += "\n\n*No attachments or downloadable content found for this item.*\n\n"
                
                # Save to file
                filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = filename[:50]  # Limit length
                if not filename:
                    filename = f"item_{i}"
                
                output_file = self.output_dir / f"{filename}_{item['key']}.md"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_markdown)
                
                # print(f"    ✅ Saved: {output_file.name}")
                
            except Exception as e:
                print(f"  ❌ Error processing item {i}: {e}")
        
        # print(f"\n🎉 Conversion complete! Files saved to {self.output_dir}")
        print(f"📊 Total items processed: {len(items)}")

# Example usage
if __name__ == "__main__":
    # Configure your Zotero credentials
    LIBRARY_ID = "17301708"  # Your Zotero User ID
    LIBRARY_TYPE = "user"  # Keep as "user" for personal library
    API_KEY = "DCOPuOZNDMpeCb0gvfiSvsOw"  # Your API key
    
    # Validate credentials before proceeding
    if LIBRARY_ID == "your_library_id" or API_KEY == "your_api_key":
        print("ERROR: Please update LIBRARY_ID and API_KEY with your actual Zotero credentials!")
        print("1. Go to zotero.org/settings/keys")
        print("2. Find your User ID (it's a number like 1234567)")
        print("3. Create a new private key with read access")
        print("4. Replace the placeholder values in this script")
        exit(1)
    
    # Create converter instance
    converter = ZoteroToMarkdownConverter(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    
    # Convert all items to markdown
    converter.convert_all_to_markdown()