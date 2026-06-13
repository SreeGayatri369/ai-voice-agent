sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]