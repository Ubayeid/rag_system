# CIROH RAG System

A Retrieval-Augmented Generation (RAG) system specifically designed for CIROH (Cooperative Institute for Research to Operations in Hydrology) documents. This system enables intelligent document search, knowledge extraction, and gap analysis in hydrological research.

## Features

- **Intelligent Document Processing**: Handles PDFs, reports, and research papers
- **Semantic Search**: Advanced document retrieval using vector embeddings
- **Knowledge Gap Detection**: Identifies research gaps and inconsistencies
- **Interactive Interface**: User-friendly web interface for querying and analysis
- **API Integration**: RESTful API for programmatic access

1. System Architecture Overview
	a. Core Components
	
	Document Ingestion Pipeline: Process CIROH documents (PDFs, reports, papers)
	Vector Database: Store document embeddings for semantic search
	Retrieval Engine: Find relevant documents based on queries
	Generation Module: LLM-powered response generation
	Knowledge Gap Detection: Identify sparse or inconsistent areas
	Interactive Interface: Web-based query system
	
	b. Technology Stack
	
	LLM: OpenAI GPT-4/3.5-turbo
	Embeddings: OpenAI text-embedding-ada-002
	Vector DB: Chroma/FAISS
	Framework: LangChain
	Backend: FastAPI
	Frontend: Streamlit
	Document Processing: PyPDF2, python-docx

2. Conceptual Framework
	Knowledge Gap Detection Strategies
	
		a. Sparse Coverage Analysis
		
		Identify topics with few supporting documents
		Calculate topic coverage scores
		Highlight underexplored research areas
		
		
		b. Inconsistency Detection
		
		Find contradictory statements across documents
		Identify conflicting methodologies or findings
		Flag areas needing reconciliation
		
		
		c. Temporal Gap Analysis
		
		Detect outdated information
		Identify areas lacking recent research
		Suggest emerging research directions
		
		
		d. Cross-Domain Opportunity Detection
		
		Find potential interdisciplinary connections
		Identify unexplored combinations of concepts
		Suggest novel research hypotheses

3. Implementation
	3.1 Environment Setup
	3.2 Requirements File
	3.3 Core System Implementation
			# config.py
			# document_processor.py
			# vector_store.py
			# knowledge_gap_detector.py
			# rag_system.py
			# api.py
			# streamlit_app.py
			# main.py

4. Deployment and Usage Instructions
	4.1 Quick Start Guide
		# 1. Clone and setup
		git clone https://github.com/Ubayeid/rag_system.git
		cd rag_system
		
		# 2. Create environment
		python -m venv rag_env
		source rag_env/bin/activate  # Windows: rag_env\Scripts\activate
		
		# 3. Install dependencies
		pip install -r requirements.txt
		
		# 4. Set OpenAI API key
		export OPENAI_API_KEY="your-api-key-here"
		
		# 5. Create documents directory and add your CIROH documents
		mkdir documents
		# Copy your PDF, DOCX, TXT files to ./documents/
		
		# 6. Run the system
		python main.py --mode interactive
		
	4.2 Usage Modes
	4.3 Example Queries for Testing

5. Advanced Features and Customization
	5.1 Custom Hydrology Keywords
	5.2 Enhanced Gap Detection
	5.3 Integration with External Data

6. Evaluation and Metrics
	6.1 System Performance Metrics
	6.2 Knowledge Gap Validation

7. Future Enhancements
	7.1 Advanced NLP Features
	7.2 Visualization Enhancements

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Ubayeid/rag_system.git
cd rag_system
```

2. Set up the environment:
```bash
python -m venv rag_env
# On Windows:
.\rag_env\Scripts\activate
# On Unix/MacOS:
source rag_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment:
- Create a `.env` file in the root directory
- Add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

5. Add your documents:
- Place your CIROH documents in the `documents/` directory
- Supported formats: PDF, DOCX, TXT

6. Run the system:
```bash
# Start the API server
python api.py

# Launch the web interface
streamlit run streamlit_app.py
```

## Project Structure

```
rag_system/
├── api.py                 # FastAPI backend
├── config.py             # Configuration settings
├── document_processor.py # Document processing pipeline
├── knowledge_gap_detector.py # Gap analysis module
├── main.py              # Main application entry
├── rag_system.py        # Core RAG implementation
├── requirements.txt     # Project dependencies
├── streamlit_app.py     # Web interface
├── vector_store.py      # Vector database operations
├── documents/           # Document storage
└── vector_db/          # Vector database storage
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.