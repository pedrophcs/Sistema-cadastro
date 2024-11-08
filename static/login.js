document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Aqui, você pode usar uma API ou lógica do servidor para validar as credenciais
    if (username === "exemploLogado" && password === "1234") {
        // Redireciona para a página de cadastro, no Flask, seria com url_for('/cadastro')
        window.location.href = "/cadastro"; // Redireciona para o cadastro na sua aplicação Flask
    } else {
        document.getElementById("loginMessage").innerText = "Usuário ou senha incorretos.";
    }
});

