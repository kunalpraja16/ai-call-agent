# transcriber.py
import requests
import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ Warning: OPENAI_API_KEY missing in transcriber.py")

openai_client = OpenAI(api_key=api_key) if api_key else None
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def transcribe_recording(recording_url: str) -> str:
    """Twilio recording URL se audio download karo aur text mein convert karo"""
    
    try:
        # Recording download karo (authentication ke saath)
        auth = (
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        
        audio_response = requests.get(recording_url + ".mp3", auth=auth)
        
        if audio_response.status_code != 200:
            return f"Recording download nahi hui (Status: {audio_response.status_code})"
        
        # Temporary file mein save karo
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(audio_response.content)
            tmp_path = tmp_file.name
        
        # OpenAI Whisper se transcribe karo
        with open(tmp_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="hi"  # Hindi ke liye, ya "en" English ke liye
            )
        
        # Temp file delete karo
        os.unlink(tmp_path)
        
        return transcription.text
        
    except Exception as e:
        print(f"Transcription error: {e}")
        return f"Transcription fail hui: {str(e)}"
    