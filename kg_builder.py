import os
import json
import spacy
from collections import defaultdict
from typing import Dict, List, Any
import re

class RelationshipIdentifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common relationship patterns
        self.relationship_patterns = {
            # Action-based relationships
            "action": {
                "patterns": [
                    r"(\w+)\s+(?:is|are)\s+(?:used|utilized|employed)\s+(?:to|for)\s+(\w+)",
                    r"(\w+)\s+(?:helps|enables|allows)\s+(?:to|for)\s+(\w+)",
                    r"(\w+)\s+(?:causes|leads to|results in)\s+(\w+)",
                    r"(\w+)\s+(?:affects|impacts|influences)\s+(\w+)"
                ],
                "type": "action_relationship"
            },
            # Hierarchical relationships
            "hierarchical": {
                "patterns": [
                    r"(\w+)\s+(?:is|are)\s+(?:part of|component of|member of)\s+(\w+)",
                    r"(\w+)\s+(?:belongs to|falls under|categorized as)\s+(\w+)",
                    r"(\w+)\s+(?:is|are)\s+(?:a|an)\s+(\w+)"
                ],
                "type": "hierarchical_relationship"
            },
            # Temporal relationships
            "temporal": {
                "patterns": [
                    r"(\w+)\s+(?:before|after|during)\s+(\w+)",
                    r"(\w+)\s+(?:follows|precedes)\s+(\w+)",
                    r"(\w+)\s+(?:occurs|happens)\s+(?:before|after)\s+(\w+)"
                ],
                "type": "temporal_relationship"
            },
            # Spatial relationships
            "spatial": {
                "patterns": [
                    r"(\w+)\s+(?:in|at|on|near)\s+(\w+)",
                    r"(\w+)\s+(?:located|situated|positioned)\s+(?:in|at|on|near)\s+(\w+)"
                ],
                "type": "spatial_relationship"
            }
        }

    def find_relationships(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Group entities by sentence and section
        sent_map = defaultdict(list)
        section_map = defaultdict(list)
        for ent in entities:
            sent_map[ent['position']['sentence_index']].append(ent)
            section_map[ent['section']].append(ent)

        relationships = []

        # Co-occurrence in the same sentence
        for sent_idx, ents in sent_map.items():
            for i in range(len(ents)):
                for j in range(i+1, len(ents)):
                    relationships.append({
                        "source": ents[i]['text'],
                        "target": ents[j]['text'],
                        "type": "co_occurs_in_sentence",
                        "sentence_index": sent_idx,
                        "section": ents[i]['section'],
                        "source_type": ents[i]['type'],
                        "target_type": ents[j]['type']
                    })

        # Pattern-based relationships
        for ent in entities:
            context = ent.get('context', '').lower()
            doc = self.nlp(context)
            
            # Check each relationship pattern category
            for category, pattern_info in self.relationship_patterns.items():
                for pattern in pattern_info['patterns']:
                    matches = re.finditer(pattern, context, re.IGNORECASE)
                    for match in matches:
                        # Find other entities in the same context window
                        for other in entities:
                            if other == ent:
                                continue
                            if other['position']['sentence_index'] == ent['position']['sentence_index']:
                                relationships.append({
                                    "source": ent['text'],
                                    "target": other['text'],
                                    "type": pattern_info['type'],
                                    "sentence_index": ent['position']['sentence_index'],
                                    "section": ent['section'],
                                    "source_type": ent['type'],
                                    "target_type": other['type'],
                                    "context_snippet": ent['context'],
                                    "pattern_category": category
                                })

        return relationships

    def process_extracted_entities(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        nodes = []
        node_ids = {}
        
        # Create nodes from entities
        for idx, ent in enumerate(extracted_data['entities']):
            node_id = f"ent_{idx}"
            node_ids[(ent['text'], ent['type'], ent['section'], ent['position']['sentence_index'])] = node_id
            nodes.append({
                "id": node_id,
                "label": ent['text'],
                "type": ent['type'],
                "type_description": ent['type_description'],
                "section": ent['section'],
                "sentence_index": ent['position']['sentence_index'],
                "paragraph_index": ent['position']['paragraph_index'],
                "context": ent['context'],
                "sentiment": ent['sentiment']
            })

        # Find relationships between entities
        relationships = self.find_relationships(extracted_data['entities'])
        
        # Create edges from relationships
        edges = []
        for rel in relationships:
            source_id = next((n['id'] for n in nodes if n['label'] == rel['source'] 
                            and n['section'] == rel['section'] 
                            and n['sentence_index'] == rel['sentence_index']), None)
            target_id = next((n['id'] for n in nodes if n['label'] == rel['target'] 
                            and n['section'] == rel['section'] 
                            and n['sentence_index'] == rel['sentence_index']), None)
            
            if source_id and target_id:
                edges.append({
                    "source": source_id,
                    "target": target_id,
                    "type": rel['type'],
                    "section": rel['section'],
                    "sentence_index": rel['sentence_index'],
                    "source_type": rel['source_type'],
                    "target_type": rel['target_type'],
                    "context_snippet": rel.get('context_snippet', ''),
                    "pattern_category": rel.get('pattern_category', '')
                })

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "document_id": extracted_data['document_id'],
                "available_entity_types": extracted_data.get('available_entity_types', []),
                "relationship_patterns": list(self.relationship_patterns.keys())
            }
        }

def main():
    entity_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\entity_extractions"
    output_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\knowledge_graphs"
    os.makedirs(output_dir, exist_ok=True)
    identifier = RelationshipIdentifier()

    for filename in os.listdir(entity_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(entity_dir, filename)
            output_path = os.path.join(output_dir, f"kg_{filename}")
            with open(input_path, 'r', encoding='utf-8') as f:
                extracted_data = json.load(f)
            kg = identifier.process_extracted_entities(extracted_data)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(kg, f, indent=2, ensure_ascii=False)
            print(f"Knowledge graph written: {output_path}")

if __name__ == "__main__":
    main() 