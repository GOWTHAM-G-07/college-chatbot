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

    if (!Array.isArray(docs)) {
      console.error("Invalid response:", docs);
      showToast("Failed to load docs");
      return;
    }

    let container = document.getElementById("docs");
    container.innerHTML = "";

    docs.forEach(doc => {
      container.innerHTML += `
        <div class="row">
          <span>${doc.title}</span>
          <span>
            <button onclick="downloadDoc('${doc.file_path}')">Download</button>
          </span>
        </div>
      `;
    });

  } catch (err) {
    console.error(err);
    showToast("Failed to load docs");
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

  let email = document.getElementById("newEmail").value;
  let password = document.getElementById("newPassword").value;
  let role = document.getElementById("role").value;

  let res = await fetch(API + "/admin/add-user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify({ email, password, role })
  });

  let data = await res.json();

  showToast(data.msg || "User added");
};

/* =========================
   DOWNLOAD
========================= */
function downloadDoc(path) {
  window.open(API + "/" + path);
}

/* =========================
   INIT
========================= */
window.onload = () => {
  loadDocs();
};