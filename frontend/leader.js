const API = "http://127.0.0.1:8000";

/* =========================
   LOAD ALL
========================= */
window.onload = () => {
  loadLayout();   // sidebar
  loadStats();    // stats
  loadUsers();    // users
  loadDocs();     // documents
};

async function loadStats() {
  const res = await fetch("/auth/leader/stats", {
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token")
    }
  });

  if (res.status === 401) return;

  const data = await res.json();

  console.log("Stats:", data);

  // ✅ FIXED (match backend)
  document.getElementById("stats").innerHTML = `
    Total Users: ${data.total_users || 0}<br>
    Admins: ${data.admins || 0}<br>
    Leaders: ${data.leaders || 0}
  `;

  // ✅ UPDATE CARDS
  document.getElementById("userCount").innerText =
    data.total_users || 0;
}

async function loadUsers() {
  try {
    const res = await fetch(API + "/auth/admin/users", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    });

    // 🔐 HANDLE AUTH FAILURE FIRST
    if (res.status === 401) {
      alert("Session expired. Please login again.");
      window.location.href = "/login.html";
      return;
    }

    const data = await res.json();

    // 🧠 VALIDATE RESPONSE TYPE
    if (!Array.isArray(data)) {
      console.error("Invalid users response:", data);
      return;
    }

    const container = document.getElementById("users");
    container.innerHTML = "";

    // HEADER
    container.innerHTML += `
      <div class="user-row user-header">
        <div>Name</div>
        <div>Email</div>
        <div>Role</div>
        <div style="text-align:right;">Actions</div>
      </div>
    `;

    data.forEach(u => {
      container.innerHTML += `
        <div class="user-row">

          <div class="user-name">
            ${u.name || "N/A"}
          </div>

          <div class="user-email" title="${u.email}">
            ${u.email}
          </div>

          <div class="user-role">
            ${u.role}
          </div>

          <div class="user-actions">
            <button onclick="deleteUser('${u.email}')">Delete</button>
            <button onclick="promote('${u.email}')">Promote</button>
            <button onclick="demote('${u.email}')">Demote</button>
          </div>

        </div>
      `;
    });

  } catch (err) {
    console.error("Users load error:", err);
  }
}

/* =========================
   DELETE USER
========================= */
async function deleteUser(email){

  if(!confirm("Delete user?")) return;

  try{
    await fetch(API + "/auth/admin/remove-user/" + email, {
      method:"DELETE",
      headers:{
        Authorization:"Bearer " + localStorage.getItem("token")
      }
    });

    loadUsers();

  }catch(err){
    console.error("Delete error:", err);
  }
}

/* =========================
   PROMOTE USER
========================= */
async function promote(email){

  try{
    await fetch(API + "/auth/promote/" + email, {
      method:"PUT",
      headers:{
        Authorization:"Bearer " + localStorage.getItem("token")
      }
    });

    loadUsers();

  }catch(err){
    console.error("Promote error:", err);
  }
}

/* =========================
   DEMOTE USER
========================= */
async function demote(email){

  try{
    await fetch(API + "/auth/demote/" + email, {
      method:"PUT",
      headers:{
        Authorization:"Bearer " + localStorage.getItem("token")
      }
    });

    loadUsers();

  }catch(err){
    console.error("Demote error:", err);
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

    // 🔐 HANDLE AUTH / ERROR
    if (res.status === 401) {
      alert("Session expired. Please login again.");
      window.location.href = "/login.html";
      return;
    }

    if (!res.ok) {
      console.error("Docs API failed:", res.status);
      return;
    }

    const docs = await res.json();

    console.log("DOCS:", docs); // DEBUG

    const container = document.getElementById("docs");
    container.innerHTML = "";

    // ✅ SAFE ARRAY CHECK
    if (!Array.isArray(docs)) {
      console.error("Invalid docs response:", docs);
      document.getElementById("docCount").innerText = 0;
      return;
    }

    // ✅ UPDATE DOCUMENT COUNT (🔥 THIS WAS MISSING)
    document.getElementById("docCount").innerText = docs.length;

    // ✅ EMPTY STATE
    if (docs.length === 0) {
      container.innerHTML = "<p>No documents found</p>";
      return;
    }

    // ✅ RENDER DOCUMENTS
    docs.forEach(doc => {
      container.innerHTML += `
        <div class="doc-row">

          <div class="doc-title" title="${doc.title || doc.filename}">
            ${doc.title || doc.filename || "Untitled"}
          </div>

          <div class="doc-actions">
            <button onclick="previewDoc(${doc.id})">Preview</button>
            <button onclick="downloadDoc(${doc.id})">Download</button>
            <button onclick="deleteDoc(${doc.id})">Delete</button>
          </div>

        </div>
      `;
    });

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

  await fetch(API + "/admin/delete/" + id, {
    method:"DELETE",
    headers:{
      Authorization:"Bearer " + localStorage.getItem("token")
    }
  });

  loadDocs();
}

/* =========================
   ADD USER (LEADER)
========================= */
async function addUser(){

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  try{
    const res = await fetch(API + "/auth/leader/add-user", {
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ name, email, password, role })
    });

    const data = await res.json();

    alert(data.message || data.detail);

    loadUsers();

  }catch(err){
    console.error("Add user error:", err);
  }
}