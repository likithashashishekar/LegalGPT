import re
import json
from collections import Counter

class LegalBiasDetector:
    def __init__(self):
        self.bias_patterns = {
            'demographic': {
                'gender_biased_terms': ['he/she', 'him/her', 'his/her', 'businessman', 'chairman'],
                'racial_terms': ['ethnicity', 'race', 'color', 'national origin'],
                'disability_terms': ['disabled', 'handicapped', 'impaired']
            },
            'legal_bias': {
                'jurisdictional': ['only in', 'exclusive to', 'not applicable to'],
                'temporal': ['current law', 'modern interpretation', 'historical context']
            }
        }
    
    def detect_demographic_bias(self, text):
        """Detect potential demographic bias in legal text"""
        bias_flags = {}
        text_lower = text.lower()
        
        # Gender bias detection
        gender_terms = [' he ', ' she ', ' him ', ' her ', ' his ', ' hers ']
        gender_counts = {term: text_lower.count(term) for term in gender_terms}
        
        total_gender_refs = sum(gender_counts.values())
        if total_gender_refs > 0:
            male_refs = sum(gender_counts.get(term, 0) for term in [' he ', ' him ', ' his '])
            female_refs = sum(gender_counts.get(term, 0) for term in [' she ', ' her ', ' hers '])
            
            if male_refs > female_refs * 2 or female_refs > male_refs * 2:
                bias_flags['gender_imbalance'] = {
                    'male_references': male_refs,
                    'female_references': female_refs,
                    'score': abs(male_refs - female_refs) / total_gender_refs if total_gender_refs > 0 else 0
                }
        
        return bias_flags
    
    def detect_legal_bias(self, text):
        """Detect legal-specific biases"""
        bias_flags = {}
        text_lower = text.lower()
        
        # Jurisdictional bias
        jurisdictional_terms = self.bias_patterns['legal_bias']['jurisdictional']
        found_terms = [term for term in jurisdictional_terms if term in text_lower]
        
        if found_terms:
            bias_flags['jurisdictional_bias'] = {
                'found_terms': found_terms,
                'severity': 'medium'
            }
        
        return bias_flags
    
    def comprehensive_bias_scan(self, text):
        """Run complete bias analysis"""
        if not text:
            return {"error": "No text provided"}
            
        results = {
            'demographic_bias': self.detect_demographic_bias(text),
            'legal_bias': self.detect_legal_bias(text),
            'overall_bias_score': 0.0
        }
        
        # Calculate overall bias score
        bias_indicators = 0
        if results['demographic_bias']:
            bias_indicators += 1
        if results['legal_bias']:
            bias_indicators += 1
            
        results['overall_bias_score'] = bias_indicators / 2
        
        return results

# Test bias detection
if __name__ == "__main__":
    detector = LegalBiasDetector()
    
    test_text = "The defendant, being a foreign national, shall be treated differently according to current law. He shall have limited rights compared to citizens."
    bias_results = detector.comprehensive_bias_scan(test_text)
    
    print("Bias Detection Results:")
    print(json.dumps(bias_results, indent=2))
