# app.py
from dotenv import load_dotenv
import os

# 1. Load env variables before importing other local modules
load_dotenv()

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import threading
import time
import sys

try:
    from ai_handler import get_ai_response, get_full_conversation, clear_conversation
    from summarizer import summarize_call
    from notes_manager import save_note
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)

app = Flask(__name__)

# 2. Ensure Twilio credentials exist
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# ─────────────────────────────────────────────
# ROUTE 1: Jab call aaye — pehla response
# ─────────────────────────────────────────────
@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    """Twilio isko call aane pe hit karta hai"""
    
    caller = request.form.get("From", "Unknown")
    call_sid = request.form.get("CallSid", "")
    
    print(f"\n📞 Call aaya: {caller} (SID: {call_sid})")
    
    # Pehla AI message lo
    first_message = get_ai_response(call_sid, "CALL_STARTED")
    
    # TwiML response banao
    response = VoiceResponse()
    
    # AI bolega aur phir caller ki baat sunne ke liye Gather use karein
    gather = Gather(
        input="speech",           # Voice input lo
        action=f"/handle-speech", # Jawab ke baad is URL pe jao
        timeout=5,                # 5 second silence ke baad submit karo
        speech_timeout="auto",    # Automatically detect karo
        language="hi-IN"          # Hindi pehle (ya en-IN English ke liye)
    )
    
    gather.say(first_message, voice="Polly.Aditi", language="hi-IN")
    
    response.append(gather)
    
    # Agar kuch nahi bola toh
    response.say("Main aapki awaaz nahi sun paaya. Please call back karein.", 
                 voice="Polly.Aditi", language="hi-IN")
    
    return Response(str(response), mimetype="text/xml")


# ─────────────────────────────────────────────
# ROUTE 2: Caller ne kuch bola — process karo
# ─────────────────────────────────────────────
@app.route("/handle-speech", methods=["POST"])
def handle_speech():
    """Caller ke speech ko AI se process karo"""
    
    caller = request.form.get("From", "Unknown")
    call_sid = request.form.get("CallSid", "")
    speech_result = request.form.get("SpeechResult", "")
    
    print(f"🗣️ Caller bola: {speech_result}")
    
    response = VoiceResponse()
    
    # Agar kuch nahi bola
    if not speech_result:
        gather = Gather(
            input="speech",
            action="/handle-speech",
            timeout=5,
            speech_timeout="auto",
            language="hi-IN"
        )
        gather.say("Kya aap wahan hain? Please baat karein.", 
                   voice="Polly.Aditi", language="hi-IN")
        response.append(gather)
        return Response(str(response), mimetype="text/xml")
    
    # AI se jawab lo
    ai_reply = get_ai_response(call_sid, speech_result)
    print(f"🤖 AI bola: {ai_reply}")
    
    # Conversation khatam karne ke signals
    end_signals = ["dhanyawad", "thank you", "bye", "alvida", "ok bye", "theek hai"]
    should_end = any(signal in speech_result.lower() for signal in end_signals)
    
    if should_end:
        response.say(ai_reply + " Dhanyawad! Main aapka message note kar lunga. Namaste!", 
                     voice="Polly.Aditi", language="hi-IN")
        response.hangup()
        
        # Background mein notes save karo
        threading.Thread(
            target=save_call_notes, 
            args=(call_sid, caller)
        ).start()
        
    else:
        # Continue conversation
        gather = Gather(
            input="speech",
            action="/handle-speech",
            timeout=5,
            speech_timeout="auto",
            language="hi-IN"
        )
        gather.say(ai_reply, voice="Polly.Aditi", language="hi-IN")
        response.append(gather)
        
        # Agar caller ne kuch nahi bola toh end karo
        response.redirect("/end-call")
    
    return Response(str(response), mimetype="text/xml")


# ─────────────────────────────────────────────
# ROUTE 3: Call khatam — notes save karo
# ─────────────────────────────────────────────
@app.route("/end-call", methods=["POST"])
def end_call():
    """Call khatam hone pe notes save karo"""
    
    call_sid = request.form.get("CallSid", "")
    caller = request.form.get("From", "Unknown")
    
    response = VoiceResponse()
    response.say("Bahut shukriya aapka. Main aapka message note kar lunga. Namaste!", 
                 voice="Polly.Aditi", language="hi-IN")
    response.hangup()
    
    # Background mein notes save karo
    threading.Thread(
        target=save_call_notes, 
        args=(call_sid, caller)
    ).start()
    
    return Response(str(response), mimetype="text/xml")


# ─────────────────────────────────────────────
# Helper: Notes save karne ka function
# ─────────────────────────────────────────────
def save_call_notes(call_sid: str, caller: str):
    """Background mein transcript + summary save karo"""
    
    print(f"\n💾 Notes save karna shuru... (SID: {call_sid})")
    
    # Conversation history se transcript nikalo
    transcript = get_full_conversation(call_sid)
    
    # AI se summary banwao
    print("📝 Summary bana raha hai...")
    summary = summarize_call(transcript, caller)
    
    # Notes file mein save karo
    saved_path = save_note(caller, summary, transcript)
    print(f"✅ Notes saved at: {saved_path}")
    
    # Memory clear karo
    clear_conversation(call_sid)


# ─────────────────────────────────────────────
# Server Start
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 AI Call Agent Server start ho raha hai...")
    print("📂 Notes saved in: notes/call_notes.md")
    app.run(debug=True, port=5000)