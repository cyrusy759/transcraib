from groq import Groq
from dotenv import load_dotenv
from audio_transcription.transcribe_speech import transcribe_audio
import os

load_dotenv()

class GroqChatBot:
    def __init__(self):
        self._client = Groq(os.getenv("GROQ_API_KEY"))
        self._available_methods = {
            "question": self.question_user,
            "translation": "language_translation",
            "summarization": "text_summarization",
            "flashcard": "make_flash_card",
            "analysis": "sentiment_analysis",
            "goodbye": "farewell"
        }
        self._text = ""

    def execute_based_on_input(self, command):
        groq_method = self._available_methods.get(command.lower())
        if command == "flashcard":
            number = input("Please input the number of flashcards you want to make")
            print("please read the piece of text you want to make flashcards for")
            text = transcribe_audio()
            return self.make_flash_card(text, number)

    def question_user (self):
        text = transcribe_audio()
        prompt = f"""Analyze this request and respond ONLY with the methods key:
        
        Available actions: {list(self._available_methods.keys())}
        Request: "{text}"

        Respond ONLY with the action key
        """

        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
        )
            key = response.choices[0].message.content.strip().lower()
            if key in self._available_methods:
                return self._available_methods[key]()
            else:
                print("We didn't quite catch that, please ask the question again")
                return self.question_user()
        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()

    def make_flash_card(self, text, number):
        prompt = f""" Create flash cards 
        
        """
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
        )
            text = response.choices[0].message.content
            
        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()
    
    