import os
import docx2txt
import PyPDF2
from pathlib import Path

def convert_docx_to_markdown(docx_path, output_path):
    """Convert a Word document to markdown format."""
    try:
        # Extract text from docx
        text = docx2txt.process(docx_path)
        
        # Basic markdown formatting
        # Convert headings (assuming they're in all caps or have specific formatting)
        lines = text.split('\n')
        markdown_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Simple heading detection (you might want to enhance this)
            if line.isupper() and len(line) < 100:
                markdown_lines.append(f"# {line}")
            else:
                markdown_lines.append(line)
        
        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(markdown_lines))
            
        print(f"Successfully converted {docx_path} to markdown")
        
    except Exception as e:
        print(f"Error converting {docx_path}: {str(e)}")

def convert_pdf_to_markdown(pdf_path, output_path):
    """Convert a PDF document to markdown format."""
    try:
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            
            # Basic markdown formatting
            lines = text.split('\n')
            markdown_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Simple heading detection
                if line.isupper() and len(line) < 100:
                    markdown_lines.append(f"# {line}")
                else:
                    markdown_lines.append(line)
            
            # Write to markdown file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(markdown_lines))
                
        print(f"Successfully converted {pdf_path} to markdown")
        
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def main():
    # Define paths
    source_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\documents"
    output_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\markdown"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each file in the source directory
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        
        # Create output filename (replace extension with .md)
        output_filename = os.path.splitext(filename)[0] + '.md'
        output_path = os.path.join(output_dir, output_filename)
        
        # Convert based on file type
        if filename.endswith('.docx'):
            convert_docx_to_markdown(source_path, output_path)
        elif filename.endswith('.pdf'):
            convert_pdf_to_markdown(source_path, output_path)

if __name__ == "__main__":
    main() 