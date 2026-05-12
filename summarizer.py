# summarizer.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in summarizer.py")
client = OpenAI(api_key=api_key)

def summarize_call(transcript: str, caller_number: str) -> str:
    """Transcript ki concise summary banata hai"""
    
    if not transcript or len(transcript.strip()) < 10:
        return "Call mein koi meaningful conversation nahi hui."
    
    prompt = f"""
Ek phone call ki transcript hai jisme ek AI agent ne mere behalf pe call li.
Caller ka number: {caller_number}

Transcript:
{transcript}

Mujhe iska concise summary do:
1. Caller kaun tha / kya kaam tha
2. Kya information li/di gayi
3. Koi important action item hai toh batao
4. Summary Hindi ya English mein de sakte ho

Summary:
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ye sasta aur fast hai
        messages=[
            {"role": "system", "content": "Aap ek helpful assistant ho jo phone call summaries banate ho."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content