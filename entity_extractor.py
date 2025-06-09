import os
import json
import spacy
from collections import defaultdict
from typing import Dict, List, Set, Any, Tuple
from pathlib import Path

class EntityExtractor:
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

    def get_context(self, doc: spacy.tokens.Doc, entity: spacy.tokens.Span, window_size: int = 5) -> str:
        """Extract context around an entity."""
        start = max(0, entity.start - window_size)
        end = min(len(doc), entity.end + window_size)
        return doc[start:end].text.strip()

    def extract_entities_with_context(self, text: str, category: str) -> List[Dict[str, Any]]:
        """Extract entities with their context and metadata."""
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in self.target_entities:
                entity_info = {
                    'text': ent.text.strip(),
                    'type': ent.label_,
                    'type_description': self.target_entities[ent.label_],
                    'start_char': ent.start_char,
                    'end_char': ent.end_char,
                    'context': self.get_context(doc, ent),
                    'category': category,
                    'sentiment': self.analyze_sentiment(doc, ent),
                    'position': {
                        'sentence_index': self.get_sentence_index(doc, ent),
                        'paragraph_index': self.get_paragraph_index(text, ent.start_char)
                    }
                }
                entities.append(entity_info)
        
        return entities

    def analyze_sentiment(self, doc: spacy.tokens.Doc, entity: spacy.tokens.Span) -> Dict[str, float]:
        """Analyze sentiment around the entity."""
        # Simple sentiment analysis based on surrounding context
        context = self.get_context(doc, entity, window_size=10)
        context_doc = self.nlp(context)
        
        # Count positive and negative words (simplified approach)
        positive_words = {'good', 'great', 'excellent', 'positive', 'successful', 'effective', 'improved', 'better'}
        negative_words = {'bad', 'poor', 'negative', 'failed', 'problem', 'issue', 'difficult', 'worse'}
        
        pos_count = sum(1 for token in context_doc if token.text.lower() in positive_words)
        neg_count = sum(1 for token in context_doc if token.text.lower() in negative_words)
        total = pos_count + neg_count
        
        if total == 0:
            return {'positive': 0.5, 'negative': 0.5}
        
        return {
            'positive': pos_count / total,
            'negative': neg_count / total
        }

    def get_sentence_index(self, doc: spacy.tokens.Doc, entity: spacy.tokens.Span) -> int:
        """Get the index of the sentence containing the entity."""
        for i, sent in enumerate(doc.sents):
            if entity.start >= sent.start and entity.end <= sent.end:
                return i
        return -1

    def get_paragraph_index(self, text: str, char_index: int) -> int:
        """Get the index of the paragraph containing the character position."""
        paragraphs = text.split('\n\n')
        current_pos = 0
        for i, para in enumerate(paragraphs):
            current_pos += len(para) + 2  # +2 for the '\n\n'
            if char_index < current_pos:
                return i
        return -1

    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a document and extract entities with their context."""
        extracted_data = {
            'document_id': document['document_id'],
            'entities': [],
            'entity_statistics': defaultdict(int),
            'category_statistics': defaultdict(lambda: defaultdict(int))
        }
        
        # Process each category
        for category, content in document['categories'].items():
            if not content:
                continue
                
            # Handle both string and list content
            if isinstance(content, str):
                texts = [content]
            else:
                texts = content
            
            for text in texts:
                entities = self.extract_entities_with_context(text, category)
                extracted_data['entities'].extend(entities)
                
                # Update statistics
                for entity in entities:
                    extracted_data['entity_statistics'][entity['type']] += 1
                    extracted_data['category_statistics'][category][entity['type']] += 1
        
        # Convert statistics to regular dict for JSON serialization
        extracted_data['entity_statistics'] = dict(extracted_data['entity_statistics'])
        extracted_data['category_statistics'] = {
            cat: dict(stats) for cat, stats in extracted_data['category_statistics'].items()
        }
        
        return extracted_data

def main():
    # Define paths
    json_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\json_output"
    output_dir = r"C:\Users\mduba\Development\projects\ai\hybrid\RAG\rag_system\entity_extractions"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize extractor
    extractor = EntityExtractor()
    
    # Process all JSON files
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(json_dir, filename)
            output_filename = f"entities_{filename}"
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # Load document
                with open(input_path, 'r', encoding='utf-8') as f:
                    document = json.load(f)
                
                # Process document
                extracted_data = extractor.process_document(document)
                
                # Save extracted data
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted_data, f, indent=2, ensure_ascii=False)
                
                print(f"Successfully processed {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main() 