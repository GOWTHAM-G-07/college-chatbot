// =========================
// LOAD LAYOUT
// =========================
async function loadLayout() {

  const token = localStorage.getItem("token");

  if (!token) {
    location.href = "/static/login.html";
    return;
  }

  let user;

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/me", {
      headers: {
        Authorization: "Bearer " + token
      }
    });

    if (!res.ok) throw new Error("Invalid token");

    user = await res.json();

  } catch (err) {
    console.error("Auth error:", err);
    localStorage.clear();
    location.href = "/static/login.html";
    return;
  }

  const email = user.email;
  const role = user.role;

  let buttons = "";

  // =========================
  // ROLE BASED MENU (SECURE)
  // =========================

  if (role === "leader") {
    buttons = `
      <button onclick="go('leader.html')">📊 Dashboard</button>
      <button onclick="scrollToSection('users')">👥 Users</button>
      <button onclick="scrollToSection('docs')">📄 Documents</button>
      <button onclick="go('announcements.html')">📢 Announcements</button>
      <button onclick="go('chat.html')">💬 Chat</button>
      <button onclick="go('leader-tools.html')">👑 Leader Tools</button>
    `;
  }

  else if (role === "admin") {
    buttons = `
      <button onclick="go('admin.html')">📊 Dashboard</button>
      <button onclick="scrollToSection('users')">👥 Users</button>
      <button onclick="scrollToSection('docs')">📄 Documents</button>
      <button onclick="go('announcements.html')">📢 Announcements</button>
      <button onclick="go('chat.html')">💬 Chat</button>
    `;
  }

  else if (role === "subleader") {
    buttons = `
      <button onclick="go('leader.html')">📊 Dashboard</button>
      <button onclick="scrollToSection('users')">👥 Users</button>
      <button onclick="go('chat.html')">💬 Chat</button>
    `;
  }

  else {
    buttons = `
      <button onclick="go('chat.html')">💬 Chat</button>
      <button onclick="go('documents.html')">📄 Documents</button>
      <button onclick="go('announcements.html')">📢 Announcements</button>
    `;
  }

  // =========================
  // PREVENT DUPLICATE SIDEBAR
  // =========================
  if (document.querySelector(".sidebar")) return;

  // =========================
  // INSERT SIDEBAR
  // =========================
  document.querySelector(".main").insertAdjacentHTML("afterbegin", `
    <div class="sidebar">

      <div class="profile">
        <h3>${email}</h3>
        <p>${role}</p>
      </div>

      ${buttons}

      <button class="logout" onclick="logout()">🚪 Logout</button>

    </div>
  `);

  // =========================
  // ACTIVE BUTTON HIGHLIGHT
  // =========================
  const currentPage = window.location.pathname.split("/").pop();

  document.querySelectorAll(".sidebar button").forEach(btn => {

    const onclick = btn.getAttribute("onclick");

    if (onclick && onclick.includes(currentPage)) {
      btn.classList.add("active");
    }

    btn.addEventListener("click", () => {
      document.querySelectorAll(".sidebar button")
        .forEach(b => b.classList.remove("active"));

      btn.classList.add("active");
    });

  });
}


// =========================
// NAVIGATION
// =========================
function go(page) {
  window.location.href = "/static/" + page;
}


// =========================
// SCROLL
// =========================
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth" });
}


// =========================
// LOGOUT
// =========================
function logout() {
  localStorage.clear();
  window.location.href = "/static/login.html";
}


// =========================
// 🔥 MAKE FUNCTIONS GLOBAL (FIX)
// =========================
window.loadLayout = loadLayout;
window.go = go;
window.logout = logout;
window.scrollToSection = scrollToSection;