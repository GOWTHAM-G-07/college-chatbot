const API = "http://127.0.0.1:8000";

/* =========================
   TOAST
========================= */
function showToast(msg) {
  let toast = document.getElementById("toast");

  if (!toast) return;

  toast.innerText = msg;
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 2000);
}

/* =========================
   LOAD DOCUMENTS
========================= */
async function loadDocs() {

  const token = localStorage.getItem("token");

  if (!token) return;

  try {
    let res = await fetch(API + "/admin/docs", {
      headers: {
        Authorization: "Bearer " + token
      }
    });

    let docs = await res.json();

    let container = document.getElementById("docs");
    container.innerHTML = "";

    // ✅ UPDATE COUNT
    document.getElementById("docCount").innerText = docs.length;

    docs.forEach(doc => {

      let fileName = doc.file_path.split("uploads/").pop();

      container.innerHTML += `
        <div class="row">
          <span>${doc.title}</span>
          <span>Today</span>
          <span>

            <button onclick="previewDoc('${fileName}')">
              Preview
            </button>

            <button onclick="downloadDoc('${fileName}')">
              Download
            </button>

            <button onclick="deleteDoc(${doc.id})">
              Delete
            </button>

          </span>
        </div>
      `;
    });

  } catch (err) {
    console.error(err);
  }
}
/* =========================
   UPLOAD (FINAL WORKING)
========================= */
async function uploadAdmin() {

  const token = localStorage.getItem("token");

  if (!token) {
    alert("❌ Login required");
    return;
  }

  const fileInput = document.getElementById("file");
  const titleInput = document.getElementById("title");

  const file = fileInput.files[0];
  const title = titleInput.value;

  if (!file || !title) {
    alert("❌ Select file and enter title");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", title);

  try {
    const response = await fetch(API + "/admin/upload", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token
      },
      body: formData
    });

    const text = await response.text();

    console.log("STATUS:", response.status);
    console.log("RESPONSE:", text);

    if (response.status === 401) {
      alert("❌ Unauthorized (login again)");
      return;
    }

    if (response.status === 500) {
      alert("❌ Server error — check backend terminal");
      return;
    }

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      alert("❌ Invalid server response");
      return;
    }

    alert("✅ " + (data.msg || "Uploaded"));

    loadDocs();

  } catch (err) {
    console.error(err);
    alert("❌ Upload crashed");
  }
}
/* =========================
   ADD USER
========================= */
window.addUser = async function () {

  const token = localStorage.getItem("token");
  let name = document.getElementById("newName").value;
  let email = document.getElementById("newEmail").value;
  let password = document.getElementById("newPassword").value;

  let roleElement = document.getElementById("role");
  let role = roleElement ? roleElement.value : "user";

 // 🔥 AUTO GENERATE NAME IF EMPTY
if (!name) {
  let prefix = email.split("@")[0];

  // remove numbers
  prefix = prefix.replace(/[0-9]/g, "");

  // keep only alphabets
  prefix = prefix.replace(/[^a-zA-Z]/g, "");

  name = prefix || "user";
}

console.log("DATA:", name, email, password, role);

  try {
    let res = await fetch(API + "/auth/admin/add-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token
      },
      body: JSON.stringify({ name, email, password, role })
    });

    let text = await res.text();
    console.log("RAW RESPONSE:", text);

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      alert("Server error");
      return;
    }

    if (!res.ok) {
      alert(data.detail || "Add user failed");
      return;
    }

    alert("User added successfully");

  } catch (err) {
    console.error(err);
    alert("Add user failed");
  }
};
/* =========================
   DOWNLOAD
========================= */
function downloadDoc(path) {

  // remove "uploads/" if already included
  let fileName = path.split("uploads/").pop();

  let url = API + "/uploads/" + fileName;

  console.log("DOWNLOAD URL:", url);

  window.open(url);
}
/*==========================
user count update
==============================*/
let allUsers = [];
async function loadUsers() {
  try {
    const res = await fetch("/auth/admin/users", {
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
      console.error(users);
      return;
    }

    const container = document.getElementById("users");
    container.innerHTML = "";

    // HEADER
    container.innerHTML += `
      <div class="user-row user-header">
        <div>Name</div>
        <div>Email</div>
      </div>
    `;

    // DATA
    users.forEach(u => {
      container.innerHTML += `
        <div class="user-row">
          <div>${u.name || "N/A"}</div>
          <div class="user-email">${u.email}</div>
        </div>
      `;
    });

  } catch (err) {
    console.error(err);
  }
}
/*==========================
          PREVIEW
============================*/
function previewDoc(path) {
  let fileName = path.split("uploads/").pop();
  let url = API + "/uploads/" + fileName;

  window.open(url, "_blank");
}
/*=============================
     FRONTEND DELETE LOGIC
=================================*/
async function deleteDoc(id) {

  const token = localStorage.getItem("token");

  if (!confirm("Delete this document?")) return;

  try {
    let res = await fetch(API + "/admin/delete/" + id, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token
      }
    });

    let data = await res.json();

    alert(data.msg);

    loadDocs(); // refresh

  } catch (err) {
    console.error(err);
  }
}
/* =========================
   INIT
========================= */
window.onload = () => {
  loadDocs();
  loadUsers();
};