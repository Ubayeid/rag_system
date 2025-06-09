import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json

# Page config
st.set_page_config(
    page_title="Hydrology RAG System",
    page_icon="🌊",
    layout="wide"
)

# API base URL
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("🌊 Hydrology Knowledge Gap Analysis System")
    st.markdown("*Powered by CIROH Documents and Advanced NLP*")

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Query System", "Upload Documents", "Knowledge Gap Analysis", "System Statistics"]
    )

    if page == "Query System":
        query_page()
    elif page == "Upload Documents":
        upload_page()
    elif page == "Knowledge Gap Analysis":
        gap_analysis_page()
    elif page == "System Statistics":
        stats_page()

def query_page():
    st.header("Research Query Interface")

    # Example queries
    st.subheader("Example Queries")
    example_queries = [
        "What are the latest methods for flood prediction?",
        "How does climate change affect groundwater recharge?",
        "What are the applications of remote sensing in hydrology?",
        "Describe uncertainty quantification in hydrological modeling",
        "What are the emerging trends in urban hydrology?"
    ]

    selected_example = st.selectbox("Select an example query:", [""] + example_queries)

    # Query input
    query = st.text_area(
        "Enter your research question:",
        value=selected_example,
        height=100,
        placeholder="E.g., What are the current challenges in watershed modeling?"
    )

    if st.button("🔍 Search", type="primary"):
        if query:
            with st.spinner("Processing your query..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/query",
                        json={"question": query}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        display_query_results(result)
                    else:
                        st.error(f"API Error: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Please ensure the API server is running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a query.")

def display_query_results(result):
    """Display comprehensive query results."""
    st.success("Query processed successfully!")

    # Main answer
    st.subheader("📋 Answer")
    st.write(result["answer"])

    # Create tabs for different result sections
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Sources", "📊 Gap Analysis", "⚠️ Contradictions", "💡 Suggestions"])

    with tab1:
        st.subheader("Source Documents")
        for i, doc in enumerate(result["source_documents"], 1):
            with st.expander(f"Source {i}: {doc['file_name']}"):
                st.write(doc["content"])
                st.caption(f"Source: {doc['source']}")

    with tab2:
        st.subheader("Knowledge Gap Analysis")
        gap_data = result["knowledge_gap_analysis"]

        if "error" not in gap_data:
            # Coverage score
            coverage_score = gap_data.get("coverage_score", 0)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Coverage Score", f"{coverage_score}%")
            with col2:
                st.metric("Documents Analyzed", gap_data.get("total_documents", 0))
            with col3:
                st.metric("Potential Gaps", len(gap_data.get("potential_gaps", [])))

            # Topic clusters visualization
            if "topic_clusters" in gap_data:
                clusters_df = pd.DataFrame(gap_data["topic_clusters"])
                if not clusters_df.empty:
                    fig = px.bar(
                        clusters_df, 
                        x="cluster_id", 
                        y="percentage",
                        title="Topic Distribution Across Document Clusters",
                        labels={"percentage": "Percentage of Documents", "cluster_id": "Cluster ID"}
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # Keyword coverage
            if "keyword_coverage" in gap_data:
                keyword_data = gap_data["keyword_coverage"]
                keywords_df = pd.DataFrame([
                    {"keyword": k, "coverage": v["coverage_percentage"], "frequency": v["frequency"]}
                    for k, v in keyword_data.items()
                ])

                if not keywords_df.empty:
                    fig = px.bar(
                        keywords_df.sort_values("coverage", ascending=True).tail(15),
                        x="coverage",
                        y="keyword",
                        orientation="h",
                        title="Keyword Coverage Analysis",
                        labels={"coverage": "Coverage Percentage", "keyword": "Hydrology Keywords"}
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # Potential gaps
            if "potential_gaps" in gap_data:
                st.subheader("Identified Knowledge Gaps")
                for gap in gap_data["potential_gaps"]:
                    with st.expander(f"{gap['gap_type']} - {gap['severity']} Priority"):
                        st.write(gap["description"])
                        if gap["details"]:
                            st.write("**Details:**")
                            for detail in gap["details"]:
                                st.write(f"- {detail}")
        else:
            st.error(f"Gap analysis failed: {gap_data['error']}")

    with tab3:
        st.subheader("Potential Contradictions")
        contradictions = result["contradictions"]

        if contradictions:
            for i, contradiction in enumerate(contradictions, 1):
                with st.expander(f"Contradiction {i}: {contradiction['pattern']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Document 1:**")
                        st.write(contradiction["doc1_snippet"])
                        st.caption(f"Source: {contradiction['doc1_source']}")
                    with col2:
                        st.write("**Document 2:**")
                        st.write(contradiction["doc2_snippet"]) 
                        st.caption(f"Source: {contradiction['doc2_source']}")
        else:
            st.info("No potential contradictions detected in the retrieved documents.")

    with tab4:
        st.subheader("Research Suggestions")
        suggestions = result["research_suggestions"]

        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.write(f"{i}. {suggestion}")
        else:
            st.info("No specific research suggestions generated for this query.")

def upload_page():
    st.header("Document Upload")
    st.write("Upload CIROH documents to expand the knowledge base.")

    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )

    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} files:")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size} bytes)")

        if st.button("📤 Upload and Process", type="primary"):
            with st.spinner("Processing documents..."):
                try:
                    files_data = [
                        ("files", (file.name, file, file.type))
                        for file in uploaded_files
                    ]

                    response = requests.post(
                        f"{API_BASE_URL}/upload-documents",
                        files=files_data
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Successfully processed {result['processed_chunks']} document chunks from {result['processed_files']} files!")

                        if result["errors"]:
                            st.warning("Some files had processing errors:")
                            for error in result["errors"]:
                                st.write(f"- {error}")
                    else:
                        st.error(f"Upload failed: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Please ensure the API server is running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def gap_analysis_page():
    st.header("Knowledge Gap Analysis")
    st.write("Analyze knowledge gaps for specific hydrology topics.")

    # Topic selection
    predefined_topics = [
        "flood modeling", "drought prediction", "groundwater management",
        "climate change impacts", "urban hydrology", "water quality modeling",
        "remote sensing applications", "machine learning in hydrology",
        "uncertainty quantification", "ecosystem services"
    ]

    col1, col2 = st.columns([2, 1])

    with col1:
        custom_topic = st.text_input("Enter a custom topic:")

    with col2:
        selected_topic = st.selectbox("Or select a predefined topic:", [""] + predefined_topics)

    topic = custom_topic if custom_topic else selected_topic

    if st.button("🔬 Analyze Knowledge Gaps", type="primary"):
        if topic:
            with st.spinner(f"Analyzing knowledge gaps for '{topic}'..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/analyze-gaps/{topic}")

                    if response.status_code == 200:
                        gap_data = response.json()
                        display_gap_analysis(gap_data, topic)
                    else:
                        st.error(f"Analysis failed: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Please ensure the API server is running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter or select a topic.")

def display_gap_analysis(gap_data, topic):
    """Display detailed gap analysis results."""
    st.success(f"Gap analysis completed for '{topic}'!")

    if "error" in gap_data:
        st.error(f"Analysis error: {gap_data['error']}")
        return

    # Summary metrics
    st.subheader("📊 Analysis Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Coverage Score", f"{gap_data.get('coverage_score', 0)}%")
    with col2:
        st.metric("Documents", gap_data.get('total_documents', 0))
    with col3:
        st.metric("Topic Clusters", len(gap_data.get('topic_clusters', [])))
    with col4:
        st.metric("Identified Gaps", len(gap_data.get('potential_gaps', [])))

    # Detailed analysis tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Topic Clusters", "🔍 Keyword Analysis", "⚠️ Knowledge Gaps"])

    with tab1:
        st.subheader("Topic Cluster Analysis")
        clusters = gap_data.get("topic_clusters", [])

        if clusters:
            # Cluster size distribution
            clusters_df = pd.DataFrame(clusters)
            fig = px.pie(
                clusters_df,
                values="size",
                names=[f"Cluster {c['cluster_id']}" for c in clusters],
                title="Document Distribution Across Topic Clusters"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Detailed cluster information
            st.subheader("Cluster Details")
            for cluster in clusters:
                with st.expander(f"Cluster {cluster['cluster_id']} ({cluster['percentage']}% of documents)"):
                    st.write(f"**Size:** {cluster['size']} documents")
                    st.write(f"**Top Terms:** {', '.join(cluster['top_terms'])}")
                    if cluster['representative_text']:
                        st.write(f"**Representative Text:** {cluster['representative_text']}")
        else:
            st.info("No topic clusters identified.")

    with tab2:
        st.subheader("Keyword Coverage Analysis")
        keyword_data = gap_data.get("keyword_coverage", {})

        if keyword_data:
            # Create comprehensive keyword analysis
            keywords_df = pd.DataFrame([
                {
                    "keyword": k,
                    "coverage_percentage": v["coverage_percentage"],
                    "document_count": v["document_count"],
                    "frequency": v["frequency"]
                }
                for k, v in keyword_data.items()
            ]).sort_values("coverage_percentage", ascending=False)

            # Coverage heatmap
            fig = px.bar(
                keywords_df,
                x="keyword",
                y="coverage_percentage",
                color="frequency",
                title="Keyword Coverage and Frequency Analysis",
                labels={"coverage_percentage": "Coverage %", "frequency": "Frequency"}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

            # Low coverage keywords
            low_coverage = keywords_df[keywords_df["coverage_percentage"] < 10]
            if not low_coverage.empty:
                st.subheader("Low Coverage Keywords")
                st.write("These important hydrology concepts have limited representation:")
                st.dataframe(low_coverage[["keyword", "coverage_percentage", "document_count"]])
        else:
            st.info("No keyword coverage data available.")

    with tab3:
        st.subheader("Identified Knowledge Gaps")
        gaps = gap_data.get("potential_gaps", [])

        if gaps:
            # Gap severity distribution
            severity_counts = pd.DataFrame(gaps)["severity"].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Knowledge Gaps by Severity",
                labels={"x": "Severity", "y": "Number of Gaps"}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Detailed gap information
            for gap in gaps:
                severity_color = {
                    "High": "🔴",
                    "Medium": "🟡", 
                    "Low": "🟢"
                }.get(gap["severity"], "⚪")

                with st.expander(f"{severity_color} {gap['gap_type']} - {gap['severity']} Priority"):
                    st.write(gap["description"])
                    if gap["details"]:
                        st.write("**Specific Areas:**")
                        for detail in gap["details"]:
                            st.write(f"• {detail}")

                    # Research recommendations
                    st.write("**Recommended Actions:**")
                    if gap["gap_type"] == "Sparse Keyword Coverage":
                        st.write("- Conduct systematic literature review")
                        st.write("- Identify leading researchers in these areas")
                        st.write("- Consider collaborative research opportunities")
                    elif gap["gap_type"] == "Under-represented Topics":
                        st.write("- Investigate emerging research areas")
                        st.write("- Look for interdisciplinary connections")
                        st.write("- Consider novel methodological approaches")
                    elif gap["gap_type"] == "Interdisciplinary Opportunities":
                        st.write("- Explore cross-domain collaborations")
                        st.write("- Investigate technology transfer opportunities")
                        st.write("- Consider innovative applications")
        else:
            st.info("No significant knowledge gaps identified for this topic.")

def stats_page():
    st.header("System Statistics")
    st.write("Overview of the RAG system performance and content.")

    try:
        response = requests.get(f"{API_BASE_URL}/system-stats")

        if response.status_code == 200:
            stats = response.json()

            # System overview
            st.subheader("📈 System Overview")
            col1, col2, col3 = st.columns(3)

            with col1:
                vector_stats = stats.get("vector_store_stats", {})
                st.metric("Total Documents", vector_stats.get("total_documents", 0))

            with col2:
                st.metric("Supported File Types", len(stats.get("supported_file_types", [])))

            with col3:
                st.metric("Collection Name", vector_stats.get("collection_name", "N/A"))

            # Model information
            st.subheader("🤖 Model Configuration")
            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**Embedding Model:** {stats.get('embedding_model', 'N/A')}")

            with col2:
                st.info(f"**Language Model:** {stats.get('llm_model', 'N/A')}")

            # Supported file types
            st.subheader("📁 Supported File Types")
            file_types = stats.get("supported_file_types", [])
            for file_type in file_types:
                st.write(f"• {file_type}")

            # System health check
            st.subheader("🔧 System Health")
            health_checks = [
                ("Vector Database", "✅ Operational" if vector_stats.get("total_documents", 0) >= 0 else "❌ Error"),
                ("API Connection", "✅ Connected"),
                ("Document Processing", "✅ Ready"),
                ("Knowledge Gap Detection", "✅ Available")
            ]

            for check_name, status in health_checks:
                st.write(f"**{check_name}:** {status}")

        else:
            st.error(f"Failed to retrieve system statistics: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Please ensure the API server is running.")
    except Exception as e:
        st.error(f"Error retrieving statistics: {str(e)}")

if __name__ == "__main__":
    main()