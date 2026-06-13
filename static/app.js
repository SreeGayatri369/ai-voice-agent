let session_id = Math.random().toString(36);

function addMessage(text, sender) {
  document.getElementById("chat").innerHTML +=
    `<p><b>${sender}:</b> ${text}</p>`;
}

async function sendMessage(text) {
  addMessage(text, "You");

  const res = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_input: text,
      session_id,
    }),
  });

  const data = await res.json();

  addMessage(data.reply, "Agent");

  speak(data.reply);
}

function sendText() {
  const input = document.getElementById("textInput");
  if (!input.value) return;

  sendMessage(input.value);
  input.value = "";
}

function startListening() {
  const rec = new webkitSpeechRecognition();

  rec.onresult = (e) => {
    sendMessage(e.results[0][0].transcript);
  };

  rec.start();
}

function speak(text) {
  speechSynthesis.speak(new SpeechSynthesisUtterance(text));
}
