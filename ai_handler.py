# ai_handler.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Please check your .env file.")
client = OpenAI(api_key=api_key)

# Conversation history store karne ke liye (simple in-memory)
conversations = {}

SYSTEM_PROMPT = """Aap ek professional AI assistant ho jo apne owner ke behalf pe phone calls handle karte ho.

Aapka naam "Assistant" hai. Owner abhi busy hai.

Guidelines:
- Professionally baat karo (Hindi ya English dono mein)
- Caller ka naam aur kaam zaroor poochho
- Important information note karo (kab call back karein, kya kaam hai)
- Politely baat karo
- Call zyada lamba mat karo - 2-3 minutes mein khatam karo
- Agar emergency ho toh owner ko message karne ka suggest karo

Shuru mein ye bolna: "Hello! Main [owner] ke AI assistant hoon. Abhi woh busy hain. Main aapka message note kar sakta hoon. Aap kaun bol rahe hain aur aapka kya kaam tha?"
"""

def get_ai_response(session_id: str, user_message: str) -> str:
    """AI se response lo"""
    
    # Conversation history initialize karo
    if session_id not in conversations:
        conversations[session_id] = []
    
    # User message add karo
    conversations[session_id].append({
        "role": "user",
        "content": user_message
    })
    
    # OpenAI se response lo
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversations[session_id]
        ],
        max_tokens=150
    )
    
    ai_reply = response.choices[0].message.content
    
    # AI response bhi history mein save karo
    conversations[session_id].append({
        "role": "assistant", 
        "content": ai_reply
    })
    
    return ai_reply

def get_full_conversation(session_id: str) -> str:
    """Poori conversation text mein do"""
    
    if session_id not in conversations:
        return "Koi conversation nahi mili."
    
    transcript_lines = []
    for msg in conversations[session_id]:
        role = "Caller" if msg["role"] == "user" else "AI Agent"
        transcript_lines.append(f"{role}: {msg['content']}")
    
    return "\n".join(transcript_lines)

def clear_conversation(session_id: str):
    """Session khatam hone pe conversation clear karo"""
    if session_id in conversations:
        del conversations[session_id]