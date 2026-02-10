function send() {
  const q = document.getElementById("q").value;
  if (!q) return;

  add("You", q);

  fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({question: q})
  })
  .then(r => r.json())
  .then(d => add("Bot", d.answer));
}

function add(sender, msg) {
  const box = document.getElementById("messages");
  box.innerHTML += `<div class="${sender}"><b>${sender}:</b> ${msg}</div>`;
  box.scrollTop = box.scrollHeight;
}
