import os
import json
import spacy
from collections import defaultdict
from typing import Dict, List, Any

class RelationshipIdentifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # Define relationship keywords and types
        self.relationship_keywords = {
            "validated by": "validated_by",
            "measured in": "measured_in",
            "addresses gap": "addresses_gap",
            "calibrated using": "calibrated_using",
            "analyzed using": "analyzed_using",
            "suggests": "suggests",
            "influenced by": "influenced_by",
            "applies to": "applies_to",
            "related to": "related_to",
            "affiliated with": "affiliated_with",
            "tested using": "tested_using",
            "solves": "solves",
            "assesses": "assesses"
        }

    def find_relationships(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Group entities by sentence and paragraph
        sent_map = defaultdict(list)
        para_map = defaultdict(list)
        for ent in entities:
            sent_map[ent['position']['sentence_index']].append(ent)
            para_map[ent['position']['paragraph_index']].append(ent)

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
                        "category": ents[i]['category']
                    })

        # Context-based relationships
        for ent in entities:
            context = ent.get('context', '').lower()
            for keyword, rel_type in self.relationship_keywords.items():
                if keyword in context:
                    # Find other entities in the same context window
                    for other in entities:
                        if other == ent:
                            continue
                        if other['position']['sentence_index'] == ent['position']['sentence_index']:
                            relationships.append({
                                "source": ent['text'],
                                "target": other['text'],
                                "type": rel_type,
                                "sentence_index": ent['position']['sentence_index'],
                                "category": ent['category'],
                                "context_snippet": ent['context']
                            })
        return relationships

    def process_extracted_entities(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        nodes = []
        node_ids = {}
        for idx, ent in enumerate(extracted_data['entities']):
            node_id = f"ent_{idx}"
            node_ids[(ent['text'], ent['type'], ent['category'], ent['position']['sentence_index'])] = node_id
            nodes.append({
                "id": node_id,
                "label": ent['text'],
                "type": ent['type'],
                "category": ent['category'],
                "sentence_index": ent['position']['sentence_index'],
                "paragraph_index": ent['position']['paragraph_index'],
                "context": ent['context']
            })

        relationships = self.find_relationships(extracted_data['entities'])
        edges = []
        for rel in relationships:
            source_id = next((n['id'] for n in nodes if n['label'] == rel['source'] and n['category'] == rel['category'] and n['sentence_index'] == rel['sentence_index']), None)
            target_id = next((n['id'] for n in nodes if n['label'] == rel['target'] and n['category'] == rel['category'] and n['sentence_index'] == rel['sentence_index']), None)
            if source_id and target_id:
                edges.append({
                    "source": source_id,
                    "target": target_id,
                    "type": rel['type'],
                    "category": rel['category'],
                    "sentence_index": rel['sentence_index'],
                    "context_snippet": rel.get('context_snippet', '')
                })

        return {
            "nodes": nodes,
            "edges": edges
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