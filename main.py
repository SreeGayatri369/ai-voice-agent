from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from agent import get_response
from db import get_all_tickets, update_ticket, get_conversation

# ✅ Twilio imports
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client

import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Static UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def user_ui():
    return FileResponse("static/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

# ================= CHAT API =================

class Query(BaseModel):
    user_input: str
    session_id: str

@app.post("/query")
def query(q: Query):
    return {"reply": get_response(q.user_input, q.session_id)}

# ================= DASHBOARD APIs =================

@app.get("/tickets")
def tickets():
    return {"tickets": get_all_tickets()}

@app.post("/update_ticket")
def update(data: dict):
    update_ticket(data["ticket_id"], data["status"])
    return {"status": "updated"}

@app.get("/conversation/{session_id}")
def conversation(session_id: str):
    return {"messages": get_conversation(session_id)}

# ================= ✅ TWILIO VOICE =================

@app.post("/voice")
async def voice(request: Request):
    form = await request.form()

    user_input = form.get("SpeechResult")
    call_sid = form.get("CallSid")

    response = VoiceResponse()

    # ✅ FIRST TIME CALL (no user speech yet)
    if not user_input:
        gather = Gather(
            input="speech",
            action="https://ai-voice-agent-b6ms.onrender.com/voice",  # ✅ FIXED (absolute URL)
            method="POST"
        )
        gather.say("Hello, welcome to AI support. How can I help you today?")
        response.append(gather)

        return Response(str(response), media_type="application/xml")

    # ✅ AFTER USER SPEAKS
    ai_reply = get_response(user_input, call_sid)

    gather = Gather(
        input="speech",
        action="https://ai-voice-agent-b6ms.onrender.com/voice",  # ✅ FIXED
        method="POST"
    )
    gather.say(ai_reply)
    response.append(gather)

    return Response(str(response), media_type="application/xml")

# ================= ✅ CALL TRIGGER =================

@app.get("/call_me")
def call_me():
    try:
        account_sid = "AC9512f01f604b0f3da9cadb70bdbc61d6"
        auth_token = "1d7fb4c63c6f7d5543eafa0aa8f7a9bd"

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to="+919866704458",   # ✅ your number
            from_="+19452454328", # ✅ Twilio number
            url="https://ai-voice-agent-b6ms.onrender.com/voice"
        )

        return {"status": "calling started", "call_sid": call.sid}

    except Exception as e:
        return {"error": str(e)}
