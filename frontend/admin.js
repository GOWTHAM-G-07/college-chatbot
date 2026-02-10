function upload() {
  const title = document.getElementById("title").value;
  const file = document.getElementById("file").files[0];

  if (!title || !file) {
    showToast("Please fill all fields", false);
    return;
  }

  const form = new FormData();
  form.append("title", title);
  form.append("file", file);

  fetch("http://127.0.0.1:8000/admin/upload", {
    method: "POST",
    body: form
  })
  .then(res => res.json())
  .then(data => {
    showToast(data.message, true);
  })
  .catch(() => {
    showToast("Upload failed", false);
  });
}

function showToast(msg, success) {
  const toast = document.getElementById("toast");
  toast.innerText = msg;
  toast.className = success ? "toast success" : "toast error";
  toast.style.display = "block";

  setTimeout(() => {
    toast.style.display = "none";
  }, 3000);
}
