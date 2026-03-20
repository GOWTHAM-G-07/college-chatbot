function loadLayout(){

// prevent duplicate
if(document.querySelector(".sidebar")) return

document.body.insertAdjacentHTML("afterbegin",`

<div class="sidebar">

<h3 id="username">User</h3>
<p id="role">Role</p>

<button onclick="go('chat.html')">💬 Chat</button>
<button onclick="go('documents.html')">📄 Documents</button>
<button onclick="go('announcements.html')">📢 Announcements</button>
<button onclick="go('news.html')">📰 News</button>

<button class="logout" onclick="logout()">🚪 Logout</button>

</div>

<canvas id="bgCanvas"></canvas>

`)

// set user info
setTimeout(()=>{
document.getElementById("username").innerText =
localStorage.getItem("email") || "User"

document.getElementById("role").innerText =
localStorage.getItem("role") || "Role"
},100)

}

/* navigation */
function go(page){
window.location.href="/static/"+page
}

/* logout */
function logout(){
localStorage.clear()
location.href="/static/login.html"
}