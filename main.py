# from fastapi import FastAPI
# from pydantic import BaseModel
# from agent import get_response
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# from db import get_all_tickets, update_ticket, get_conversation

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # ✅ Serve static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# def user_ui():
#     return FileResponse("static/index.html")

# @app.get("/dashboard")
# def dashboard():
#     return FileResponse("static/dashboard.html")

# # ✅ API
# class Query(BaseModel):
#     user_input: str
#     session_id: str

# @app.post("/query")
# def query(q: Query):
#     return {"reply": get_response(q.user_input, q.session_id)}

# @app.get("/tickets")
# def tickets():
#     return {"tickets": get_all_tickets()}

# @app.post("/update_ticket")
# def update(data: dict):
#     update_ticket(data["ticket_id"], data["status"])
#     return {"status": "updated"}

# @app.get("/conversation/{session_id}")
# def conversation(session_id: str):
#     return {"messages": get_conversation(session_id)}



from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import get_response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from db import get_all_tickets, update_ticket, get_conversation

# ✅ NEW (Twilio)
from twilio.twiml.voice_response import VoiceResponse, Gather

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Serve static UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def user_ui():
    return FileResponse("static/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")


# ✅ ========= EXISTING CHAT API =========
class Query(BaseModel):
    user_input: str
    session_id: str

@app.post("/query")
def query(q: Query):
    return {"reply": get_response(q.user_input, q.session_id)}


# ✅ ========= EXISTING DASHBOARD APIs =========
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


# ========== ✅ NEW: TWILIO VOICE HANDLER ==========

@app.post("/voice")
async def voice(request: Request):
    form = await request.form()

    # ✅ speech input from Twilio
    user_input = form.get("SpeechResult")

    # ✅ call session ID (critical for tracking)
    call_sid = form.get("CallSid")

    response = VoiceResponse()

    # ✅ FIRST CALL (no user input yet)
    if not user_input:
        gather = Gather(
            input="speech",
            action="/voice",
            method="POST"
        )
        gather.say("Hello, welcome to AI support. How can I help you today?")
        response.append(gather)

        return Response(content=str(response), media_type="application/xml")

    # ✅ PROCESS USER INPUT
    ai_reply = get_response(user_input, call_sid)

    # ✅ SPEAK RESPONSE
    gather = Gather(
        input="speech",
        action="/voice",
        method="POST"
    )
    gather.say(ai_reply)
    response.append(gather)

    return Response(content=str(response), media_type="application/xml")
from twilio.rest import Client

@app.get("/call_me")
def call_me():
    account_sid = "YOUR_ACCOUNT_SID"
    auth_token = "YOUR_AUTH_TOKEN"

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to="+919866704458",   # YOUR mobile number
        from_="+19452454328", # YOUR Twilio number
        url="https://ai-voice-agent-b6ms.onrender.com/voice"
    )

    return {"status": "calling"}