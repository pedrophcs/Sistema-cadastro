document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    
    if (username === "exemploLogado" && password === "1234") {
        
        window.location.href = "/cadastro"; 
    } else {
        document.getElementById("loginMessage").innerText = "Usuário ou senha incorretos.";
    }
});

