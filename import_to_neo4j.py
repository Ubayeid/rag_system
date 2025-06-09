import os
import json
from neo4j import GraphDatabase

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

# Path to your knowledge graph JSON files
KG_DIR = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\knowledge_graphs"

def import_kg_to_neo4j(driver, kg_path):
    with open(kg_path, 'r', encoding='utf-8') as f:
        kg = json.load(f)
    nodes = kg['nodes']
    edges = kg['edges']

    with driver.session() as session:
        # Create nodes
        for node in nodes:
            session.run(
                """
                MERGE (e:Entity {id: $id})
                SET e.label = $label, e.type = $type, e.category = $category,
                    e.sentence_index = $sentence_index, e.paragraph_index = $paragraph_index,
                    e.context = $context
                """,
                id=node['id'],
                label=node['label'],
                type=node['type'],
                category=node['category'],
                sentence_index=node['sentence_index'],
                paragraph_index=node['paragraph_index'],
                context=node['context']
            )
        # Create relationships
        for edge in edges:
            session.run(
                """
                MATCH (a:Entity {id: $source}), (b:Entity {id: $target})
                MERGE (a)-[r:RELATION {type: $type, category: $category, sentence_index: $sentence_index, context_snippet: $context_snippet}]->(b)
                """,
                source=edge['source'],
                target=edge['target'],
                type=edge['type'],
                category=edge['category'],
                sentence_index=edge['sentence_index'],
                context_snippet=edge.get('context_snippet', '')
            )

if __name__ == "__main__":
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    for filename in os.listdir(KG_DIR):
        if filename.endswith('.json'):
            print(f"Importing {filename}...")
            import_kg_to_neo4j(driver, os.path.join(KG_DIR, filename))
    driver.close()
    print("Import complete! Open Neo4j Browser to explore your knowledge graph.")