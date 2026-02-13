const API_BASE = "https://college-chatbot-opdo.onrender.com";

async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {

        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await res.json();

        if (!res.ok || data.error) {
            alert("Login failed");
            return;
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("role", data.role);

        if (data.role === "admin") {
            window.location.href = "/admin";
        } else {
            window.location.href = "/chat";
        }

    } catch (err) {

        console.error(err);
        alert("Server not reachable");

    }
}
