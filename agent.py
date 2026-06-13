import requests
import uuid
from db import save_message, create_ticket, get_conversation

NVIDIA_API_KEY = "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"
URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def get_response(user_input, session_id):
    try:
        history = get_conversation(session_id)

        # ✅ prevent fake memory answers
        if len(history) == 0 and "previous" in user_input.lower():
            return "No previous conversation exists in this session."

        save_message(session_id, "user", user_input)

        # ✅ improved ticket detection
        if any(word in user_input.lower() for word in 
               ["refund", "damaged", "issue", "problem", "broken", "wrong"]):
            ticket_id = str(uuid.uuid4())[:8]
            create_ticket(ticket_id, session_id, user_input)

        history = get_conversation(session_id)

        messages = [{"role": "system", "content": "You are a helpful support agent."}]

        for role, msg in history[-6:]:
            messages.append({"role": role, "content": msg})

        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta/llama-4-maverick-17b-128e-instruct",
            "messages": messages
        }

        res = requests.post(URL, headers=headers, json=payload, verify=False)
        data = res.json()

        if "choices" not in data:
            return f"Error: {data}"

        reply = data["choices"][0]["message"]["content"]

        save_message(session_id, "assistant", reply)

        return reply

    except Exception as e:
        return f"Error: {str(e)}"