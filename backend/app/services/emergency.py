from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from app.core.config import (
    TWILIO_ACCOUNT_SID, 
    TWILIO_AUTH_TOKEN, 
    TWILIO_FROM_NUMBER, 
    EMERGENCY_CONTACT
)


CRISIS_HELPLINES = """
CRISIS HELPLINES:
- USA: 988 (Suicide & Crisis Lifeline)
- UK: 116 123 (Samaritans)
- Canada: 1-833-456-4566
- Australia: 13 11 14 (Lifeline)

If in immediate danger, call your local emergency number (911, 999, 112).
"""


def create_emergency_twiml() -> str:
    """Create TwiML for emergency call voice message."""
    response = VoiceResponse()
    response.say(
        "This is an urgent message from AI Therapist. "
        "Someone you care about may be experiencing a mental health crisis "
        "and needs your support right now. "
        "Please reach out to them immediately. "
        "This is not a test. Please call them back as soon as possible.",
        voice="alice",
        language="en-US"
    )
    response.pause(length=1)
    response.say(
        "Again, please contact them immediately. They need you.",
        voice="alice",
        language="en-US"
    )
    return str(response)


def call_emergency() -> str:
    """Place emergency call to trusted contact via Twilio API."""
    try:
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT]):
            return (
                f"Emergency calling not configured. Please reach out for help:\n{CRISIS_HELPLINES}"
            )
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        twiml = create_emergency_twiml()
        
        call = client.calls.create(
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER,
            twiml=twiml
        )
        
        print(f"[EMERGENCY] Call initiated - SID: {call.sid}")
        
        return (
            "💚 I've reached out to someone who cares about you. Help is coming.\n\n"
            "While we wait, I want you to know:\n"
            "• You are not alone in this\n"
            "• These feelings can get better with support\n"
            "• Reaching out was brave - I'm proud of you\n\n"
            "I'm here with you. Let's take some slow, deep breaths together. "
            "Breathe in... and out... You're doing great.\n\n"
            f"If you need immediate support:{CRISIS_HELPLINES}"
        )
        
    except Exception as e:
        print(f"[ERROR] Emergency call failed: {e}")
        return (
            "I couldn't connect the call, but please don't give up. "
            f"You deserve support. Please reach out:{CRISIS_HELPLINES}"
        )
