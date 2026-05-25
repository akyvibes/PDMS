from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chatbot_reply(data: ChatRequest):

    user_message = data.message.lower()

    # SIMPLE AI RESPONSES
    if "hello" in user_message:
        reply = "Hello! How can I help you today?"

    elif "donation" in user_message:
        reply = "You can donate blood every 3 months if eligible."

    elif "tips" in user_message:
        reply = "Drink water, eat healthy, and rest well before donating blood."

    elif "hours" in user_message:
        reply = "Donation centers are usually open from 9 AM to 5 PM."

    elif "blood" in user_message:
        reply = "Blood donation helps save lives during emergencies and surgeries."
    
    elif "eligibility" in user_message:
        reply = "To be eligible to donate blood, you must be at least 18 years old, weigh at least 50 kg, and be in good health. You should not have donated blood in the last 3 months."

    else:
        reply = "I'm HemaAssist AI. Ask me about blood donation, camps, requests, or eligibility."

    

    return {
        "response": reply
    }