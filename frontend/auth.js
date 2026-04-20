const API = "http://127.0.0.1:8000"

async function checkAuth(requiredRole){

    const token = localStorage.getItem("token")

    if(!token){
        location.href = "/static/login.html"
        return
    }

    try{

        const res = await fetch(API + "/auth/me",{
            headers:{
                Authorization: "Bearer " + token
            }
        })

        if(!res.ok){
            throw new Error()
        }

        const user = await res.json()

        // set sidebar user info
        if(document.getElementById("username")){
            document.getElementById("username").innerText = user.email
        }

        if(document.getElementById("role")){
            document.getElementById("role").innerText = user.role
        }

        // role protection
        if(requiredRole && user.role !== requiredRole){
            alert("Access Denied")
            location.href = "/static/login.html"
        }

    }catch{
        localStorage.clear()
        location.href = "/static/login.html"
    }
}