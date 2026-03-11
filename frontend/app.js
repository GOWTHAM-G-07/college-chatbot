const API = "http://127.0.0.1:8000";

// -----------------------------
// LOGIN
// -----------------------------
async function login(){

let email = document.getElementById("email").value
let password = document.getElementById("password").value

let r = await fetch(API + "/auth/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
email:email,
password:password
})
})

let d = await r.json()

if(!r.ok){
alert(d.detail)
return
}

localStorage.setItem("token", d.token)
localStorage.setItem("role", d.role)

if(d.role === "admin"){
location.href = "/static/admin.html"
}
else if(d.role === "leader"){
location.href = "/static/leader.html"
}
else{
location.href = "/static/chat.html"
}

}

// -----------------------------
// CHATBOT
// -----------------------------
async function send(){

let q = document.getElementById("q").value

let r = await fetch(API + "/auth/chat",{
method:"POST",
headers:{
"Content-Type":"application/json",
Authorization:"Bearer " + localStorage.getItem("token")
},
body:JSON.stringify({
query:q
})
})

let d = await r.json()

let box = document.getElementById("box")

box.innerHTML += `<div class="msg user">${q}</div>`
box.innerHTML += `<div class="msg bot">${d.response}</div>`

}

// -----------------------------
// ADMIN UPLOAD
// -----------------------------
async function upload(){

let title = document.getElementById("title").value
let file = document.getElementById("file").files[0]

let form = new FormData()

form.append("title",title)
form.append("file",file)

await fetch(API + "/admin/upload",{
method:"POST",
headers:{
Authorization:"Bearer " + localStorage.getItem("token")
},
body:form
})

alert("Upload successful")

}

// -----------------------------
// LOGOUT
// -----------------------------
function logout(){

localStorage.removeItem("token")
localStorage.removeItem("role")

location.href="/static/login.html"

}