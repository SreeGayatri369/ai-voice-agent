async function loadTickets() {
  const res = await fetch("/tickets");
  const data = await res.json();

  document.getElementById("tickets").innerHTML = data.tickets
    .map(
      (t) =>
        `Ticket ${t[0]} | ${t[2]} | ${t[3]}
       <button onclick="view('${t[1]}')">View</button>`,
    )
    .join("<br>");
}

async function view(session_id) {
  const res = await fetch(`/conversation/${session_id}`);
  const data = await res.json();

  alert(data.messages.map((m) => m.join(": ")).join("\n"));
}
