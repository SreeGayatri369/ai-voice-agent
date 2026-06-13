import streamlit as st
import requests

st.title("📊 Admin Dashboard")

if st.button("Load Tickets"):
    res = requests.get("http://127.0.0.1:8000/tickets")
    data = res.json()

    for t in data["tickets"]:
        st.write(f"Ticket: {t[0]}")
        st.write(f"Issue: {t[2]}")
        st.write(f"Status: {t[3]}")

        if st.button(f"View {t[0]}"):
            conv = requests.get(f"http://127.0.0.1:8000/conversation/{t[1]}")
            messages = conv.json()["messages"]

            for m in messages:
                st.write(f"{m[0]}: {m[1]}")