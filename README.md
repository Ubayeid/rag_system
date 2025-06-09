# RAG (Retrieval-Augmented Generation) System

This project implements a Retrieval-Augmented Generation (RAG) system that combines document retrieval with language model generation to provide more accurate and contextually relevant responses.

## Features

- Document ingestion and processing
- Vector storage and retrieval
- Integration with language models
- Query processing and response generation
- Support for multiple document formats (PDF, DOCX, TXT)

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

## Error Handling

The system includes comprehensive error handling and logging. Check the logs directory for detailed information about any issues that occur during processing.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 