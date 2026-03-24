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
aasync function loadDocs() {

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
   UPLOAD
========================= */
async function upload() {

  const token = localStorage.getItem("token");

  if (!token) {
    showToast("Login required");
    return;
  }

  let file = document.getElementById("file").files[0];
  let title = document.getElementById("title").value;

  if (!file || !title) {
    showToast("Fill all fields");
    return;
  }

  let formData = new FormData();
  formData.append("file", file);
  formData.append("title", title);

  try {
    let res = await fetch(API + "/admin/upload", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token
      },
      body: formData
    });

    let data = await res.json();

    showToast(data.msg || "Uploaded");

    loadDocs();

  } catch (err) {
    console.error(err);
    showToast("Upload failed");
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