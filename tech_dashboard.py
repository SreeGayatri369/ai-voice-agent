import streamlit as st
import requests

st.title("🧑‍💻 Tech Dashboard")

res = requests.get("http://127.0.0.1:8000/tickets")
data = res.json()

for t in data["tickets"]:
    st.write(f"{t[0]} - {t[2]} - {t[3]}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Start {t[0]}"):
            requests.post("http://127.0.0.1:8000/update_ticket",
                          json={"ticket_id": t[0], "status": "IN_PROGRESS"})

    with col2:
        if st.button(f"Complete {t[0]}"):
            requests.post("http://127.0.0.1:8000/update_ticket",
                          json={"ticket_id": t[0], "status": "COMPLETED"})
