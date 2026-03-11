async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {

        const res = await fetch("http://127.0.0.1:8000/auth/login", {
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

        if (!res.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("role", data.role);

        alert("Login successful");

        if (data.role === "admin") {
            window.location.href = "/static/admin.html";
        } else {
            window.location.href = "/static/chat.html";
        }

    } catch (error) {

        console.error(error);
        alert("Cannot connect to backend server");

    }
}