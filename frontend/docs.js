const API="http://127.0.0.1:8000"

async function ocs(){

let res = await fetch(API+"/admin/docs")

let docs = await res.json()

let container=document.getElementById("docs")

container.innerHTML=""

docs.forEach(doc=>{

container.innerHTML+=`

<div class="item">

<div>

<b>${doc.title}</b><br>
${doc.filename}

</div>

<div>

<a href="/documents/preview/${doc.id}" target="_blank">
<button>Preview</button>
</a>

<a href="/documents/download/${doc.id}">
<button>Download</button>
</a>

</div>

</div>

`

})

}
async function ocs(){

let res = await fetch(API+"/admin/docs",{
headers:{
Authorization:"Bearer "+localStorage.getItem("token")
}
})

let docs = await res.json()

let container=document.getElementById("docs")

container.innerHTML=""

docs.forEach(doc=>{

container.innerHTML+=`

<div class="item">

<div>

<b>${doc.title}</b><br>
${doc.filename}

</div>

<div>

<a href="/documents/preview/${doc.id}" target="_blank">
<button>Preview</button>
</a>

<a href="/documents/download/${doc.id}">
<button>Download</button>
</a>

</div>

</div>

`

})

}