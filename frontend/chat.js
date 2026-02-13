async function send() {
    const q = document.getElementById("q").value;
    if (!q) return;

    add("You", q);

    try {
        const res = await fetch("https://college-chatbot-opdo.onrender.com", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: q
            })
        });

        const data = await res.json();

        add("Bot", data.answer);

    } catch (err) {
        add("Bot", "Error connecting to server");
    }

    document.getElementById("q").value = "";
}

function add(sender, msg) {
    const box = document.getElementById("messages");
    box.innerHTML += `<div><b>${sender}:</b> ${msg}</div>`;
    box.scrollTop = box.scrollHeight;
}


function add(sender, msg) {
  const box = document.getElementById("messages");
  box.innerHTML += `<div class="${sender}"><b>${sender}:</b> ${msg}</div>`;
  box.scrollTop = box.scrollHeight;
}
