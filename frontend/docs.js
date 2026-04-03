const API = "http://127.0.0.1:8000";

async function loadDocs() {
  try {
    const token = localStorage.getItem("token");

    const res = await fetch(API + "/admin/docs", {
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    if (!res.ok) {
      console.error("API error:", res.status);
      return;
    }

    const result = await res.json();

    console.log("DOC RESPONSE:", result);

    // HANDLE ALL CASES
    const docs = result.docs || result.documents || result;

    const container = document.getElementById("docs");
    container.innerHTML = "";

    if (!docs || docs.length === 0) {
      container.innerHTML = "<p>No documents found</p>";
      return;
    }

    docs.forEach(doc => {
      const div = document.createElement("div");
      div.className = "item";

      div.innerHTML = `
        <div>
          <b>${doc.title || doc.filename || "Document"}</b><br>
          ${doc.filename || ""}
        </div>

        <div>
          <a href="${API}/documents/preview/${doc.id}" target="_blank">
            <button>Preview</button>
          </a>

          <a href="${API}/documents/download/${doc.id}">
            <button>Download</button>
          </a>
        </div>
      `;

      container.appendChild(div);
    });

  } catch (err) {
    console.error("Error:", err);
  }
}