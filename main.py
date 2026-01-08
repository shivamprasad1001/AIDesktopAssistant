# main.py

import joblib
import json
import inspect
from datetime import datetime
import pyttsx3
import speech_recognition as sr


from utils.handler import (
    handle_set_reminder,
    handle_get_reminder,
    handle_open_app,
    WallpaperHandler,
    Notepad,
    Calculator

)
from nlu.simple_ner_model.ner import predict_entities
from utils.voice import VoiceAssistant

INTENT_TO_FUNCTION = {
    "set_reminder": handle_set_reminder,
    "get_reminder": handle_get_reminder,
    "open_app": handle_open_app,
    'change_wallpaper': WallpaperHandler,
    'open_notepad': Notepad,
    'open_calculator': Calculator,

    

    # ...
}

# import voice class from utils -> voice.py
voice  = VoiceAssistant()


# Load intent classifier
intent_model = joblib.load("nlu/intent_classifier_emmo0.1.joblib")


def predict_intent(user_input):
    intent = intent_model.predict([user_input])[0]
    return intent


def dispatch_intent(intent, entities, user_id="shivam"):
    handler = INTENT_TO_FUNCTION.get(intent)

    if handler:
        sig = inspect.signature(handler)
        if len(sig.parameters) == 0:
            return handler()
        else:
            return handler(entities, user_id)

    return " Sorry, I don't understand that command."



def assistant_loop():
    print(" Hello! I'm your assistant. Type something (type 'exit' to quit).")

    while True:
        user_input = voice.listen()
        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit']:
            print(" Goodbye!")
            break

        intent = predict_intent(user_input)
        print(f"Intent: {intent}")
        entities = predict_entities(user_input)  # From your NER model
        print(f"Entities: {entities}")
        
        response  = dispatch_intent(intent, entities )
        voice.speak(response)
       



if __name__ == "__main__":
    assistant_loop()

