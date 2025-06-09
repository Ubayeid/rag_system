# main.py
import os
import sys
from pathlib import Path
import argparse
import logging

from document_processor import DocumentProcessor
from rag_system import HydrologyRAGSystem
from config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_system():
    """Initialize the complete RAG system."""
    logger.info("Setting up Hydrology RAG System...")

    # Ensure required directories exist
    os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)
    os.makedirs(config.DOCUMENTS_PATH, exist_ok=True)

    # Initialize components
    doc_processor = DocumentProcessor()
    rag_system = HydrologyRAGSystem()

    logger.info("System setup complete!")
    return doc_processor, rag_system

def load_documents(doc_processor, rag_system, documents_path):
    """Load and process documents from a directory."""
    logger.info(f"Loading documents from {documents_path}...")

    if not os.path.exists(documents_path):
        logger.warning(f"Documents directory {documents_path} does not exist")
        return

    # Process documents
    documents = doc_processor.process_documents_directory(documents_path)

    if documents:
        logger.info(f"Adding {len(documents)} document chunks to vector store...")
        rag_system.add_documents(documents)
        logger.info("Documents loaded successfully!")
    else:
        logger.warning("No documents found to process")

def run_interactive_session(rag_system):
    """Run an interactive query session."""
    logger.info("Starting interactive session...")
    print("\n" + "="*60)
    print("🌊 Hydrology RAG System - Interactive Mode")
    print("="*60)
    print("Enter your hydrology research questions.")
    print("Type 'quit' to exit, 'stats' for system statistics, or 'help' for commands.")
    print("-"*60)

    while True:
        try:
            query = input("\n🔍 Query: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            elif query.lower() == 'stats':
                stats = rag_system.get_system_stats()
                print(f"\n📊 System Statistics:")
                print(f"Total Documents: {stats['vector_store_stats'].get('total_documents', 0)}")
                print(f"Embedding Model: {stats['embedding_model']}")
                print(f"LLM Model: {stats['llm_model']}")
                continue
            elif query.lower() == 'help':
                print("\n📋 Available Commands:")
                print("- Enter any hydrology research question")
                print("- 'stats' - Show system statistics")
                print("- 'quit' - Exit the system")
                continue
            elif not query:
                continue

            print("\n🔄 Processing your query...")
            result = rag_system.query(query)

            if "error" in result:
                print(f"❌ Error: {result['error']}")
                continue

            # Display results
            print(f"\n📋 Answer:")
            print("-" * 40)
            print(result["answer"])

            print(f"\n📚 Sources ({len(result['source_documents'])}):")
            print("-" * 40)
            for i, doc in enumerate(result["source_documents"], 1):
                print(f"{i}. {doc['file_name']}")
                print(f"   {doc['content'][:100]}...")

            # Knowledge gap analysis
            gap_analysis = result.get("knowledge_gap_analysis", {})
            if gap_analysis and "error" not in gap_analysis:
                coverage_score = gap_analysis.get("coverage_score", 0)
                gaps = gap_analysis.get("potential_gaps", [])

                print(f"\n📊 Knowledge Gap Analysis:")
                print("-" * 40)
                print(f"Coverage Score: {coverage_score}%")
                print(f"Potential Gaps: {len(gaps)}")

                if gaps:
                    print("\nTop Knowledge Gaps:")
                    for gap in gaps[:3]:
                        print(f"• {gap['gap_type']} ({gap['severity']} priority)")

            # Research suggestions
            suggestions = result.get("research_suggestions", [])
            if suggestions:
                print(f"\n💡 Research Suggestions:")
                print("-" * 40)
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")

        except KeyboardInterrupt:
            print("\n\nExiting... 👋")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Hydrology RAG System")
    parser.add_argument("--mode", choices=["interactive", "api", "web"], default="interactive", help="System mode")
    parser.add_argument("--load-docs", type=str, help="Path to documents directory")
    parser.add_argument("--port", type=int, default=8000, help="API port")

    args = parser.parse_args()

    try:
        # Setup system
        doc_processor, rag_system = setup_system()

        # Load documents if specified
        if args.load_docs:
            load_documents(doc_processor, rag_system, args.load_docs)
        elif os.path.exists(config.DOCUMENTS_PATH):
            load_documents(doc_processor, rag_system, config.DOCUMENTS_PATH)

        # Run in specified mode
        if args.mode == "interactive":
            run_interactive_session(rag_system)
        elif args.mode == "api":
            logger.info(f"Starting API server on port {args.port}...")
            import uvicorn
            uvicorn.run("api:app", host="0.0.0.0", port=args.port, reload=True)
        elif args.mode == "web":
            logger.info("Starting web interface...")
            os.system("streamlit run streamlit_app.py")

    except Exception as e:
        logger.error(f"System error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()