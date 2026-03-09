async function sendQuestion(){

const question = document.getElementById("question").value
const chatBox = document.getElementById("chatBox")

if(!question) return

chatBox.innerHTML += `<div class="user">You: ${question}</div>`

const aiMode = document.getElementById("aiMode").checked

const mode = aiMode ? "ai" : "doc"

try{

const res = await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
question:question,
mode:mode
})

})

const data = await res.json()

chatBox.innerHTML += `<div class="bot">Bot: ${data.answer}</div>`

}catch{

chatBox.innerHTML += `<div class="bot">Bot: Server error</div>`

}

document.getElementById("question").value=""

}