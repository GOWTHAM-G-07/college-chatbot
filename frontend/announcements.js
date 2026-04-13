const API = "http://127.0.0.1:8000/api";

let active = "all";

// DATE
document.getElementById("todayDate").innerText =
  new Date().toDateString();

// FILTER
function filter(cat, btn){
  active = cat;

  document.querySelectorAll(".filter-btn")
    .forEach(b => b.classList.remove("active"));

  btn.classList.add("active");

  loadAnnouncements();
}

// LOAD
async function loadAnnouncements(){

  try {
    const res = await fetch(API + "/announcements", {
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("token")
      }
    });

    const data = await res.json();

    updateStats(data);
    render(data);

  } catch {
    document.getElementById("cards").innerHTML =
      "<p style='color:red'>Failed to load</p>";
  }
}

// STATS
function updateStats(data){

  let counts = {
    exam:0,event:0,admin:0,urgent:0,general:0
  };

  data.forEach(a=>{
    const c = a.category || "general";
    counts[c]++;
  });

  document.getElementById("examCount").innerText = counts.exam;
  document.getElementById("eventCount").innerText = counts.event;
  document.getElementById("adminCount").innerText = counts.admin;
  document.getElementById("urgentCount").innerText = counts.urgent;
  document.getElementById("generalCount").innerText = counts.general;
}

// RENDER
function render(data){

  const container = document.getElementById("cards");

  const list = active === "all"
    ? data
    : data.filter(a => (a.category || "general") === active);

  container.innerHTML = list.map(a => `

    <div class="announce-card">

      <div class="card-type">
        ${a.category || "General"}
      </div>

      <div class="card-content">

        <div class="card-title">${a.title}</div>

        <div class="card-body">${a.content}</div>

        <div class="card-footer">
          <span>${new Date(a.date).toLocaleDateString()}</span>

          <div>
            <button class="btn" onclick="copyText('${a.content}')">Copy</button>
            <button class="btn">View</button>
          </div>
        </div>

      </div>

    </div>

  `).join("");
}

// COPY
function copyText(text){
  navigator.clipboard.writeText(text);
  alert("Copied");
}

// INIT
loadAnnouncements();