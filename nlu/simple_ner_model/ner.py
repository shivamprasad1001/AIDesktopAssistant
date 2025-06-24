# nlu/simple_ner_model/ner.py


import spacy
from pathlib import Path


# Load the trained spaCy model
MODEL_PATH = Path("nlu/simple_ner_model")  # adjust if needed
nlp = spacy.load(MODEL_PATH)


def predict_entities(text):
    doc = nlp(text)
    print(doc)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_.lower()] = ent.text
    return entities
