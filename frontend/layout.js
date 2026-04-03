function loadLayout(){

  // prevent duplicate sidebar
  if(document.querySelector(".sidebar")) return;

  const role = localStorage.getItem("role") || "user";
  const email = localStorage.getItem("email") || "User";

  let buttons = "";

// =========================
// ROLE BASED MENU
// =========================
if(role === "leader"){
  buttons = `
    <button onclick="go('leader.html')">Dashboard</button>
    <button onclick="go('users.html')">Users</button>
    <button onclick="go('docs.html')">Documents</button>
    <button onclick="go('chat.html')">Chat</button>
    <button onclick="go('leader-tools.html')">👑 Leader Tools</button>
  `;
}
else if(role === "admin"){
  buttons = `
    <button onclick="go('admin.html')">Dashboard</button>
    <button onclick="go('users.html')">Users</button>
    <button onclick="go('docs.html')">Documents</button>
    <button onclick="go('chat.html')">Chat</button>
  `;
}
else{
  buttons = `
    <button onclick="go('chat.html')">💬 Chat</button>
    <button onclick="go('documents.html')">📄 Documents</button>
    <button onclick="go('announcements.html')">📢 Announcements</button>
  `;
}
  // =========================
  // INSERT SIDEBAR
  // =========================
  document.body.insertAdjacentHTML("afterbegin",`
    <div class="sidebar">

      <div class="profile">
        <h3>${email}</h3>
        <p>${role}</p>
      </div>

      ${buttons}

      <button class="logout" onclick="logout()">🚪 Logout</button>

    </div>

    <canvas id="bgCanvas"></canvas>
  `);

  // =========================
  // ACTIVE BUTTON HIGHLIGHT
  // =========================
  const currentPage = window.location.pathname;

  document.querySelectorAll(".sidebar button").forEach(btn => {
    const onclick = btn.getAttribute("onclick");

    if(onclick && currentPage.includes(onclick.split("'")[1])){
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
function go(page){
  window.location.href = "/static/" + page;
}

/* =========================
   LOGOUT
========================= */
function logout(){
  localStorage.clear();
  window.location.href = "/static/login.html";
}