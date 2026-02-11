function send() {
  const qInput = document.getElementById("q");
  const q = qInput.value;

  if (!q) return;

  add("You", q);

  fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question: q
    })
  })
  .then(response => response.json())
  .then(data => {
    add("Bot", data.answer);
  })
  .catch(error => {
    add("Bot", "Error connecting to server.");
    console.error(error);
  });

  qInput.value = "";
}

function add(sender, msg) {
  const box = document.getElementById("messages");
  box.innerHTML += `<div class="${sender}"><b>${sender}:</b> ${msg}</div>`;
  box.scrollTop = box.scrollHeight;
}
