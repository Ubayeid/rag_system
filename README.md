# RAG (Retrieval-Augmented Generation) System

This project implements a Retrieval-Augmented Generation (RAG) system that combines document retrieval, entity extraction, relationship identification, and knowledge graph construction to provide structured, contextually relevant information from unstructured documents.

## Features

- Document ingestion and conversion (PDF, DOCX to Markdown)
- Markdown to structured JSON conversion
- Entity extraction with context and sentiment analysis
- Relationship identification between entities
- Knowledge graph generation and import to Neo4j
- Modular pipeline for end-to-end processing
- Support for multiple document formats (PDF, DOCX)
- Comprehensive error handling and logging

## Project Structure

- `documents/`: Source documents (PDF, DOCX)
- `markdown/`: Markdown files generated from source documents
- `json_output/`: Structured JSON files generated from markdown
- `entity_extractions/`: Extracted entities with context and statistics
- `knowledge_graphs/`: Knowledge graph JSON files
- `src/`: (Not used; scripts are in the root directory)
- `archived/`: Older or experimental scripts
- Main scripts:
  - `convert_to_markdown.py`: Converts DOCX/PDF to Markdown
  - `markdown_to_json.py`: Converts Markdown to structured JSON
  - `entity_extractor.py`: Extracts entities and context from JSON
  - `relationship_identifier.py`: Identifies relationships between entities
  - `import_to_neo4j.py`: Imports knowledge graph to Neo4j
  - `run_pipeline.py`: Runs the full pipeline in sequence
  - `test_dependencies.py`: Verifies environment and key dependencies

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install the SpaCy English model:
```bash
python -m spacy download en_core_web_sm
```

3. (Optional) Test your environment:
```bash
python test_dependencies.py
```

## Usage

### 1. Prepare Documents
Place your source documents (PDF, DOCX) in the `documents/` folder.

### 2. Run the Pipeline
To process all documents through the full pipeline:
```bash
python run_pipeline.py
```
This will:
- Convert documents to Markdown (`convert_to_markdown.py`)
- Convert Markdown to JSON (`markdown_to_json.py`)
- Extract entities (`entity_extractor.py`)
- Identify relationships (`relationship_identifier.py`)
- Import the knowledge graph to Neo4j (`import_to_neo4j.py`)

### 3. Explore Outputs
- `markdown/`: Contains Markdown versions of your documents
- `json_output/`: Contains structured JSON representations
- `entity_extractions/`: Contains extracted entities and statistics
- `knowledge_graphs/`: Contains knowledge graph JSON files

### 4. Import to Neo4j
Ensure Neo4j is running and update credentials in `import_to_neo4j.py` if needed. Then run:
```bash
python import_to_neo4j.py
```

## Configuration

- Update paths and Neo4j credentials in scripts as needed for your environment.
- The `.env` file can be used for additional configuration (see `.env.example`).

## Data Storage

The following directories are not tracked in git due to their potentially large size:
- `entity_maps/`, `knowledge_graphs/`, `documents/`, `vector_store/`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 