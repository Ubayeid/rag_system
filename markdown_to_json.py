import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any

class DocumentProcessor:
    def __init__(self):
        # Define category patterns
        self.category_patterns = {
            'title': r'^# (.+)$',
            'abstract': r'(?i)abstract[:\s]+(.+?)(?=\n\n|\Z)',
            'introduction': r'(?i)introduction[:\s]+(.+?)(?=\n\n|\Z)',
            'methodology': r'(?i)methodology|methods[:\s]+(.+?)(?=\n\n|\Z)',
            'results': r'(?i)results[:\s]+(.+?)(?=\n\n|\Z)',
            'conclusion': r'(?i)conclusion[:\s]+(.+?)(?=\n\n|\Z)',
            'references': r'(?i)references[:\s]+(.+?)(?=\n\n|\Z)',
            'keywords': r'(?i)keywords[:\s]+(.+?)(?=\n\n|\Z)',
            'authors': r'(?i)authors?[:\s]+(.+?)(?=\n\n|\Z)',
            'date': r'(?i)date[:\s]+(.+?)(?=\n\n|\Z)',
            'institution': r'(?i)institution|affiliation[:\s]+(.+?)(?=\n\n|\Z)',
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        return text.strip()

    def extract_categories(self, content: str) -> Dict[str, Any]:
        """Extract structured information from markdown content."""
        if not content:
            return {}
            
        categories = {}
        
        # Extract title
        title_match = re.search(self.category_patterns['title'], content, re.MULTILINE)
        if title_match:
            title_text = title_match.group(1)
            if title_text:
                categories['title'] = self.clean_text(title_text)
        
        # Extract other categories
        for category, pattern in self.category_patterns.items():
            if category == 'title':  # Skip title as it's already processed
                continue
                
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            category_content = []
            
            for match in matches:
                if match and match.group(1):
                    text = self.clean_text(match.group(1))
                    if text:
                        category_content.append(text)
            
            if category_content:
                categories[category] = category_content
        
        # Extract any remaining paragraphs as general content
        remaining_content = content
        for category in categories.values():
            if isinstance(category, str):
                remaining_content = remaining_content.replace(category, '')
            elif isinstance(category, list):
                for item in category:
                    remaining_content = remaining_content.replace(item, '')
        
        # Clean up remaining content
        remaining_content = re.sub(r'\n{3,}', '\n\n', remaining_content.strip())
        if remaining_content:
            # Split into paragraphs and clean each one
            paragraphs = [self.clean_text(p) for p in remaining_content.split('\n\n')]
            # Filter out empty paragraphs
            paragraphs = [p for p in paragraphs if p]
            if paragraphs:
                categories['general_content'] = paragraphs
        
        return categories

    def process_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single markdown file and return structured data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content:
                print(f"Warning: Empty file {file_path}")
                return {}
            
            # Extract filename without extension
            filename = os.path.splitext(os.path.basename(file_path))[0]
            
            # Create document structure
            document = {
                'document_id': filename,
                'categories': self.extract_categories(content)
            }
            
            return document
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return {}

def main():
    # Define paths
    markdown_dir = r"C:\Users\mduba\Development\projects\ai\nlp\RAG\ciroh_x\markdown"
    output_dir = r"C:\Users\mduba\Development\projects\ai\nlp\RAG\ciroh_x\json_output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Process all markdown files
    for filename in os.listdir(markdown_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(markdown_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.json'
            output_path = os.path.join(output_dir, output_filename)
            
            # Process file
            document = processor.process_markdown_file(input_path)
            
            # Save as JSON
            if document and document.get('categories'):
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(document, f, indent=2, ensure_ascii=False)
                print(f"Successfully processed {filename}")
            else:
                print(f"Failed to process {filename} - No valid content extracted")

if __name__ == "__main__":
    main() 