async function sendMsg() {
  const q = document.getElementById("question").value;

  const form = new FormData();
  form.append("query", q);

  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    body: form
  });

  const data = await res.json();
  document.getElementById("reply").innerText = data.answer;
}
