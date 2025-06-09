import os
import json
import spacy
from collections import defaultdict
from typing import Dict, List, Set, Any
from pathlib import Path

class CategoryEntityMapper:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Define entity types to extract
        self.target_entities = {
            'ORG': 'Organizations',
            'PERSON': 'People',
            'GPE': 'Geopolitical Entities',
            'LOC': 'Locations',
            'PRODUCT': 'Products',
            'EVENT': 'Events',
            'WORK_OF_ART': 'Works of Art',
            'LAW': 'Laws',
            'LANGUAGE': 'Languages',
            'DATE': 'Dates',
            'PERCENT': 'Percentages',
            'MONEY': 'Monetary Values',
            'QUANTITY': 'Quantities',
            'ORDINAL': 'Ordinal Numbers',
            'CARDINAL': 'Cardinal Numbers'
        }
        
        # Define category-entity relationships
        self.category_entity_relationships = {
            'title': ['ORG', 'PERSON', 'PRODUCT', 'EVENT'],
            'abstract': ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT', 'EVENT'],
            'introduction': ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT', 'EVENT'],
            'methodology': ['ORG', 'PERSON', 'PRODUCT', 'QUANTITY', 'PERCENT'],
            'results': ['QUANTITY', 'PERCENT', 'MONEY', 'ORDINAL', 'CARDINAL'],
            'conclusion': ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT', 'EVENT'],
            'references': ['ORG', 'PERSON', 'WORK_OF_ART', 'LAW'],
            'keywords': ['PRODUCT', 'EVENT', 'LANGUAGE'],
            'authors': ['PERSON', 'ORG'],
            'institution': ['ORG', 'GPE', 'LOC'],
            'general_content': ['ORG', 'PERSON', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'QUANTITY', 'PERCENT']
        }

    def extract_entities(self, text: str) -> Dict[str, Set[str]]:
        """Extract entities from text using spaCy."""
        entities = defaultdict(set)
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in self.target_entities:
                entities[ent.label_].add(ent.text.strip())
        
        return entities

    def process_category(self, category_name: str, category_content: Any) -> Dict[str, Set[str]]:
        """Process a category and extract its entities."""
        entities = defaultdict(set)
        
        if isinstance(category_content, str):
            # Process single string
            category_entities = self.extract_entities(category_content)
            for entity_type, entity_set in category_entities.items():
                if entity_type in self.category_entity_relationships.get(category_name, []):
                    entities[entity_type].update(entity_set)
        
        elif isinstance(category_content, list):
            # Process list of strings
            for content in category_content:
                category_entities = self.extract_entities(content)
                for entity_type, entity_set in category_entities.items():
                    if entity_type in self.category_entity_relationships.get(category_name, []):
                        entities[entity_type].update(entity_set)
        
        return entities

    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a document and create category-entity mapping."""
        category_entity_map = {
            'document_id': document['document_id'],
            'category_entities': {},
            'entity_categories': defaultdict(list),
            'entity_relationships': defaultdict(list)
        }
        
        # Process each category
        for category_name, category_content in document['categories'].items():
            if category_content:  # Skip empty categories
                entities = self.process_category(category_name, category_content)
                if entities:
                    category_entity_map['category_entities'][category_name] = {
                        entity_type: list(entity_set)
                        for entity_type, entity_set in entities.items()
                    }
                    
                    # Build reverse mapping (entity -> categories)
                    for entity_type, entity_list in entities.items():
                        for entity in entity_list:
                            category_entity_map['entity_categories'][entity].append(category_name)
        
        # Build entity relationships
        for entity, categories in category_entity_map['entity_categories'].items():
            for category in categories:
                if category in category_entity_map['category_entities']:
                    for entity_type, related_entities in category_entity_map['category_entities'][category].items():
                        for related_entity in related_entities:
                            if related_entity != entity:
                                category_entity_map['entity_relationships'][entity].append({
                                    'related_entity': related_entity,
                                    'relationship_type': f'co-occurs_in_{category}',
                                    'category': category
                                })
        
        return category_entity_map

def main():
    # Define paths
    json_dir = r"C:\Users\mduba\Development\projects\ai\nlp\RAG\ciroh_x\json_output"
    output_dir = r"C:\Users\mduba\Development\projects\ai\nlp\RAG\ciroh_x\entity_maps"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize mapper
    mapper = CategoryEntityMapper()
    
    # Process all JSON files
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(json_dir, filename)
            output_filename = f"entity_map_{filename}"
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # Load document
                with open(input_path, 'r', encoding='utf-8') as f:
                    document = json.load(f)
                
                # Process document
                entity_map = mapper.process_document(document)
                
                # Save entity map
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(entity_map, f, indent=2, ensure_ascii=False)
                
                print(f"Successfully processed {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main() 