import spacy

# Load English tokenizer, POS tagger, parser, NER
nlp = spacy.load('en_core_web_sm')

categories = ['Terrorism/Protest', 'Positive/Uplifting', 'Natural Disasters', 'Others']

def classify_category(text):
    # Simple keyword-based classification (can be extended with ML models)
    doc = nlp(text)
    if 'terrorism' in text or 'protest' in text:
        return 'Terrorism/Protest'
    elif 'happy' in text or 'uplifting' in text:
        return 'Positive/Uplifting'
    elif 'earthquake' in text or 'flood' in text:
        return 'Natural Disasters'
    else:
        return 'Others'
