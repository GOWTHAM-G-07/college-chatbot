function loadLayout() {

  const email = localStorage.getItem("email") || "No Email";
  const role = localStorage.getItem("role") || "user";

  let buttons = "";

  // =========================
  // ROLE BASED MENU
  // =========================
  if (role === "leader") {
    buttons = `
      <button onclick="go('leader.html')">Dashboard</button>
      <button onclick="scrollToSection('users')">Users</button>
      <button onclick="scrollToSection('docs')">Documents</button>
      <button onclick="go('announcements.html')">📢 Announcements</button>
      <button onclick="go('chat.html')">Chat</button>
      <button onclick="go('leader-tools.html')">👑 Leader Tools</button>
    `;
  }
  else if (role === "admin") {
    buttons = `
      <button onclick="go('admin.html')">Dashboard</button>
      <button onclick="scrollToSection('users')">Users</button>
      <button onclick="scrollToSection('docs')">Documents</button>
      <button onclick="go('announcements.html')">📢 Announcements</button>
      <button onclick="go('chat.html')">Chat</button>
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
  // INSERT SIDEBAR (ONLY ONCE)
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
  const currentPage = window.location.pathname;

  document.querySelectorAll(".sidebar button").forEach(btn => {
    const onclick = btn.getAttribute("onclick");

    if (onclick && onclick.includes(currentPage.split("/").pop())) {
      btn.classList.add("active");
    }

    btn.addEventListener("click", () => {
      document.querySelectorAll(".sidebar button")
        .forEach(b => b.classList.remove("active"));

      btn.classList.add("active");
    });
  });
}


/* =========================
   NAVIGATION
========================= */
function go(page) {
  window.location.href = "/static/" + page;
}

/* =========================
   SCROLL (FOR SAME PAGE)
========================= */
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth" });
}

/* =========================
   LOGOUT
========================= */
function logout() {
  localStorage.clear();
  window.location.href = "/static/login.html";
}