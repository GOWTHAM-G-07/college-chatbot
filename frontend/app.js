async function login(){
  let r = await fetch("http://127.0.0.1:8000/login",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:new URLSearchParams({email, password})
  });
  let d = await r.json();
  localStorage.setItem("role", d.role);
  location.href = d.role=="admin"?"admin.html":"chat.html";
}

async function send(){
  let r = await fetch("http://127.0.0.1:8000/search",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:new URLSearchParams({query:q.value})
  });
  let d = await r.json();
  box.innerHTML += `<div>${d.answer}</div>`;
}

async function upload(){
  let f=new FormData();
  f.append("title",title.value);
  f.append("file",file.files[0]);
  await fetch("http://127.0.0.1:8000/admin/upload",{method:"POST",body:f});
}
