import re
import spacy
from langdetect import detect, DetectorFactory
import nltk
from nltk.tokenize import sent_tokenize

DetectorFactory.seed = 0

class LegalTextPreprocessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy English model not available")
            self.nlp = None
    
    def clean_legal_text(self, text):
        """Clean and normalize legal text"""
        if not text:
            return ""
            
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s§¶©®@#$%&*()\-=+\[\]{}|;:,.<>?/]', '', text)
        return text.strip()
    
    def detect_language(self, text):
        """Detect language of legal text"""
        try:
            return detect(text)
        except:
            return "en"
    
    def extract_legal_entities(self, text):
        """Extract legal entities using spaCy"""
        if not self.nlp or not text:
            return {"entities": "Not available"}
            
        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [], 
            'LAW': [],
            'DATE': [],
            'GPE': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities

    def process_document(self, document):
        """Process a single legal document"""
        text = document.get('text', '')
        
        processed = {
            'original_text': text,
            'cleaned_text': self.clean_legal_text(text),
            'language': self.detect_language(text),
            'entities': self.extract_legal_entities(text),
            'type': document.get('type', 'unknown'),
            'jurisdiction': document.get('jurisdiction', 'unknown')
        }
        
        return processed

    def process_batch(self, documents):
        """Process multiple legal documents"""
        processed_docs = []
        
        for doc in documents:
            processed_docs.append(self.process_document(doc))
        
        return processed_docs

# Test the preprocessor
if __name__ == "__main__":
    preprocessor = LegalTextPreprocessor()
    
    sample_docs = [
        {
            "text": "This Agreement is made on January 1, 2024 between John Doe and ABC Corporation in New York.", 
            "type": "contract",
            "jurisdiction": "US"
        }
    ]
    
    processed = preprocessor.process_batch(sample_docs)
    print("Processed document sample:")
    print(processed[0])
