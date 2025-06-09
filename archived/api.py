from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile
import os
from pydantic import BaseModel

from rag_system import HydrologyRAGSystem
from document_processor import DocumentProcessor

app = FastAPI(title="Hydrology RAG System API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize systems
rag_system = HydrologyRAGSystem()
doc_processor = DocumentProcessor()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    source_documents: List[dict]
    knowledge_gap_analysis: dict
    contradictions: List[dict]
    research_suggestions: List[str]

@app.post("/query", response_model=QueryResponse)
async def query_system(request: QueryRequest):
    """Process a research query."""
    try:
        result = rag_system.query(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process documents."""
    processed_count = 0
    errors = []

    for file in files:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name

            # Process document
            documents = doc_processor.process_document(tmp_file_path)

            if documents:
                rag_system.add_documents(documents)
                processed_count += len(documents)

            # Clean up
            os.unlink(tmp_file_path)

        except Exception as e:
            errors.append(f"Error processing {file.filename}: {str(e)}")

    return {
        "processed_chunks": processed_count,
        "processed_files": len(files) - len(errors),
        "errors": errors
    }

@app.get("/system-stats")
async def get_system_stats():
    """Get system statistics."""
    return rag_system.get_system_stats()

@app.get("/analyze-gaps/{query}")
async def analyze_knowledge_gaps(query: str):
    """Analyze knowledge gaps for a specific topic."""
    return rag_system.gap_detector.analyze_topic_coverage(query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)