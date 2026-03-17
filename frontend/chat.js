async function sendQuestion(){

const questionInput = document.getElementById("question")
const question = questionInput.value.trim()
const chatBox = document.getElementById("chatBox")

if(!question) return

/* SHOW USER QUESTION */

const questionDiv = document.createElement("div")
questionDiv.className = "question message"
questionDiv.innerText = question

chatBox.appendChild(questionDiv)

questionInput.value = ""

chatBox.scrollTop = chatBox.scrollHeight


/* MODE */

const aiMode = document.getElementById("aiMode").checked
const mode = aiMode ? "ai" : "doc"


/* TYPING INDICATOR */

const typingDiv = document.createElement("div")
typingDiv.className = "answer message"
typingDiv.innerText = "Typing..."

chatBox.appendChild(typingDiv)

chatBox.scrollTop = chatBox.scrollHeight


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

typingDiv.innerText = ""

typeAnswer(typingDiv,data.answer)

}catch{

typingDiv.innerText = "Server error"

}

}


/* AI TYPING EFFECT */

function typeAnswer(element,text){

let i = 0

function typing(){

if(i < text.length){

element.innerHTML += text.charAt(i)

i++

setTimeout(typing,20)

}

}

typing()

}


/* ENTER KEY SUPPORT */

document.getElementById("question")
.addEventListener("keypress",function(e){

if(e.key==="Enter"){
sendQuestion()
}

})