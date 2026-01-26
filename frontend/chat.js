document.getElementById("username").innerText =
  localStorage.getItem("name") || "Student";

const chatBox = document.getElementById("chat-box");

async function sendMessage() {
  const input = document.getElementById("query");
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  // typing indicator
  const typing = addMessage("Thinking…", "bot typing");

  try {
    const res = await fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({ query: text })
    });

    const data = await res.json();
    typing.remove();

    addMessage(
      data.answer || "No relevant content found in uploaded documents.",
      "bot"
    );

  } catch (err) {
    typing.remove();
    addMessage("Server error. Please try again.", "bot");
  }
}

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = "message " + type;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

// Enter key support
document.getElementById("query").addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
window.onload = () => {
  addMessage(
    "Hello! Ask questions based on your uploaded college notes.",
    "bot"
  );
};
function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}
