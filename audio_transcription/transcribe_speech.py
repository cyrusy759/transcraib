import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.effects import normalize
import os
import whisper

class SpeechTranscriber:
    def __init__(self):
        self.raw_audio_path = "audio_store.wav"
        self.processed_audio_path = "processed_audio.wav"
        self.model = whisper.load_model("tiny")
    
    def record_speech(self):
        """Record speech from microphone and save to file"""
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... (3 seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            print("Speak now! (Max 30 seconds)")
            
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=30)
                print("Saving recording...")
                
                with open(self.raw_audio_path, "wb") as f:
                    f.write(audio.get_wav_data())
                
                return True
                
            except sr.WaitTimeoutError:
                print("No speech detected. Try again.")
                return False
            except Exception as e:
                print(f"Error: {str(e)}")
                return False
    
    def preprocess_audio(self):
        """Process the recorded audio for better transcription"""
        if not os.path.exists(self.raw_audio_path):
            print("Error: Invalid audio file path")
            return False
            
        try:
            print("Processing audio...")
            audio = AudioSegment.from_wav(self.raw_audio_path)
            
            audio = normalize(audio)
            audio = audio.low_pass_filter(3000)
            audio = audio.high_pass_filter(200)
            audio = audio.set_frame_rate(16000)
            
            audio.export(self.processed_audio_path, format="wav")
            print(f"Saved processed audio to {self.processed_audio_path}")
            return True
            
        except Exception as e:
            print(f"Processing failed: {str(e)}")
            return False
    
    def transcribe(self):
        """Execute full transcription pipeline"""
        if not self.record_speech():
            return None
            
        if not self.preprocess_audio():
            return None
            
        try:
            result_text = self.model.transcribe(self.processed_audio_path, fp16=False)
            return result_text["text"]
        except Exception as e:
            print(f"Transcription failed: {str(e)}")
            return None
