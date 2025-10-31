import requests
import json
from datasets import load_dataset
import pandas as pd

class LegalDataCollector:
    def __init__(self):
        self.sources = {
            'english': ['case_law', 'contracts', 'statutes'],
            'multilingual': ['european_union', 'un_documents']
        }
    
    def download_sample_data(self):
        """Download sample legal datasets"""
        try:
            print("Downloading legal datasets...")
            
            # Try to load available legal datasets
            contracts = load_dataset("neil-code/contracts", split='train[:100]')
            legal_docs = load_dataset("joelito/legal_documents", split='train[:50]')
            
            return {
                'contracts': contracts,
                'legal_documents': legal_docs
            }
            
        except Exception as e:
            print(f"Dataset download failed: {e}")
            return self.create_sample_data()
    
    def create_sample_data(self):
        """Create comprehensive sample legal data"""
        print("Creating sample legal data...")
        
        sample_contracts = [
            {
                "text": "This Agreement is made and entered into as of January 1, 2024, between John Smith ('Party A') and ABC Corporation ('Party B'). Party A agrees to provide consulting services to Party B for the term of one year.",
                "language": "en",
                "type": "contract",
                "jurisdiction": "US"
            },
            {
                "text": "The employee shall not disclose any confidential information belonging to the company during or after the term of employment. This obligation survives termination of this agreement.",
                "language": "en", 
                "type": "contract",
                "jurisdiction": "US"
            }
        ]
        
        sample_case_law = [
            {
                "text": "The court held that the defendant's right to a fair trial was violated when evidence was improperly admitted. The conviction was reversed and the case remanded for a new trial.",
                "language": "en",
                "type": "case_law",
                "court": "Supreme Court"
            }
        ]
        
        return {
            'contracts': sample_contracts,
            'case_law': sample_case_law
        }

    def save_data(self, data, filename):
        """Save data to JSON file"""
        with open(f'data/raw/{filename}.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to data/raw/{filename}.json")

# Test the data collector
if __name__ == "__main__":
    collector = LegalDataCollector()
    legal_data = collector.download_sample_data()
    collector.save_data(legal_data, 'legal_corpora')
    print("Sample data collection completed!")
