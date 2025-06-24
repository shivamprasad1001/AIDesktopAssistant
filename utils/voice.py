import speech_recognition as sr
import pyttsx3

class VoiceAssistant:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)  # Speed of speech
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print(f"🧠 Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, prompt=None):
        if prompt:
            self.speak(prompt)

        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.listener.adjust_for_ambient_noise(source)
            audio = self.listener.listen(source)

        try:
            command = self.listener.recognize_google(audio)
            print(f"👂 You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak(" Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            self.speak("⚠️ Speech service is unavailable.")
            return None
