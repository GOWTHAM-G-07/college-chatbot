async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const form = new FormData();
  form.append("email", email);
  form.append("password", password);

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    body: form
  });

  if (!res.ok) {
    alert("Login failed");
    return;
  }

  const data = await res.json();

  if (data.role === "admin") {
    window.location = "admin.html";
  } else {
    window.location = "chat.html";
  }
}
