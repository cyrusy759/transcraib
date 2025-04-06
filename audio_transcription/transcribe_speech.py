import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub.effects import normalize
import os
import whisper

def record_speech():
    recognizer = sr.Recognizer()
    raw_audio_path = "audio_store.wav"
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... (3 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print("Speak now! (Max 10 seconds)")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Saving recording...")
            
            with open(raw_audio_path, "wb") as f:
                f.write(audio.get_wav_data())
            
            return raw_audio_path
            
        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

def preprocess_audio(input_path):
    if not input_path or not os.path.exists(input_path):
        print("Error: Invalid audio file path")
        return False
        
    try:
        print("Processing audio...")
        audio = AudioSegment.from_wav(input_path)
        
        audio = normalize(audio)
        audio = audio.low_pass_filter(3000)  # Reduce high-frequency noise
        audio = audio.high_pass_filter(200)  # Reduce low-frequency rumble
        audio = audio.set_frame_rate(16000)   # Standard sample rate
        
        output_path = "processed_audio.wav"
        audio.export(output_path, format="wav")
        print(f"Saved processed audio to {output_path}")
        return True
        
    except Exception as e:
        print(f"Processing failed: {str(e)}")
        return False
    
def transcribe_audio():
    model = whisper.load_model("base")
    result_text = model.transcribe("processed_audio.wav", fp16=False)
    print(result_text["text"])

