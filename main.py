from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, Conversation
from schemas import UserCreate, ChatRequest
from auth import hash_password, verify_password, create_access_token
from chat import generate_ai_response, save_message

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chat Platform (SQLite Version)")


# -------------------------
# USER REGISTER
# -------------------------
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}


# -------------------------
# LOGIN
# -------------------------
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token}


# -------------------------
# CREATE CONVERSATION
# -------------------------
@app.post("/conversation")
def create_conversation(user_id: int, db: Session = Depends(get_db)):

    conv = Conversation(user_id=user_id, title="New Chat")
    db.add(conv)
    db.commit()
    db.refresh(conv)

    return conv


# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    # Save user message
    save_message(db, req.conversation_id, "user", req.message)

    # Generate AI response
    response = generate_ai_response(req.message)

    # Save AI message
    save_message(db, req.conversation_id, "assistant", response)

    return {
        "response": response
    }