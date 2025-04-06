from groq import Groq
from dotenv import load_dotenv
from audio_transcription.transcribe_speech import SpeechTranscriber
import os
import sys
import json

load_dotenv()

class GroqChatBot:
    def __init__(self):
        self._client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self._available_methods = {
            "question": self.question_user,
            "translation": self.translation,
            "summarization": self.summarize,
            "flashcard": self.make_flash_card,
            "sentiment_analysis": self.sentiment_analysis,
            "goodbye": self.farewell
        }

    def question_user (self):
        print("Please ask a question")
        record = SpeechTranscriber()
        text = record.transcribe()
        if not text:
            print("Please try again")
            return self.question_user()

        prompt = f"""Analyze this request and respond ONLY with the methods key:
        
        Available actions: {list(self._available_methods.keys())}
        Request: "{text}"

        Respond ONLY with the action key
        """
        try:
            response = self._client.chat.completions.create(
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

    def make_flash_card(self):
        try:
            count = input("Please input the number of flashcards you want to make")
            print("Please read out the text you want to make flash cards for, after the system gets ready")
            record = SpeechTranscriber()
            text = record.transcribe()
            prompt = f"""Create {count} flashcards from this text: {text}
            Format each flashcard as a VALID JSON array like this:
            [
                {{
                    "title": "Example Title",
                    "question": "Example Question",
                    "answer": "Example Answer"
                }}
            ]               
            Return ONLY the JSON, no extra text.
            """
            response = self.get_groq_response(prompt)
            flashcards = json.loads(response)
            
            print("\nGenerated Flashcards:")
            for card in flashcards:
                print(f"\nTitle: {card['title']}")
                print(f"Q: {card['question']}")
                print(f"A: {card['answer']}")
                
            print("Do you have any other questions?")
            return self.question_user()
            
        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()
    
    def summarize(self):
        try:
            print("Please read out the text you want to summarize, after the system gets ready")
            record = SpeechTranscriber()
            text = record.transcribe()
            prompt = f""" Summarize the text of {text} """
            
            response = self.get_groq_response(prompt)
            print(response)
            print("Do you have any other questions?")
            return self.question_user()
        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()
    
    def translation(self):
        try:
            language = input("Please input the language you want to translate the text into")
            print("Please read out the text you want to translate, after the system gets ready")
            record = SpeechTranscriber()
            text = record.transcribe()
            prompt = f""" Translate the text of {text} into the language {language}
            """
            
            response = self.get_groq_response(prompt)
            print(response)
            print("Do you have any other questions?")
            return self.question_user()
            
        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()

    def sentiment_analysis(self):
        try:
            print("Please read out the text you want to summarize, after the system gets ready")
            record = SpeechTranscriber()
            text = record.transcribe()
            prompt = f""" Perform sentiment analysis on the text of {text} """
            
            response = self.get_groq_response(prompt)
            print(response)
            print("Do you have any other questions?")
            return self.question_user()

        except Exception as e:
            print(f"Groq error {e}, please ask another question")
            return self.question_user()

    def get_groq_response(self, prompt):
        response = self._client.chat.completions.create(
            model="llama3-70b-8192", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content

    def farewell(self):
        print("Thanks for using Transcraib, goodbye!")
        sys.exit()