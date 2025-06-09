import os
import json
from neo4j import GraphDatabase
from typing import Dict, Any, List, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('neo4j_import.log'),
        logging.StreamHandler()
    ]
)

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

# Path to your knowledge graph JSON files
KG_DIR = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\knowledge_graphs"

def validate_kg_data(kg: Dict[str, Any]) -> bool:
    """Validate the knowledge graph data structure."""
    required_keys = {'nodes', 'edges'}
    if not all(key in kg for key in required_keys):
        logging.error(f"Missing required keys in knowledge graph: {required_keys - set(kg.keys())}")
        return False
    
    if not isinstance(kg['nodes'], list) or not isinstance(kg['edges'], list):
        logging.error("Nodes and edges must be lists")
        return False
    
    # Validate node structure
    required_node_keys = {'id', 'label', 'type', 'section'}
    for node in kg['nodes']:
        if not all(key in node for key in required_node_keys):
            logging.error(f"Invalid node structure: {node}")
            return False
    
    # Validate edge structure
    required_edge_keys = {'source', 'target', 'type', 'section'}
    for edge in kg['edges']:
        if not all(key in edge for key in required_edge_keys):
            logging.error(f"Invalid edge structure: {edge}")
            return False
    
    return True

def create_constraints(session):
    """Create constraints for the graph database."""
    try:
        # Create constraints for Entity nodes
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Section) REQUIRE s.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:EntityType) REQUIRE t.name IS UNIQUE")
        logging.info("Successfully created database constraints")
    except Exception as e:
        logging.error(f"Error creating constraints: {str(e)}")
        raise

def create_entity_type_nodes(session, entity_types: List[str]):
    """Create nodes for entity types."""
    try:
        for type_name in entity_types:
            session.run(
                """
                MERGE (t:EntityType {name: $name})
                """,
                name=type_name
            )
        logging.info(f"Created {len(entity_types)} entity type nodes")
    except Exception as e:
        logging.error(f"Error creating entity type nodes: {str(e)}")
        raise

def create_section_nodes(session, sections: Set[str]):
    """Create nodes for document sections."""
    try:
        for section in sections:
            session.run(
                """
                MERGE (s:Section {name: $name})
                """,
                name=section
            )
        logging.info(f"Created {len(sections)} section nodes")
    except Exception as e:
        logging.error(f"Error creating section nodes: {str(e)}")
        raise

def import_kg_to_neo4j(driver, kg_path: str):
    """Import knowledge graph data into Neo4j."""
    try:
        with open(kg_path, 'r', encoding='utf-8') as f:
            kg = json.load(f)
        
        # Validate knowledge graph data
        if not validate_kg_data(kg):
            raise ValueError(f"Invalid knowledge graph data in {kg_path}")
        
        nodes = kg['nodes']
        edges = kg['edges']
        metadata = kg.get('metadata', {})
        
        with driver.session() as session:
            # Create constraints
            create_constraints(session)
            
            # Create entity type nodes if available
            if 'available_entity_types' in metadata:
                create_entity_type_nodes(session, metadata['available_entity_types'])
            
            # Get unique sections
            sections = {node['section'] for node in nodes}
            create_section_nodes(session, sections)
            
            # Create entity nodes
            for node in nodes:
                try:
                    session.run(
                        """
                        MERGE (e:Entity {id: $id})
                        SET e.label = $label,
                            e.type = $type,
                            e.type_description = $type_description,
                            e.sentence_index = $sentence_index,
                            e.paragraph_index = $paragraph_index,
                            e.context = $context,
                            e.sentiment_positive = $sentiment_positive,
                            e.sentiment_negative = $sentiment_negative
                        WITH e
                        MATCH (s:Section {name: $section})
                        MERGE (e)-[:BELONGS_TO]->(s)
                        WITH e
                        MATCH (t:EntityType {name: $type})
                        MERGE (e)-[:IS_TYPE]->(t)
                        """,
                        id=node['id'],
                        label=node['label'],
                        type=node['type'],
                        type_description=node.get('type_description', ''),
                        sentence_index=node['sentence_index'],
                        paragraph_index=node['paragraph_index'],
                        context=node['context'],
                        sentiment_positive=node.get('sentiment', {}).get('positive', 0.5),
                        sentiment_negative=node.get('sentiment', {}).get('negative', 0.5),
                        section=node['section']
                    )
                except Exception as e:
                    logging.error(f"Error creating entity node {node['id']}: {str(e)}")
                    continue
            
            # Create relationships
            for edge in edges:
                try:
                    session.run(
                        """
                        MATCH (a:Entity {id: $source}), (b:Entity {id: $target})
                        MERGE (a)-[r:RELATION {
                            type: $type,
                            section: $section,
                            sentence_index: $sentence_index,
                            source_type: $source_type,
                            target_type: $target_type,
                            context_snippet: $context_snippet,
                            pattern_category: $pattern_category
                        }]->(b)
                        """,
                        source=edge['source'],
                        target=edge['target'],
                        type=edge['type'],
                        section=edge['section'],
                        sentence_index=edge['sentence_index'],
                        source_type=edge['source_type'],
                        target_type=edge['target_type'],
                        context_snippet=edge.get('context_snippet', ''),
                        pattern_category=edge.get('pattern_category', '')
                    )
                except Exception as e:
                    logging.error(f"Error creating relationship {edge['source']}->{edge['target']}: {str(e)}")
                    continue
            
            logging.info(f"Successfully imported knowledge graph from {kg_path}")
            
    except Exception as e:
        logging.error(f"Error importing knowledge graph from {kg_path}: {str(e)}")
        raise

def main():
    """Main function to import all knowledge graphs."""
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        # Verify connection
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            if not result.single():
                raise Exception("Could not connect to Neo4j database")
        
        logging.info("Connected to Neo4j database successfully!")
        
        # Process all knowledge graph files
        for filename in os.listdir(KG_DIR):
            if filename.endswith('.json'):
                logging.info(f"Importing {filename}...")
                import_kg_to_neo4j(driver, os.path.join(KG_DIR, filename))
        
        logging.info("Import complete! Open Neo4j Browser to explore your knowledge graph.")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.close()

if __name__ == "__main__":
    main()