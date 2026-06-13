let ticketsData = [];

async function loadTickets() {
  const res = await fetch("/tickets");
  const data = await res.json();

  ticketsData = data.tickets;

  render(ticketsData);
}

function render(tickets) {
  document.querySelectorAll(".column").forEach((col) => {
    col.innerHTML = `<h3>${col.id}</h3>`;
  });

  tickets.forEach((t) => {
    const card = document.createElement("div");
    card.className = "card";
    card.draggable = true;

    card.innerHTML = `
      <div class="card-title">${t[2]}</div>

      <div class="card-footer">
        <span class="badge">${t[0]}</span>
        <button onclick="view('${t[1]}')">View</button>
      </div>
    `;

    card.ondragstart = (e) => {
      e.dataTransfer.setData("id", t[0]);
    };

    document.getElementById(t[3]).appendChild(card);
  });
}

// ✅ drag-drop
document.querySelectorAll(".column").forEach((col) => {
  col.ondragover = (e) => e.preventDefault();

  col.ondrop = async (e) => {
    const id = e.dataTransfer.getData("id");

    await fetch("/update_ticket", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticket_id: id,
        status: col.id,
      }),
    });

    loadTickets();
  };
});

// ✅ modal view
async function view(session_id) {
  const res = await fetch(`/conversation/${session_id}`);
  const data = await res.json();

  const container = document.getElementById("conversation");

  container.innerHTML = data.messages
    .map((m) => `<p><b>${m[0]}:</b> ${m[1]}</p>`)
    .join("");

  document.getElementById("modal").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}

// ✅ search
function searchTickets() {
  const q = document.getElementById("searchBox").value.toLowerCase();

  const filtered = ticketsData.filter(
    (t) => t[2].toLowerCase().includes(q) || t[0].toLowerCase().includes(q),
  );

  render(filtered);
}

loadTickets();
