For Beaverhacks 2025 by Cyrus

Transcraib is a speech to text AI assistant powered by Groq and OpenAI-whisper that works to help users translate, make flash cards, summarize and perform
sentiment analysis on real time audio. 

Prerequisites:
Python 3.9+
[Groq API key](https://console.groq.com/)
FFmpeg (for Whisper audio processing)

Installation:
Clone the repository:
```bash
git clone https://github.com/yourusername/transcraib.git
cd transcraib

Create and activate virtual environment:
python -m venv venv

For Windows
.\venv\Scripts\activate

For Mac
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Setup environmental variables
echo "GROQ_API_KEY=your_api_key_here" > .env

Run the application
python main.py
```
