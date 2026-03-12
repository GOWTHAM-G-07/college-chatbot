async function sendQuestion(){

const question = document.getElementById("question").value
const chatBox = document.getElementById("chatBox")

if(!question) return

// show question
chatBox.innerHTML += `
<div class="question">
${question}
</div>
`

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

// show answer
chatBox.innerHTML += `
<div class="answer">
${data.answer}
</div>
`

}catch{

chatBox.innerHTML += `
<div class="answer">
Server error
</div>
`

}

document.getElementById("question").value=""

// auto scroll
chatBox.scrollTop = chatBox.scrollHeight

}