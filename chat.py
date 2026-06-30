from models import Message, Conversation

# THIS IS WHERE YOU CONNECT GPT / GEMINI / GROQ LATER


def generate_ai_response(user_message: str):
    """
    Placeholder AI logic.
    Replace this with OpenAI / Gemini / local model later.
    """
    return f"AI Response: You said -> {user_message}"


def save_message(db, conversation_id, role, content):
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg