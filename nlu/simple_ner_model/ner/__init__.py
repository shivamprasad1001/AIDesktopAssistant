# simple_ner_model/ner/__init__.py

import spacy

# Load the trained spaCy model
nlp = spacy.load("nlu/simple_ner_model")  # path to model dir

def predict_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_.lower()] = ent.text
    return entities
