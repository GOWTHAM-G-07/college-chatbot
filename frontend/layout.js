function loadLayout(){

document.body.insertAdjacentHTML("afterbegin",`

<div class="bg-animation"></div>

<div class="sidebar">

<div class="profile">
<div class="avatar"></div>
<div>
<p id="username">User</p>
<p id="role">Role</p>
</div>
</div>

<button onclick="go('chat.html')">Chat</button>
<button onclick="go('documents.html')">Documents</button>
<button onclick="go('announcements.html')">Announcements</button>
<button onclick="go('news.html')">News</button>

<button class="logout" onclick="logout()">Logout</button>

</div>

`)
}

/* page navigation */
function go(page){
window.location.href="/static/"+page
}

/* logout */
function logout(){
localStorage.clear()
location.href="/static/login.html"
}
setTimeout(()=>{
document.getElementById("username").innerText =
localStorage.getItem("email") || "User"

document.getElementById("role").innerText =
localStorage.getItem("role") || "Role"
},100)
document.body.insertAdjacentHTML("beforeend", `
<canvas id="bgCanvas"></canvas>
`)