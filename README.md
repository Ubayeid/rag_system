# RAG (Retrieval-Augmented Generation) System

This project implements a Retrieval-Augmented Generation (RAG) system that combines document retrieval with language model generation to provide more accurate and contextually relevant responses.

## Features

- Document ingestion and processing
- Vector storage and retrieval
- Integration with language models
- Query processing and response generation
- Support for multiple document formats (PDF, DOCX, TXT)
- Entity mapping and knowledge graph generation

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
```bash
cp .env.example .env
```
Then edit the `.env` file with your configuration settings.

## Project Structure

- `documents/`: Directory for storing source documents
- `vector_store/`: Directory for storing document embeddings
- `entity_maps/`: Directory for storing entity mappings (not tracked in git due to size)
- `knowledge_graphs/`: Directory for storing knowledge graphs (not tracked in git due to size)
- `src/`: Source code directory
  - `document_processor.py`: Handles document ingestion and processing
  - `embedding_generator.py`: Generates embeddings for documents
  - `retriever.py`: Implements document retrieval logic
  - `generator.py`: Handles response generation
  - `utils.py`: Utility functions

## Usage

1. Place your documents in the `documents` folder
2. Run the document processor:
```bash
python src/document_processor.py
```
3. Start the RAG system:
```bash
python src/main.py
```

## Configuration

The system can be configured through the `.env` file:
- Model settings
- Vector store parameters
- API keys and endpoints
- Processing options

## Data Storage

The following directories are not tracked in git due to their potentially large size:
- `entity_maps/`: Contains JSON files mapping entities from documents
- `knowledge_graphs/`: Contains JSON files representing knowledge graphs
- `documents/`: Contains source documents
- `vector_store/`: Contains document embeddings

To use the system, you'll need to generate these files locally or obtain them from a separate source.

## Error Handling

The system includes comprehensive error handling and logging. Check the logs directory for detailed information about any issues that occur during processing.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 