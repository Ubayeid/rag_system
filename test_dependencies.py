import sys
import langchain
import chromadb
import sentence_transformers
import spacy
import torch

def test_imports():
    print("Python version:", sys.version)
    print("\nKey package versions:")
    print("LangChain:", langchain.__version__)
    print("ChromaDB:", chromadb.__version__)
    print("Sentence Transformers:", sentence_transformers.__version__)
    print("SpaCy:", spacy.__version__)
    print("PyTorch:", torch.__version__)
    
    # Test SpaCy model
    print("\nTesting SpaCy model...")
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("This is a test sentence.")
    print("SpaCy tokenization:", [token.text for token in doc])
    
    # Test Sentence Transformers
    print("\nTesting Sentence Transformers...")
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode("This is a test sentence.")
    print("Embedding shape:", embeddings.shape)
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_imports()