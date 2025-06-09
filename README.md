# Document to Markdown Converter

This tool converts DOCX and PDF documents to Markdown format. It automatically processes all documents placed in the `documents` folder and saves the converted markdown files in the `markdown_output` folder.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Place your documents (DOCX or PDF files) in the `documents` folder.

## Usage

Run the script:
```bash
python document_processor.py
```

The script will:
1. Create a `documents` folder if it doesn't exist
2. Create a `markdown_output` folder if it doesn't exist
3. Process all DOCX and PDF files in the `documents` folder
4. Convert them to markdown format
5. Save the converted files in the `markdown_output` folder

## Supported File Types

- DOCX files (Microsoft Word documents)
- PDF files

## Output

The converted markdown files will be saved in the `markdown_output` folder with the same name as the original file but with a `.md` extension.

## Error Handling

The script includes error handling and will print messages for any files that fail to process. Check the console output for any error messages. 