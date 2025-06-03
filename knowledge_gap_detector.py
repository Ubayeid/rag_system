import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from langchain.schema import Document
import re

class KnowledgeGapDetector:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.hydrology_keywords = [
            "watershed", "streamflow", "groundwater", "precipitation", "evapotranspiration",
            "runoff", "infiltration", "aquifer", "discharge", "flood", "drought",
            "water quality", "sediment", "erosion", "climate change", "modeling",
            "remote sensing", "GIS", "SWAT", "HEC", "statistical analysis"
        ]

    def analyze_topic_coverage(self, query: str, num_clusters: int = 10) -> Dict[str, Any]:
        """Analyze topic coverage and identify gaps."""
        # Get relevant documents
        docs = self.vector_store.similarity_search(query, k=50)

        if not docs:
            return {"error": "No relevant documents found"}

        # Extract text content
        texts = [doc.page_content for doc in docs]

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(texts)

            # K-means clustering
            kmeans = KMeans(n_clusters=min(num_clusters, len(texts)), random_state=42)
            clusters = kmeans.fit_predict(tfidf_matrix)

            # Analyze clusters
            cluster_analysis = self._analyze_clusters(texts, clusters, vectorizer)

            # Calculate coverage scores
            keyword_coverage = self._calculate_keyword_coverage(texts)

            # Identify potential gaps
            gaps = self._identify_gaps(cluster_analysis, keyword_coverage)

            return {
                "topic_clusters": cluster_analysis,
                "keyword_coverage": keyword_coverage,
                "potential_gaps": gaps,
                "total_documents": len(docs),
                "coverage_score": self._calculate_overall_coverage_score(keyword_coverage)
            }

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def _analyze_clusters(self, texts: List[str], clusters: np.ndarray, vectorizer) -> List[Dict]:
        """Analyze document clusters to identify topics."""
        cluster_info = []
        feature_names = vectorizer.get_feature_names_out()

        for cluster_id in np.unique(clusters):
            cluster_docs = [texts[i] for i in range(len(texts)) if clusters[i] == cluster_id]
            cluster_size = len(cluster_docs)

            # Get top terms for this cluster
            cluster_texts = " ".join(cluster_docs)
            cluster_vectorizer = TfidfVectorizer(max_features=10, stop_words='english')

            try:
                cluster_tfidf = cluster_vectorizer.fit_transform([cluster_texts])
                top_terms = cluster_vectorizer.get_feature_names_out()

                cluster_info.append({
                    "cluster_id": int(cluster_id),
                    "size": cluster_size,
                    "percentage": round((cluster_size / len(texts)) * 100, 2),
                    "top_terms": list(top_terms),
                    "representative_text": cluster_docs[0][:200] + "..." if cluster_docs else ""
                })
            except:
                cluster_info.append({
                    "cluster_id": int(cluster_id),
                    "size": cluster_size,
                    "percentage": round((cluster_size / len(texts)) * 100, 2),
                    "top_terms": [],
                    "representative_text": ""
                })

        return sorted(cluster_info, key=lambda x: x['size'], reverse=True)

    def _calculate_keyword_coverage(self, texts: List[str]) -> Dict[str, Dict]:
        """Calculate coverage of key hydrology concepts."""
        coverage = {}
        total_docs = len(texts)

        for keyword in self.hydrology_keywords:
            count = sum(1 for text in texts if keyword.lower() in text.lower())
            coverage[keyword] = {
                "document_count": count,
                "coverage_percentage": round((count / total_docs) * 100, 2) if total_docs > 0 else 0,
                "frequency": sum(text.lower().count(keyword.lower()) for text in texts)
            }

        return coverage

    def _identify_gaps(self, cluster_analysis: List[Dict], keyword_coverage: Dict) -> List[Dict]:
        """Identify potential knowledge gaps."""
        gaps = []

        # Gap 1: Under-represented topics (small clusters)
        small_clusters = [c for c in cluster_analysis if c['percentage'] < 5]
        if small_clusters:
            gaps.append({
                "gap_type": "Under-represented Topics",
                "description": "Topics with limited documentation",
                "details": [f"Cluster {c['cluster_id']}: {', '.join(c['top_terms'][:3])}" for c in small_clusters[:5]],
                "severity": "Medium"
            })

        # Gap 2: Missing key concepts
        low_coverage_keywords = [
            kw for kw, data in keyword_coverage.items() 
            if data['coverage_percentage'] < 10
        ]
        if low_coverage_keywords:
            gaps.append({
                "gap_type": "Sparse Keyword Coverage",
                "description": "Important hydrology concepts with limited coverage",
                "details": low_coverage_keywords[:10],
                "severity": "High"
            })

        # Gap 3: Potential interdisciplinary opportunities
        interdisciplinary_terms = ["machine learning", "artificial intelligence", "IoT", "blockchain", "social", "economic"]
        missing_interdisciplinary = []
        for term in interdisciplinary_terms:
            found = any(term.lower() in text.lower() for text in [str(cluster_analysis)])
            if not found:
                missing_interdisciplinary.append(term)

        if missing_interdisciplinary:
            gaps.append({
                "gap_type": "Interdisciplinary Opportunities",
                "description": "Potential areas for cross-domain research",
                "details": missing_interdisciplinary,
                "severity": "Low"
            })

        return gaps

    def _calculate_overall_coverage_score(self, keyword_coverage: Dict) -> float:
        """Calculate an overall coverage score (0-100)."""
        if not keyword_coverage:
            return 0.0

        total_coverage = sum(data['coverage_percentage'] for data in keyword_coverage.values())
        avg_coverage = total_coverage / len(keyword_coverage)
        return round(min(avg_coverage, 100.0), 2)

    def find_contradictions(self, query: str) -> List[Dict]:
        """Find potentially contradictory information."""
        docs = self.vector_store.similarity_search(query, k=20)

        if len(docs) < 2:
            return []

        contradictions = []

        # Look for contradictory patterns
        contradiction_patterns = [
            (r"\bincreas\w+", r"\bdecreas\w+"),
            (r"\bpositive\w*", r"\bnegative\w*"),
            (r"\bhigh\w*", r"\blow\w*"),
            (r"\beffective\w*", r"\bineffective\w*"),
            (r"\bsignificant\w*", r"\binsignificant\w*")
        ]

        for i, doc1 in enumerate(docs):
            for j, doc2 in enumerate(docs[i+1:], i+1):
                for pos_pattern, neg_pattern in contradiction_patterns:
                    pos_in_doc1 = bool(re.search(pos_pattern, doc1.page_content, re.IGNORECASE))
                    neg_in_doc1 = bool(re.search(neg_pattern, doc1.page_content, re.IGNORECASE))
                    pos_in_doc2 = bool(re.search(pos_pattern, doc2.page_content, re.IGNORECASE))
                    neg_in_doc2 = bool(re.search(neg_pattern, doc2.page_content, re.IGNORECASE))

                    if (pos_in_doc1 and neg_in_doc2) or (neg_in_doc1 and pos_in_doc2):
                        contradictions.append({
                            "doc1_source": doc1.metadata.get("source", "Unknown"),
                            "doc2_source": doc2.metadata.get("source", "Unknown"),
                            "pattern": f"{pos_pattern} vs {neg_pattern}",
                            "doc1_snippet": doc1.page_content[:200] + "...",
                            "doc2_snippet": doc2.page_content[:200] + "...",
                        })

        return contradictions[:5]  # Return top 5 contradictions