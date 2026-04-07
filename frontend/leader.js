const API = "http://127.0.0.1:8000";

let allUsers = [];

/* =========================
   LOAD ALL
========================= */
window.onload = () => {
  loadLayout();
  loadStats();
  loadUsers();
  loadDocs();
};

/* =========================
   LOAD STATS
========================= */
async function loadStats() {
  try {
    const res = await fetch(API + "/auth/leader/stats", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    });

    if (res.status === 401) {
      window.location.href = "/login.html";
      return;
    }

    const data = await res.json();

    // 📊 TEXT BLOCK
    document.getElementById("stats").innerHTML = `
      👥 Total Members: <b>${data.total || 0}</b><br>
      👨‍🎓 Users: <b>${data.users || 0}</b><br>
      🛡️ Admins: <b>${data.admins || 0}</b><br>
      👑 Leaders: <b>${data.leaders || 0}</b>
    `;

    // ✅ FIXED CARD VALUE
    document.getElementById("userCount").innerText =
      data.users || 0;

  } catch (err) {
    console.error("Stats error:", err);
  }
}

/* =========================
   LOAD USERS
========================= */
async function loadUsers() {
  try {
    const res = await fetch(API + "/auth/admin/users", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    });

    if (res.status === 401) {
      window.location.href = "/login.html";
      return;
    }

    const users = await res.json();

    if (!Array.isArray(users)) {
      console.error("Invalid users response:", users);
      return;
    }

    allUsers = users;
    renderUsers(users);

  } catch (err) {
    console.error("Users load error:", err);
  }
}

/* =========================
   RENDER USERS
========================= */
function renderUsers(users) {

  const container = document.getElementById("users");

  let html = `
    <div class="user-row user-header">
      <div>Name</div>
      <div>Email</div>
      <div>Role</div>
      <div style="text-align:right;">Actions</div>
    </div>
  `;

  users.forEach(u => {
    html += `
      <div class="user-row">

        <div>${u.name || "N/A"}</div>

        <div class="user-email" title="${u.email}">
          ${u.email}
        </div>

        <div>
          <select onchange="changeRole('${u.email}', this.value)">
            <option value="user" ${u.role==="user"?"selected":""}>User</option>
            <option value="admin" ${u.role==="admin"?"selected":""}>Admin</option>
            <option value="leader" ${u.role==="leader"?"selected":""}>Leader</option>
          </select>
        </div>

        <div class="user-actions">
          <button onclick="deleteUser('${u.email}')">Delete</button>
        </div>

      </div>
    `;
  });

  container.innerHTML = html;
}

/* =========================
   SEARCH USERS
========================= */
function filterUsers() {
  const q = document.getElementById("searchUser").value.toLowerCase();

  const filtered = allUsers.filter(u =>
    u.email.toLowerCase().includes(q) ||
    (u.name || "").toLowerCase().includes(q)
  );

  renderUsers(filtered);
}

/* =========================
   DELETE USER
========================= */
async function deleteUser(email) {
  if (!confirm("Delete user?")) return;

  try {
    await fetch(API + "/auth/admin/remove-user/" + email, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    });

    loadUsers();

  } catch (err) {
    console.error("Delete error:", err);
  }
}

/* =========================
   CHANGE ROLE (LEADER)
========================= */
async function changeRole(email, role) {

  try {
    const res = await fetch(API + "/auth/leader/update-role", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ email, role })
    });

    const data = await res.json();

    alert(data.message || "Role updated");

    loadUsers();

  } catch (err) {
    console.error("Role update error:", err);
  }
}

/* =========================
   LOAD DOCUMENTS
========================= */
async function loadDocs() {
  try {
    const res = await fetch(API + "/admin/docs", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    });

    if (res.status === 401) {
      window.location.href = "/login.html";
      return;
    }

    const docs = await res.json();

    const container = document.getElementById("docs");

    // COUNT FIX
    document.getElementById("docCount").innerText = docs.length;

    if (!docs || docs.length === 0) {
      container.innerHTML = "<p>No documents found</p>";
      return;
    }

    let html = "";

    docs.forEach(doc => {
      html += `
        <div class="doc-row">
          <div>${doc.title || doc.filename}</div>
          <div>
            <button onclick="previewDoc(${doc.id})">Preview</button>
            <button onclick="downloadDoc(${doc.id})">Download</button>
            <button onclick="deleteDoc(${doc.id})">Delete</button>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;

  } catch (err) {
    console.error("Docs error:", err);
  }
}

/* =========================
   DOC ACTIONS
========================= */
function previewDoc(id){
  window.open(API + "/documents/preview/" + id, "_blank");
}

function downloadDoc(id){
  window.open(API + "/documents/download/" + id);
}

async function deleteDoc(id){
  if(!confirm("Delete document?")) return;

  try {
    await fetch(API + "/admin/delete/" + id, {
      method:"DELETE",
      headers:{
        Authorization:"Bearer " + localStorage.getItem("token")
      }
    });

    loadDocs();

  } catch (err) {
    console.error("Delete doc error:", err);
  }
}