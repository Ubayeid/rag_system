from typing import List, Dict, Any, Optional
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from config import config
from vector_store import VectorStore
from knowledge_gap_detector import KnowledgeGapDetector

class HydrologyRAGSystem:
    def __init__(self):
        self.vector_store = VectorStore()
        self.gap_detector = KnowledgeGapDetector(self.vector_store)
        self.llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name=config.LLM_MODEL,
            temperature=0.3
        )

        # Custom prompt for hydrology research
        self.qa_prompt = PromptTemplate(
            template="""You are an expert hydrologist and research assistant. Use the following pieces of context to answer the question about hydrology research. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Additionally, when appropriate, suggest potential research directions or knowledge gaps you notice.

Context:
{context}

Question: {question}

Please provide a comprehensive answer that includes:
1. Direct answer to the question
2. Supporting evidence from the context
3. Any limitations or uncertainties
4. Potential research directions or gaps identified

Answer:""",
            input_variables=["context", "question"]
        )

        # Initialize QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.vector_db.as_retriever(
                search_kwargs={"k": config.TOP_K_RETRIEVAL}
            ),
            chain_type_kwargs={"prompt": self.qa_prompt},
            return_source_documents=True
        )

    def query(self, question: str) -> Dict[str, Any]:
        """Process a research query and return comprehensive results."""
        try:
            # Get QA response
            qa_result = self.qa_chain({"query": question})

            # Analyze knowledge gaps
            gap_analysis = self.gap_detector.analyze_topic_coverage(question)

            # Find contradictions
            contradictions = self.gap_detector.find_contradictions(question)

            # Compile response
            response = {
                "question": question,
                "answer": qa_result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content[:300] + "...",
                        "source": doc.metadata.get("source", "Unknown"),
                        "file_name": doc.metadata.get("file_name", "Unknown")
                    }
                    for doc in qa_result["source_documents"]
                ],
                "knowledge_gap_analysis": gap_analysis,
                "contradictions": contradictions,
                "research_suggestions": self._generate_research_suggestions(
                    question, gap_analysis, contradictions
                )
            }

            return response

        except Exception as e:
            return {
                "question": question,
                "error": f"Query processing failed: {str(e)}",
                "answer": None
            }

    def _generate_research_suggestions(self, question: str, gap_analysis: Dict, contradictions: List[Dict]) -> List[str]:
        """Generate research suggestions based on gap analysis."""
        suggestions = []

        # Based on gaps
        if "potential_gaps" in gap_analysis:
            for gap in gap_analysis["potential_gaps"]:
                if gap["gap_type"] == "Sparse Keyword Coverage":
                    suggestions.append(
                        f"Investigate {', '.join(gap['details'][:3])} in the context of {question}"
                    )
                elif gap["gap_type"] == "Interdisciplinary Opportunities":
                    suggestions.append(
                        f"Explore interdisciplinary approaches combining hydrology with {', '.join(gap['details'][:2])}"
                    )

        # Based on contradictions
        if contradictions:
            suggestions.append(
                "Reconcile contradictory findings in the literature through systematic review or meta-analysis"
            )

        # Coverage-based suggestions
        if gap_analysis.get("coverage_score", 0) < 50:
            suggestions.append(
                f"Conduct comprehensive literature review on {question} - current coverage appears limited"
            )

        return suggestions[:5]  # Return top 5 suggestions

    def add_documents(self, documents: List[Document]) -> None:
        """Add new documents to the system."""
        self.vector_store.add_documents(documents)

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            "vector_store_stats": self.vector_store.get_collection_stats(),
            "supported_file_types": [".pdf", ".docx", ".txt"],
            "embedding_model": config.EMBEDDING_MODEL,
            "llm_model": config.LLM_MODEL
        }