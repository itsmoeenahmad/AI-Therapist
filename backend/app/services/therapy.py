from groq import Groq
from app.core.prompts import THERAPIST_PROMPT
from app.core.config import GROQ_API_KEY, THERAPEUTIC_MODEL, THERAPEUTIC_TEMPERATURE

def query_therapeutic_model(prompt: str) -> str:
    """Generate therapeutic response using Groq API with clinical psychology profile."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": THERAPIST_PROMPT},
                {"role": "user", "content": prompt}
            ],
            model=THERAPEUTIC_MODEL,
            temperature=THERAPEUTIC_TEMPERATURE,
            max_tokens=500,
            top_p=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"[ERROR] Therapeutic model error: {e}")
        return (
            "I'm experiencing technical difficulties right now, but your feelings matter. "
            "Please try again, or reach out to a crisis helpline if you need immediate support."
        )
