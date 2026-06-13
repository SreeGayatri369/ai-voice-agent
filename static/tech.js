async function load() {
  const res = await fetch("/tickets");
  const data = await res.json();

  document.getElementById("tickets").innerHTML = data.tickets
    .map(
      (t) =>
        `${t[0]} - ${t[2]} - ${t[3]}
       <button onclick="update('${t[0]}','IN_PROGRESS')">Start</button>
       <button onclick="update('${t[0]}','COMPLETED')">Done</button>`,
    )
    .join("<br>");
}

async function update(id, status) {
  await fetch("/update_ticket", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticket_id: id, status }),
  });
  load();
}

load();
