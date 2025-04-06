import speech_recognition as sr
import pyaudio

def transcribe_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... (please wait)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening to speech you have 1 minute to speak")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing your speech...")
            
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return text