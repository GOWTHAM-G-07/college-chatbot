function login() {
  fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    body: new URLSearchParams({
      email: email.value,
      password: password.value
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("name", data.name);
    window.location = "dashboard.html";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("name")) {
    document.getElementById("name").innerText =
      localStorage.getItem("name");
  }
});

function search() {
  fetch("http://127.0.0.1:8000/search", {
    method: "POST",
    body: new URLSearchParams({ query: query.value })
  })
  .then(res => res.json())
  .then(data => {
    results.innerHTML = data.results.join("<hr>");
  });
}
async function upload() {
  const data = new FormData();
  data.append("title", document.getElementById("title").value);
  data.append("file", document.getElementById("file").files[0]);

  await fetch("http://127.0.0.1:8000/admin/upload", {
    method: "POST",
    body: data
  });

  loadDocs();
}

async function loadDocs() {
  const res = await fetch("http://127.0.0.1:8000/admin/docs");
  const docs = await res.json();

  const ul = document.getElementById("docList");
  ul.innerHTML = "";

  docs.forEach(d => {
    ul.innerHTML += `
      <li>
        ${d.title}
        <button onclick="del(${d.id})">Delete</button>
      </li>`;
  });
}

async function del(id) {
  await fetch("http://127.0.0.1:8000/admin/delete", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ doc_id: id })
  });

  loadDocs();
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

loadDocs();
